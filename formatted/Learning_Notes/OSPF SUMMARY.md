# OSPF SUMMARY

Source: <https://momcanfixanything.com/ospf-summary/>

* *OSPF PACKET TYPES**

![](image/922d09f7fc22999536aeea3f599ac188.png)

* *HELLO PACKETS**

![](image/7d1d0566a0cce54a53f73585b2ab6db4.png)

* *Adjacencies formation:**

An adjacency could fail if there is a mismatch of any of the following parameters:

- MTU (stuck in exstart)
- Network address
- Subnet mask
- Hello interval and/or dead interval
- Area type
- Authentication
- Area id
- Interface type (broadcast, ptp, ptmp…)

OR if there is a Duplicate RID or IP address

* *DR ELECTION**

- Highest priority wins
- Default priority is 128
- Priority = 0 means ineligible
- Highest RID if same priority
- Election NOT deterministic

- Election occurs within the first 40 sec of OSPF coming up

- No preemption
- point-to-point link (**set protocols ospf area  interface  interface-type p2p**) => no DR

* *LSA TYPES:**

![](image/3eb6825507aff0c2923966834c8171ae.png)

- **ONLY LSA with domain scope = LSA type 5!!!**

![](image/c2a19ff7af4ad7e9448faad6fe5217da.png)

* *LSA TYPES AND AREA TYPE:**

![](image/67ba43cc51c7bbfdac833fde4e4bc3cc.png)

* *LSAs HEADER:**

![](image/689a3fed56a5db9bf02f36e579f81226.png)

```text
*LINK STATE TYPE AND LINK STATE ID:**
Meaning of **LINK STATE ID** field in the **LSA HEADER** depends on the LSA type:
```
![](image/90f287782b465d3669eb40a841e5b202.png)

* *LSA TYPE 1**

![](image/a82e009b2ae8e048fd6f466d98cf4ac5.png)

Meaning of **LINK ID** and **LINK DATA** fields, within the **ROUTER LSA** (TYPE 1), depends on the **LINK TYPE**:

![](image/a917abc4d91465081927275fcd8e3f45.png)

How to remember? For Link Types 1, 2, and 4 Link ID = neighbors info, Link Data = Local info.

* *NOTE**: A point to point link is advertised with TWO LSAs Type 1 (Link type 1 and link type 3):

![](image/119c531b9711f29e2335aaac5eb0d04d.png)

* *LSA TYPE 2**

![](image/0fadee52582d016f5d6f1939ef06ec19.png)

Network LSA does NOT contain any prefix information, though it advertises the subnet mask for the network.

* *LSA TYPE 3**

![](image/869b22ac0b61298a996cb371b2d2c436.png)

```text
For **LSAs type 3**, the **advertised prefix** is in the **LINK STATE ID** (in the **LSA HEADER**).
```
* *LSA TYPE 4**

![](image/8ca44bb55447e186bba5a33e67306286.png)

```text
For **LSAs type** **4,** the **advertised ASBR RID** is in the **LINK STATE ID** (in the **LSA HEADER**).
```
* *LSA TYPE 5**

![](image/0be326c4c56acc32b521f6633206d928.png)

External LSAs header E-bit:

![](image/83d55063f789e6fb284fecf206f6c7e0.png)

* *LSA TYPE 7**

Same format as LSA Type 5

Translated into an AS external LSA (Type 5) by the ABR at the NSSA border. This CANNOT be disabled!

If more than one ABR exists the one with the highest RID does the translation.

* *Other LSAs supported by Junos:**

- Type 9: used for graceful restart capability
- Type 10: used for MPLS traffic engineering

* *ADVERTISEMENT OF DEFAULT ROUTE INTO AREAS**

* *Default route not advertised into NSSA area or stub area by default**. Use **default-metric** command.

![](image/270e128fb260e656ef1bba34eae256b2.png)

* *Default-route** advertised as an **LSA type 3 for a STUB area**; as an **LSA type 7 or type 3 on NSSA** depending on configuration.

![](image/47c25928a2d9268eca35cf1b4bead9a5.png)

* *ROUTE SUMMARIZATION**

Only an ABR can summarize prefixes.

You **CANNOT summarize LSAs type 1 and type 2**, but an ABR can summarize prefixes learned from LSAs type 1 and type 2 and place the summary into LSAs type 3, instead of the specific prefixes.

![](image/ff2ed9f61387fc26aac2126b63a24b39.png)

This is NOT possible!

![](image/900b1e309aa908277e9d3d91bee39d42.png)

Default behavior.

![](image/e485c3abfceecd86592040d1acbf0633.png)

Also, just like LSAs type 1 and type 2 cannot be summarized, LSAs type 5 cannot be summarize. However, an ABR that is translating LSAs type 7 into LSAs type 5 can summarize prefixes, within the LSA type 5.

![](image/3ca86db60472fe6c63cb9c1d7e2123d8.png)![](image/c512a1efb963e241bcb291718c24e98f.png)

* *Regular area:**

* *set area  area-range**  **[restrict]**

- Configured on the ABR only!!!
- Summarizes prefixes injected by the ABR, into an area (within LSAs type 3.
- ABR learns about these prefixes from **LSAs type 1 and type 2**.
- Specific prefixes are suppressed automatically
- Restrict option can be used to filter prefixes.

* *EXAMPLE:**

* *set area 1 area-range 10.1.0/22**

Summarizes all prefixes within the 10.1.0/22 range.

![](image/e485c3abfceecd86592040d1acbf0633.png)

* *set area 1 area-range 10.1.0/22** **[restrict]**

![](image/097a571d15d4fa1f675c23bb0222d6b0.png)

Because all specific prefixes are suppressed automatically, and the restrict suppresses the summary, this effectively filters LSAs type 3.

The example summarizes all prefixes within the 10.1.0/22 range, but the restrict action suppresses the update.

* *NSSA area:**

* *set area  nssa default-lsa** **area-range**  **[restrict]**

- Configured on the ABR only!!!
- Summarizes prefixes injected by the ABR, into an area (within LSAs type 5) when translating from LSAs type 7 into LSAs type 5..
- ABR learns about these prefixes from **LSAs type 7**
- Specific prefixes are suppressed automatically
- Restrict option can be used to filter prefixes.

* *EXAMPLE:**

* *set area 1 nssa default-lsa** **area-range 10.1.0/22**

![](image/c512a1efb963e241bcb291718c24e98f.png)

Summarizes all prefixes within the 10.1.0/22 range.

* *set area 1 area-range 10.1.0/22** **[restrict]**

![](image/7d40094f4ec4132913362df4f56d0a43.png)

Because all specific prefixes are suppressed automatically, and the restrict suppresses the summary, this effectively filters LSAs type 5 (translated from type 7) within the range.

The example summarizes all prefixes within the 10.1.0/22 range, but the restrict action suppresses the update.

* *OSPF ROUTE FILTERING / ROUTING POLICIES and REDISTRIBUTION**

LSAs filtering is NOT possible. The database of ALL routers within an area must be identical. You can limit propagation of some LSAs by converting the area into a stub, nssa, or stub/nssa no-summaries.

Routing policies can be used to control creation and propagation of LSAs type 3 and LSAs type 5.

LSAs 1 and 2 cannot controlled with any routing policies policies.

![](image/f499ffd6878ce2dc670224c263a05ccd.png)![](image/1fc77680d1841fe07590033977eb420a.png)

* *JUNOS <=> IOS**

![](image/04e869f75b4e647d97efe8d4552d4b62.png)

- --

As we can see in the above output, R1 prefers LSAs Type-7 from R2. This is because we are following RFC 3101, which has the following path calculation preference

1. A Type-7 LSA with the P-bit set.

2. A Type-5 LSA.

3. The LSA with the higher router ID.

Note: Please be aware that the following path calculation preference is applicable if the current LSA is functionally the same as an installed LSA. We can verify that the forwarding metric for both LSAs are the same looking at Type-1 LSA of R1.
