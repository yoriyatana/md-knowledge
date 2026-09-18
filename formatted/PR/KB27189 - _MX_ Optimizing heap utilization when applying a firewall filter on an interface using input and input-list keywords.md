# KB27189 - [MX] Optimizing heap utilization when applying a firewall filter on an interface using input and input-list keywords

<https://kb.juniper.net/InfoCenter/index?page=content&id=KB27189&cat=MX5_1&actp=LIST>

* *SUMMARY:**

This article provides background data about heap utilization to help making an informed decision when applying a firewall filter on an interface with input and input-list keywords. The data illustrates conclusively the theory of heap utilization on a line card with regard to firewall filters. The article supplements information available in the MX Series technical documentation, and is useful to evaluate issues of heap utilization when considering to scale up the network footprint.

* *SYMPTOMS:**

A firewall filter generates different heap utilization on the MPC1 line card when applied on the 10-GbE interface by using **input**and **input-list** keywords. For example, when using:

- **input** keywords, the heap is **6%**.
- **input-list** keywords,the heap is **23%**.

What is the cause of this difference in heap utilization, when the same filter is applied by using **input** or **input-list** keywords?

By definition, input or output filter lists create interface-specific filters, regardless of whether the firewall filters in the list were configured as interface-specific. For more information, refer to the **Interface-Specific Names for Filter Lists** section in the following link:

[www.juniper.net/techpubs/en\_US/junos/topics/concept/firewall-filter-option-multiple-listed-overview.html](http://www.juniper.net/techpubs/en_US/junos/topics/concept/firewall-filter-option-multiple-listed-overview.html)

Even then, the application of the same firewall-filter as **interface-specific** with **input** keyword generates a different heap usage, as compared to the same filter being applied, without **interface-specific,** in the **input-list**.

The test results in Cases 1 through 4 in this section explain the issue in detail:

* *Case 1 - Interface-specific firewall filter is applied as input**:

[edit]

jtac@ERX-MX960-2-RE0# run show chassis fpc | match "Temp|Slot|Online"

Temp  CPU Utilization (%)  Memory    Utilization (%)

Slot State            (C)  Total  Interrupt      DRAM (MB) Heap    Buffer

1  Online            43    20          0      2048        9        13

3  Online            42    19          0      2048        9        13

8  Online            42    19          0      2048        9        13

10  Online            40    19          0      2048        6        17  < Heap 6%

[edit]

jtac@ERX-MX960-2-RE0# show interfaces xe-10/1/0 | match input

input TEST-ACL-V4;

input TEST-ACL-V4;

input TEST-ACL-V4;

input TEST-ACL-V4;

[edit]

jtac@ERX-MX960-2-RE0# show interfaces xe-10/1/0 | match input | count

Count: 999 lines

[edit groups  firewall family inet]

jtac@ERX-MX960-2-RE0# show filter TEST-ACL-V4

interface-specific;

term block-to-internal {

from {

destination-prefix-list {

internal-v4;

}

}

* *Case 2 - Non interface-specific firewall filter is applied as input**:

[edit]

jtac@ERX-MX960-2-RE0# run show chassis fpc | match "Temp|Slot|Online"

Temp  CPU Utilization (%)  Memory    Utilization (%)

Slot State            (C)  Total  Interrupt      DRAM (MB) Heap    Buffer

1  Online            43    20          0      2048        9        13

3  Online            42    19          0      2048        9        13

8  Online            42    20          0      2048        9        13

10  Online            41    21          0      2048        6        17  < Heap 6%

[edit]

jtac@ERX-MX960-2-RE0# show interfaces xe-10/1/0 | match input

input TEST-ACL-V4;

input TEST-ACL-V4;

input TEST-ACL-V4;

input TEST-ACL-V4;

[edit]

jtac@ERX-MX960-2-RE0# show interfaces xe-10/1/0 | match input | count

Count: 999 lines

[edit groups  firewall family inet]

jtac@ERX-MX960-2-RE0# show filter TEST-ACL-V4 < not interface-specific

term block-to-internal {

from {

destination-prefix-list {

internal-v4;

}

}

then {

count to-internal-v4-dscd;

discard;

}

}

* *Case 3 - Interface-specific firewall filter is applied by using input-list**:

[edit]

jtac@ERX-MX960-2-RE0# run show chassis fpc | match "Temp|Slot|Online"

Temp  CPU Utilization (%)  Memory    Utilization (%)

Slot State            (C)  Total  Interrupt      DRAM (MB) Heap    Buffer

1  Online            42    21          0      2048      23        13

3  Online            42    18          0      2048      22        13

8  Online            42    20          0      2048      22        13

10  Online            40    20          0      2048      23        17  < Heap 23%

[edit]

jtac@ERX-MX960-2-RE0# show interfaces xe-10/1/0 | match input

input-list TEST-ACL-V4;

input-list TEST-ACL-V4;

input-list TEST-ACL-V4;

input-list TEST-ACL-V4;

[edit]

jtac@ERX-MX960-2-RE0# show interfaces xe-10/1/0 | match input | count

Count: 1001 lines

[edit groups  firewall family inet]

jtac@ERX-MX960-2-RE0# show filter TEST-ACL-V4

interface-specific;

term block-to-internal {

from {

destination-prefix-list {

internal-v4;

}

}

* *Case 4 - Non interface-specific firewall filter is applied by using input-list**:

[edit]

jtac@ERX-MX960-2-RE0# run show chassis fpc | match "Temp|Slot|Online"

Temp  CPU Utilization (%)  Memory    Utilization (%)

Slot State            (C)  Total  Interrupt      DRAM (MB) Heap    Buffer

1  Online            42    20          0      2048      23        13

3  Online            42    20          0      2048      22        13

8  Online            42    19          0      2048      22        13

10  Online            40    19          0      2048      23        17 < Heap 23%

[edit]

jtac@ERX-MX960-2-RE0# show interfaces xe-10/1/0 | match input

input-list TEST-ACL-V4;

input-list TEST-ACL-V4;

input-list TEST-ACL-V4;

input-list TEST-ACL-V4;

[edit]

jtac@ERX-MX960-2-RE0# show interfaces xe-10/1/0 | match input | count

Count: 999 lines

[edit groups  firewall family inet]

jtac@ERX-MX960-2-RE0# show filter TEST-ACL-V4

term block-to-internal {

from {

destination-prefix-list {

internal-v4;

}

}

then {

count to-internal-v4-dscd;

discard;

}

}

* *CAUSE:**

* *SOLUTION:**

The test results appearing in the "Problem or Goal" section of this article give useful information on the behavior of heap utilization when applying firewall filters with **input** or **input-list** keywords. The conclusions based on this data should be used when evaluating to scale up the network, and applied depending on the network configuration:

- More heap memory is required if the firewall filter is attached to multiple interfaces via **input-list** or **output-list** keywords(Case 3 and Case 4). This is because a separate **filter definition**, or filter program, is created for each interface. The available technical documentation refers to this instance as interface-specific.
- An interface-specific firewall filter that is configured via CLI and attached to multiple interfaces by the **input** or **output** keyword (Case 1), produces a single **filter definition**, thus lower heap memory utilization. This is in contrast to the interface-specific instance that creates separate policers/counters for each interface in the ASIC memory (not heap memory).
- A non interface-specific firewall filter that is attached to multiple interfaces by using an **input** or **output** filter keyword (Case 2) produces a single **filter definition** and only a single set of counters/policers in the ASIC memory. The same amount of heap memory is utilized, similar to Case 4, but lower ASIC memory utilization. In this case, there are no separate counters/policers per interface, only a single policer/counter in the ASIC memory.
