# Port mirror on Juniper MX

+ [MX] Example: Configuring port mirroring on MX devices

From <https://kb.juniper.net/InfoCenter/index?page=content&id=kb33488>

+ [MX] Example Configuration of port-mirroring in logical systems

From <https://kb.juniper.net/InfoCenter/index?page=content&id=KB32566&cat=MX480_1&actp=LIST>

+ [MX] Configuring port mirroring to mirror MPLS traffic without using an instance

From <https://kb.juniper.net/InfoCenter/index?page=content&id=KB33518&cat=MX2020&actp=LIST>
Miror được traffic MPLS, inet, vpls, bridge (đã test thử)

# Cấu hình cổng gắn laptop để bắt wireshark:
set interfaces ge-5/0/1 encapsulation ethernet-bridge
set interfaces ge-5/0/1 unit 0 family bridge
set bridge-domains PORT-MIRROR interface ge-5/0/1.0

# Cấu hình các option liên quan đến port-mirror:
set forwarding-options port-mirroring input rate 1
set forwarding-options port-mirroring family any output interface ge-5/0/1.0

# Cấu hình firewall để mirror:
set firewall family any filter port-mirror term mirror then count port-mirror
set firewall family any filter port-mirror term mirror then port-mirror
set firewall family any filter port-mirror term mirror then accept

# Apply vào các unit cần mirror:
set interfaces ae0 unit 151 filter input port-mirror
set interfaces ae0 unit 151 filter output port-mirror
set interfaces ae0 unit 1024 filter input port-mirror
set interfaces ae0 unit 1024 filter output port-mirror
set interfaces ae0 unit 3000 filter input port-mirror
set interfaces ae0 unit 3000 filter output port-mirror

Note:
Không mirror được traffic host outbound (do ko đi qua lookup chip).
https://kb.juniper.net/InfoCenter/index?page=content&id=KB33762&actp=RSS
