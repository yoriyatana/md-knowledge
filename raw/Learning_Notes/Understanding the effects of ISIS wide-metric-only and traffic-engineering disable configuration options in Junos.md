# Understanding the effects of ISIS wide-metric-only and traffic-engineering disable configuration options in Junos

<https://kb.juniper.net/InfoCenter/index?page=content&id=KB25145&act=login>

SUMMARY:

This article provides information about the effects of ISIS wide-metrics-only and traffic-engineering disable configuration options in Junos.

SYMPTOMS:

- When ISIS wide-metrics-only is configured for a level or interface, TLV`s 2 and 128 are suppressed from being sent by the local router.
- When ISIS Traffic Engineering is disabled, TLV`s 22, 134, and 135 are suppressed from being sent.
- The combination of wide-metrics-only and traffic-engineering disable under protocols ISIS will result in the total loss of ISIS routing information for that level.
- This combination suppresses TLV`s 2, 22, 128, 134, and 135 from being sent.

---

- Compared to the previous LSP output, TLV 2 and TLV 128 are missing, as the wide-metrics-only option is enabled. TLV`s corresponding to the narrow (old style) metric are suppressed
  
- 'Suppressed' indicates that the local router, which is configured for wide-metric, does not send TLVs 2 and 128; but accepts them, if received.

---

> Note:
>
> - TLV`s 2, 22, 128, 134, and 135 are suppressed from being sent.
>   
> - Essentially, no IP prefix and IS neighbor information are exchanged.
>   
> - So, the routing information is not available.
