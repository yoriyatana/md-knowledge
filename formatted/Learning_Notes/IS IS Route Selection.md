# IS IS Route Selection

# **<http://wiki.kemot-net.com/is-is-route-selection>**

# Route Selection

- ISIS Route Selection is based on the following process:

```text
L1 over L2 - select Level 1 routes over Level 2 routes.
Internal over External - if levels are equal, select internal over external.
Lowest Metric - if types are the same select route with lowest metric.
Load Share - if metric is the same for multiple routes, load-share.
```
