# l3vpn hub and spoke

- ở hub site, nếu sử dụng BGP để signalling
    - VRF_HUB sẽ nhận được route có as-path bị loop
    - VRF_SPOKE site HUB sẽ không cần chứa route của CE
