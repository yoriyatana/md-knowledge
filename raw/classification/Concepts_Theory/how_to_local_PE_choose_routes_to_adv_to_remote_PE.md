# how to local PE choose routes to adv to remote PE

When upgrading to Junos OS Release 5.4 or later, be aware that route export behavior differs when using the auto-export command instead of rib-group export:

When you use the rib-group statement to export between routing tables, both primary routes (routes in the originating routing table) and secondary routes (routes imported from other routing tables) are exported to the remote PE routers. When you use the auto-export statement, only the primary routes from the originating routing table are exported.

Routes exported from an originating VRF instance to another on the same PE now honor export policy changes to route attributes. When you use the auto-export statement, you must add the originating route target to the exported routes. With rib-group statements, no additional configuration is necessary.
