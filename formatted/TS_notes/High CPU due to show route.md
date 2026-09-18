# High CPU due to show route

I was checking with engineering team and they confirmed that either you run  any combination of "show route" with large scale is bound to take time to display. In our case of " show route protocols static", it would need to go through all the tree entries and check if its protocol type is static.

- --

The command only filter static route in the inet.0 table and the number of static routes is 1.3k but why is it still causing high CPU?

àIt doesn’t matter the nature of the routes ie static/bgp/ or other protocols but whenever we run show route and filter static the complete routing table has to be parse and it will cause high CPU.

- --

I found the following KB which explains the behavior of running show route command.

<https://kb.juniper.net/InfoCenter/index?page=content&id=KB31807&actp=METADATA>

If customer wants to collect them we can run those commands the 2sec refresh rate is very aggressive you might have to run them at say every 4hrs or so considering there is 900k routes present.
