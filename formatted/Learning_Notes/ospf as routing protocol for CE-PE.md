# ospf as routing protocol for CE-PE

> > it is possible to break a few ospf 'rules' and have it 'work'
>
> First thing is no OSPF rules are being broken nor can be broken in regards to L3VPN because (outside of sham-links) the superbackbone between the PEs are not necessarily treated as directly connected. As they are not treated as such, OSPF's rules do not particularly apply.
>
> By default these are still BGP redistributed routes with logic to properly redistribute them in the LSDB via the use of BGP communities such as rte-type and domain-id. This allows for easy creation and imports of type 3/5 LSAs in the local LSDB. However, the BGP routes are lacking most of the LSA attributes and a PE would not be able to properly add the LSAs required to build the full LSDB.
>
> In order for PEs to have true OSPF adjacency, sham-links are required. When enabled, the PEs exchange OSPF messages tunneled directly over the LSP. This allows for full adjacency and LSDB hence then will follow the full OSPF rules for adj. (P2P anyway) but not for area rules. But this adj. only pertains to the LSDB, not routing. This is a key point in this scenario.
>
> However, in either scenario the BGP routes are still the end-all in the decision process. The received BGP routes and their community along with sham-link adj. are used to build this "pseudo" LSDB. I call this pseudo because OSPF routes received via BGP from a remote PE which are added to the LSDB are not locally significant to the PE (AKA not involved in routing, SFP, etc). The remote routes will only exist as BGP routes and just imported into the LSDB. A local PE only uses the LSDB for local CE routes.
>
> You can try this for yourself by not exporting OSPF VRF routes and building a sham-link. You'll have the full OSFP database at either PE/CE but no routing functionality because this is again reliant on BGP.
>
> When you think the PEs in a L3VPN can break OSPF rules, they are not actually breaking any rules because "OSPF is not really involved" between the PEs.
>
> Also you can have these insane OSPF designs that appear to work but in reality do not because of the explanations above. Since the PEs are simply importing these OSPF routes into the LSDB yet not using them for routing between VRFs, this means routing can appear fine a lot of the time at the PE, but the downstreams CEs can run SPF and improperly select best paths for particular routes because the database is not always equal to the actual BGP routes in the PE's table. This is primarily a concern when backdoor-links are involved.
>
> Summary, yes, you can have some wild and standard breaking OSPF area configurations at each PE and they can still work but when it comes to the CE's LSDB and if there are backdoor-links, routing can break at various points. This is because L3VPN and OSPF is not as interconnected as you think.
>
> ---
>
> L3VPN lets you connect different areas (acting as a superbackbone 'area 0')

First thing is while the L3VPN fabric acts as an OSPF superbackbone and has some analogies to area 0, it's more akin in practice to a standard inter-AS interconnect. AKA, by default, there would little difference in a scenario where no L3VPN was used and the PEs were simply redistributing OSPF into BGP and the inverse.

The route tables and OSPF database would be near identical, albeit it not being a VPN. This is because in either scenario it's still standard redistribution. The only difference is with L3VPN is it provides more control on the OSPF LSDB when routes are redistributed so the proper LSAs are created.

Even with sham-links though, the L3VPN fabric is more analogous to a standard area neighborship because it's actually creating a neighborship.

Essentially, while it lets you connect different areas and type that are not normally possible, it's due to redistribution. The limitation on functionality is down to redistribution and the area types, ex. if one area is a stub, you cannot redistribute because of Type-5 but can make use of the domain-ID tag so they are injected as a Type-3 instead.

> \*Initially I jumped on changing the domain-id however not sure it is required....The 'DOWN' bit (Junos calls this DN bit ), also the domain-id (which is different to the DN bit) and finally automatic tagging. (Junos does it for us but you can see it doing it).

Correct, there are 3 primary mechanisms that are used with L3VPN and OSPF. Each are independent and used simultaneously. There are actually a few more knobs that really let you incorporate overly complex designs too.

> DOWN BIT:

This is simply a loop prevention for redistribution, very important when backdoors are involved. When the PE redistributes the VPN BGP prefix into OSPF, it sets the DN bit flag so that there is not potential of the remote PE from redistributing it again. Type-3/5/7 LSAs support this bit.

> VPN Tag:

If the DN bit is not supported on the device, you can use the VPN Tag instead. This is essentially a fallback when DN bit cannot be used reliably and has the purpose/use.

> Domain ID community:

This is probably the most important when it comes to dealing with different areas or route manipulation. This simple tag ensure routes are redistributed with the correct LSA types. Summed up to if the domain-ids match, it's treated as a Type-3, else it's a Type-5.

> IE: we are using the L3VPN as an induced Superbackbone to seperate the non (NSSA) compatible areas.

So back to the primary scenario. By default (with proper export configurations), this should work for the most part but there may be instances on the CE side in their OSPF LSDB that would result in non-optimal routing or blackholing of traffic.

Again, remember that the key is the PE's are simply constructing their LSAs to build an LSDB. It's uses the BGP redistributed routes for this and when it comes to routing traffic only the BGP routes are used. The PEs are basically advertising this "pseudo" network.

- --

Lưu ý: Trong mô hình hub-spoke, nếu routing giữa hub-PE và hub-CE là OSPF, khi đó hub-downstream-vrf sẽ có hành xử bên dưới khi flooding LSA đến hub-CE:

Đối với LSA Type3: set DN bit (Down bit).

Đối với LSA Type5: set DN bit và VPN-Tag

By default, all LSAs originated by the hub PE router in the spoke routing instance have the DN bit set.  Also, all externally originated LSAs have the VPN route tag set.

For Type 3 summary LSAs, routing loops are not a concern because the hub CE router, as an area border router (ABR), reoriginates the LSAs with the DN bit clear and sends them back to the hub PE router.

However, the hub CE router does not reoriginate external LSAs, because they have an AS flooding scope.

Đây là tính năng chống loop mặc định của giao thức OSPF trong L3VPN. Khi hub-upstream-vrf nhận được các LSA này sẽ xem là bất hợp lệ và không xử lý. Để tránh việc này, thực hiện tắt hành xử này tại vị trí hub-downstream-vrf bằng cách chuyển toàn bộ LSA Type3 sang LSA Type 5 và tắt DN bit khi flooding LSA đến hub-CE bằng cấu hình bên dưới:

domain-id disable;

domain-vpn-tag 0;

domain-id disable; ->> vì dù không set dn bit và vpn-tag là không nhưng HUB VRF cũng không học route này do nghĩ disjoint backbone area. Khi tắt thì PE ở HUB VRF sẽ hành xử như non-ABR.

Lệnh này  có tác dụng với LSA Type 3, convert sang LSA T5

domain-vpn-tag 0; or no-domain-vpn-tag; ->> lệnh này tắt DN bit và set vpn-tag là 0 cho route được advertise từ SPOKE VRF to CE. Lệnh này set ở SPOKE VRF

>- có tác dụng với LSA Type 5

For Type 3 summary LSAs, routing loops are not a concern because the hub CE router, as an area border router (ABR), reoriginates the LSAs with the DN bit clear and sends them back to the hub PE router. However, the hub CE router does not reoriginate external LSAs, because they have an AS flooding scope.

- --

Khi sử dụng vrf-target thì extended community rte-type được tự dộng add vào route quảng bá sang MP-BGP

Khi sử dụng vrf-import/export thì extended community rte-type không được tự dộng add vào route quảng bá sang MP-BGP

>>> Khi sử dụng vrf-import/export thì tất cả route sẽ được remote PE được xem là external (do không có rte-type)

>>> Khi sử dụng vrf-target thì route LSA T 1,2,3 sẽ được remote PE adv theo LSA type 3 (tái tạo từ rte-type)

- --

To get these routes advertised as hub-routes to spoke sites, I have 2 options:

Option 1:

1a. Put CE1's vpnA-dowstream interface in another area, so the Type-3

LSAs will be re-originated at ABR CE1 with DN-bit cleared.

1b. Configure "domain-id disable" in vpnA-downstream instance, to

allow these Type-3 LSAs(DN-bit cleared) to be considered in SPF

algorithm.

(set ref#1)

1c. Configure "domain-vpn-tag 0" in vpnA-upstream instance, to allow

Type-5 LSAs to be considered in SPF algorithm.

Option 2:

2a. Both of the CE's vpnA-upstream/downstream interfaces are in the same area.

2b. Configure "domain-id disable" in vpnA-upstream instance, to flood

Type-3 LSAs with DN-bit cleared. (I found that these LSAs will be

converted to Type-5 LSAs)

2c. Configure "domain-vpn-tag 0" in vpnA-upstream instance, to allow

Type-5 LSAs to be considered in SPF algorithm.

The only difference between Options 1&2 is the route type of remote

OSPF internal spoke routes.

Option 1 will consider them as OSPF/10(Type-3 LSAs)

Option 2 will consider them as OSPF/150(Type-5 LSAs)

Q1: What is the best practice? Option 1, 2 or another approach?

Q2: What are the side effects of "domain-id disable"?

Different domain-ids will make PEs convert remote Type-3 LSAs to

Type-5 LSAs. And "domain-id disable" will clear the DN-bit in Type-3

LSAs.

But I cannot find whether "domain-id disable" makes PEs convert Type-3

LSAs to Type-5 LSAs or not. (According to my test, it will.)

Q3: What are the side effects of "domain-vpn-tag 0"? It will clear the

DN-bit in Type-5 LSAs and set vpn-tag to 0. Anything else?

Q4: In this case, will sham-links help?

Q5: I cannot find usage guidelines of "domain-id disable" and

"domain-vpn-tag 0" for versions after JunOS 12.2. Do these behaviors

change in later versions?

- -

'domain-vpn-tag 0' have the side effect of "remove the DN bit from Type 5 and Type 7 LSAs"

<https://supportportal.juniper.net/s/article/How-to-install-LSA-type-3-LSA-type-5-and-LSA-type-7-OSPF-routes-in-the-VRF-routing-table?language=en_US>

- --

#### Hub-and-Spoke Layer 3 VPNs and OSPF Domain IDs

The default behavior of an OSPF domain ID causes some problems for hub-and-spoke Layer 3 VPNs configured with OSPF between the hub PE router and the hub CE router when the routes are not aggregated. A hub-and-spoke configuration has a hub PE router with direct links to a hub CE router. The hub PE router receives Layer 3 BGP updates from the other remote spoke PE routers, and these are imported into the spoke routing instance. From the spoke routing instance, the OSPF LSAs are originated and sent to the hub CE router.

The hub CE router typically aggregates these routes, and then sends these newly originated LSAs back to the hub PE router. The hub PE router exports the BGP updates to the remote spoke PE routers containing the aggregated prefixes. However, if there are nonaggregated Type 3 summary LSAs or external LSAs, two issues arise with regard to how the hub PE router originates and sends LSAs to the hub CE router, and how the hub PE router processes LSAs received from the hub CE router:

- By default, all LSAs originated by the hub PE router in the spoke routing instance have the DN bit set. Also, all externally originated LSAs have the VPN route tag set. These settings help prevent routing loops. For Type 3 summary LSAs, routing loops are not a concern because the hub CE router, as an area border router (ABR), reoriginates the LSAs with the DN bit clear and sends them back to the hub PE router. However, the hub CE router does not reoriginate external LSAs, because they have an AS flooding scope.

  You can originate the external LSAs (before sending them to the hub CE router) with the DN bit clear and the VPN route tag set to 0 by altering the hub PE router’s routing instance configuration. To clear the DN bit and set the VPN route tag to zero on external LSAs originated by a PE router, configure 0 for the domain-vpn-tag statement at the [edit routing-instances routing-instance-name protocols ospf] hierarchy level. You should include this configuration in the routing instance on the hub PE router facing the hub CE router where the LSAs are sent. When the hub CE router receives external LSAs from the hub PE router and then forwards them back to the hub PE router, the hub PE router can use the LSAs in its OSPF route calculation.
- When LSAs flooded by the hub CE router arrive at the hub PE router’s routing instance, the hub PE router, acting as an ABR, does not consider these LSAs in its OSPF route calculations, even though the LSAs do not have the DN bits set and the external LSAs do not have a VPN route tag set. The LSAs are assumed to be from a disjoint backbone area.

  You can change the configuration of the PE router’s routing instance to cause the PE router to act as a non-ABR by including the disable statement at the [edit routing-instances routing-instance-name protocols ospf domain-id] hierarchy level. You make this configuration change to the hub PE router that receives the LSAs from the hub CE router.

  By making this configuration change, the PE router’s routing instance acts as a non-ABR. The PE router then considers the LSAs arriving from the hub CE router as if they were coming from a contiguous nonbackbone area.

<https://github.com/rendoaw/notes/blob/master/juniper/junos.ospf.domain-id.md>
