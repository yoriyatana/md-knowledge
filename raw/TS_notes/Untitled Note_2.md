# Untitled Note

Providers can specify a source class or destination class for an output firewall filter. Although providers can specify a source class and destination class for an input firewall filter, the counters are incremented only if the firewall filter is applied on the output interface.

The class-based filter match condition works only for output filters because the SCU and DCU are determined after route lookup.
