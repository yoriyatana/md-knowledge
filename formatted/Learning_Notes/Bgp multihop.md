# Bgp multihop

EBGP multihop is kludge to kill this check, but also kludge to kill convergence

of your BGP session, due to disabling fall over on linkdown.

Proper way to disable this check is JunOS 'accept-remote-nexthop' or IOS

'disable-connected-check'.
