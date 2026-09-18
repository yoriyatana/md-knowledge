# LAB advanced_l3vpn_lab_01

---

**LAB L3VPN (advanced)**

---

**Task 1:**

- **R1**:

```
[edit protocols mpls label-switched-path to-r2]
+    ldp-tunneling;
[edit protocols mpls label-switched-path to-r4]
+    ldp-tunneling;
[edit protocols bgp group ibgp]
+     family inet {
+         unicast;
+     }
+     family inet-vpn {
+         unicast;
+     }
+     family inet6-vpn {
+         unicast;
+     }
```

- **R2**:

```
[edit protocols mpls label-switched-path to-r5]
+    ldp-tunneling;
[edit protocols mpls label-switched-path to-r1]
+    ldp-tunneling;
[edit protocols bgp group ibgp]
+     family inet {
+         unicast;
+     }
+     family inet-vpn {
+         unicast;
+     }
+     family inet6-vpn {
+         unicast;
+     }
```

- **R3**:

```
[edit groups interface-family interfaces <ge-0/0/*> unit 0]
+       family mpls;
[edit interfaces]
+   ge-0/0/3 {
+       apply-groups-except interface-family;
+       unit 0 {
+           family inet {
+               address 10.100.1.5/30;
+           }
+       }
+   }
[edit protocols bgp group ibgp]
+     family inet {
+         unicast;
+     }
+     family inet-vpn {
+         unicast;
+     }
+     family inet6-vpn {
+         unicast;
+     }
[edit]
+  policy-options {
+      policy-statement EXPORT_OSPF_CE_C1 {
+          term 1 {
+              from protocol bgp;
+              then accept;
+          }
+      }
+      policy-statement EXPORT_VRF_C1 {
+          term 1 {
+              then {
+                  community add target:123:1;
+                  accept;
+              }
+          }
+          term final {
+              then reject;
+          }
+      }
+      policy-statement IMPORT_VRF_C1 {
+          term 1 {
+              from {
+                  protocol bgp;
+                  community target:123:1;
+              }
+              then accept;             
+          }
+          term final {
+              then reject;
+          }
+      }
+      community target:123:1 members target:123:1;
+  }
+  routing-instances {
+      C1 {
+          instance-type vrf;
+          interface ge-0/0/3.0;
+          route-distinguisher 10.210.1.3:1;
+          vrf-import IMPORT_VRF_C1;
+          vrf-export EXPORT_VRF_C1;
+          inactive: vrf-target target:123:1;
+          vrf-table-label;
+          protocols {
+              ospf {
+                  inactive: domain-id disable;
+                  domain-vpn-tag 0;
+                  export EXPORT_OSPF_CE_C1;
+                  area 0.0.0.0 {
+                      interface ge-0/0/3.0 {
+                          interface-type p2p;
+                      }
+                  }
+              }
+          }
+      }
+  }
```

- **R4**:

```
[edit protocols mpls label-switched-path to-r1]
+    ldp-tunneling;
[edit protocols mpls label-switched-path to-r5]
+    ldp-tunneling;
[edit protocols bgp group ibgp]
+     family inet {
+         unicast;
+     }
+     family inet-vpn {
+         unicast;
+     }
+     family inet6-vpn {
+         unicast;
+     }
```

- **R5**:

```
[edit protocols mpls label-switched-path to-r4]
+    ldp-tunneling;
[edit protocols mpls label-switched-path to-r2]
+    ldp-tunneling;
[edit protocols bgp group ibgp]
+     family inet {
+         unicast;
+     }
+     family inet-vpn {
+         unicast;
+     }
+     family inet6-vpn {
+         unicast;
+     }
```

- **R6**:

```
[edit interfaces]
+   ge-0/0/5 {
+       apply-groups-except interface-family;
+       flexible-vlan-tagging;
+       encapsulation flexible-ethernet-services;
+       unit 11 {
+           vlan-id 11;
+           family inet {
+               address 10.100.1.1/30;
+           }
+       }
+   }
[edit protocols bgp group ibgp]
+     family inet {
+         unicast;
+     }
+     family inet-vpn {
+         unicast;
+     }
+     family inet6-vpn {
+         unicast;
+     }
[edit]
+  policy-options {                     
+      policy-statement EXPORT_OSPF_C1 {
+          term 1 {
+              from protocol bgp;
+              then accept;
+          }
+      }
+      policy-statement EXPORT_VRF_C1 {
+          term 1 {
+              then {
+                  community add target:123:1;
+                  community add domain-id:192.168.1.1:0;
+                  accept;
+              }
+          }
+          term final {
+              then reject;
+          }
+      }
+      policy-statement IMPORT_VRF_C1 {
+          term 1 {
+              from {
+                  protocol bgp;
+                  community target:123:1;
+              }
+              then accept;
+          }
+          term final {
+              then reject;
+          }
+      }
+      community domain-id:192.168.1.1:0 members domain-id:192.168.1.1:0;
+      community target:123:1 members target:123:1;
+  }
+  routing-instances {
+      C1 {
+          instance-type vrf;
+          interface ge-0/0/5.11;
+          route-distinguisher 10.210.1.6:1;
+          vrf-import IMPORT_VRF_C1;
+          vrf-export EXPORT_VRF_C1;
+          inactive: vrf-target target:123:1;
+          protocols {
+              ospf {
+                  domain-id 192.168.1.1;
+                  export EXPORT_OSPF_C1;
+                  area 0.0.0.0 {       
+                      interface ge-0/0/5.11;
+                  }
+              }
+          }
+      }
+  }
```

- **R7**:

```
[edit interfaces ge-0/0/3]
+   apply-groups-except interface-family;
[edit protocols]
+   bgp {
+       group ibgp {
+           type internal;
+           local-address 10.210.1.7;
+           family inet {
+               unicast;
+           }
+           family inet-vpn {
+               unicast;
+           }
+           family inet6-vpn {
+               unicast;
+           }
+           neighbor 10.210.1.8;
+       }
+   }
[edit]
+  policy-options {
+      policy-statement EXPORT_OSPF_CE_C1 {
+          term 1 {
+              from protocol bgp;       
+              then accept;
+          }
+      }
+  }
+  routing-instances {
+      C1 {
+          instance-type vrf;
+          interface ge-0/0/3.0;
+          route-distinguisher 10.210.1.7:1;
+          vrf-target target:345:1;
+          vrf-table-label;
+          protocols {
+              ospf {
+                  domain-id disable;
+                  domain-vpn-tag 0;
+                  export EXPORT_OSPF_CE_C1;
+                  area 0.0.0.0 {
+                      interface ge-0/0/3.0 {
+                          interface-type p2p;
+                      }
+                  }
+              }
+          }                            
+      }
+  }
```

- **R8**:

```
[edit interfaces]
+   ge-0/0/5 {
+       apply-groups-except interface-family;
+       flexible-vlan-tagging;
+       encapsulation flexible-ethernet-services;
+       unit 12 {
+           vlan-id 12;
+           family inet {
+               address 10.100.1.9/30;
+           }
+       }
+   }
[edit protocols bgp group ibgp]
+     family inet {
+         unicast;
+     }
+     family inet-vpn {
+         unicast;
+     }
+     family inet6-vpn {
+         unicast;
+     }
[edit]
+  policy-options {                     
+      policy-statement EXPORT_OSPF_C1 {
+          term 1 {
+              from protocol bgp;
+              then accept;
+          }
+      }
+  }
+  routing-instances {
+      C1 {
+          instance-type vrf;
+          interface ge-0/0/5.12;
+          route-distinguisher 10.210.1.8:1;
+          vrf-target target:345:1;
+          vrf-table-label;
+          protocols {
+              ospf {
+                  export EXPORT_OSPF_C1;
+                  area 0.0.0.0 {
+                      interface ge-0/0/5.12 {
+                          interface-type p2p;
+                      }
+                  }
+              }                        
+          }
+      }
+  }
```

- **RR**:

```
[edit]
- apply-groups nhs;
[edit routing-options]
+   rib inet.3 {
+       static {
+           route 0.0.0.0/0 discard;
+       }
+   }
+   rib inet6.3 {
+       static {
+           route ::/0 discard;
+       }
+   }
[edit protocols bgp group ibgp]
+     family inet {
+         unicast;
+     }
+     family inet-vpn {
+         unicast;
+     }
+     family inet6-vpn {
+         unicast;
+     }
+     cluster 10.210.1.10;
```

**Task 2:**

- **R4:**

```
[edit interfaces]
+   ge-0/0/5 {
+       apply-groups-except interface-family;
+       flexible-vlan-tagging;
+       encapsulation flexible-ethernet-services;
+       unit 22 {
+           vlan-id 22;
+           family inet {
+               address 10.100.2.5/30;
+           }
+       }
+   }
[edit interfaces lo0]
+    unit 2 {
+        family inet {
+            address 192.168.2.14/32;
+        }
+    }
[edit]
+  policy-options {
+      policy-statement EXPORT_OSPF_C2_S2 {
+          term 1 {
+              from protocol bgp;
+              then accept;             
+          }
+      }
+  }
+  routing-instances {
+      C2 {
+          instance-type vrf;
+          interface ge-0/0/5.22;
+          interface lo0.2;
+          route-distinguisher 10.210.1.4:2;
+          vrf-target target:123:2;
+          vrf-table-label;
+          routing-options {
+              router-id 192.168.2.14;
+          }
+          protocols {
+              ospf {
+                  inactive: export EXPORT_OSPF_C2_S2;
+                  sham-link local 192.168.2.14;
+                  area 0.0.0.0 {
+                      sham-link-remote 192.168.2.15;
+                      interface ge-0/0/5.22 {
+                          interface-type p2p;
+                      }                
+                      interface lo0.2 {
+                          passive;
+                      }
+                  }
+              }
+          }
+      }
+  }
```

- **R5:**

```
[edit interfaces]
+   ge-0/0/5 {
+       apply-groups-except interface-family;
+       flexible-vlan-tagging;
+       encapsulation flexible-ethernet-services;
+       unit 21 {
+           vlan-id 21;
+           family inet {
+               address 10.100.2.1/30;
+           }
+       }
+   }
[edit interfaces lo0]
+    unit 2 {
+        family inet {
+            address 192.168.2.15/32;
+        }
+    }
[edit]
+  policy-options {
+      policy-statement EXPORT_OSPF_C2_S1 {
+          term 1 {
+              from protocol bgp;
+              then accept;             
+          }
+      }
+  }
+  routing-instances {
+      C2 {
+          instance-type vrf;
+          interface ge-0/0/5.21;
+          interface lo0.2;
+          route-distinguisher 10.210.1.5:2;
+          vrf-target target:123:2;
+          vrf-table-label;
+          routing-options {
+              router-id 192.168.2.15;
+          }
+          protocols {
+              ospf {
+                  inactive: export EXPORT_OSPF_C2_S1;
+                  sham-link local 192.168.2.15;
+                  area 0.0.0.0 {
+                      sham-link-remote 192.168.2.14;
+                      interface ge-0/0/5.21 {
+                          interface-type p2p;
+                      }                
+                      interface lo0.2 {
+                          passive;
+                      }
+                  }
+              }
+          }
+      }
+  }
```

**Task 3:**

- **R3:**

```
[edit interfaces]
+   ge-0/0/5 {
+       apply-groups-except interface-family;
+       flexible-vlan-tagging;
+       encapsulation flexible-ethernet-services;
+       unit 100 {
+           vlan-id 100;
+           family inet {
+               address 10.10.11.3/24;
+           }
+           family mpls;
+       }
+   }
[edit protocols bgp]
     group ibgp { ... }
+    group ebgp_R11 {
+        type external;
+        import IMPORT_BGP_R11;
+        family inet-vpn {
+            unicast;
+        }
+        export EXPORT_BGP_R11;
+        vpn-apply-export;
+        neighbor 10.10.11.11 {         
+            peer-as 567;
+        }
+    }
[edit policy-options]
+   policy-statement EXPORT_BGP_R11 {
+       term ALLOW_C2 {
+           from community target:123:2;
+           then {
+               community add target:567:2222;
+               accept;
+           }
+       }
+       term FINAL {
+           then reject;
+       }
+   }
+   policy-statement IMPORT_BGP_R11 {
+       term CHANGE_COMM_C2 {
+           from community target:567:2222;
+           then {
+               community add target:123:2;
+               accept;
+           }                           
+       }
+       term FINAL {
+           then reject;
+       }
+   }
[edit policy-options]
+   community target:123:2 members target:123:2;
+   community target:567:2222 members target:567:2222;
```

- **R4:**

```
[edit routing-instances C2 protocols ospf]
-     inactive: export EXPORT_OSPF_C2_S2;
+     export EXPORT_OSPF_C2_S2;
```

- **R5:**

```
[edit routing-instances C2 protocols ospf]
-     inactive: export EXPORT_OSPF_C2_S1;
+     export EXPORT_OSPF_C2_S1;
```

**Task 4, 5, 6:**

- **R1:**

```
[edit interfaces]
+   ge-0/0/5 {
+       apply-groups-except interface-family;
+       flexible-vlan-tagging;
+       encapsulation flexible-ethernet-services;
+       unit 31 {
+           vlan-id 31;
+           family inet {
+               address 10.100.3.1/30;
+           }
+       }
+       unit 32 {
+           vlan-id 32;
+           family inet {
+               address 10.100.3.5/30;
+           }
+       }
+   }
[edit]
+  policy-options {
+      policy-statement EXPORT_VRF_C3_S1_HUB {
+          term 1 {
+              then {
+                  local-preference 600;
+                  community add C3_HUB;
+                  community add C3_ORIGIN_R1;
+                  accept;
+              }
+          }
+          term final {
+              then reject;
+          }
+      }
+      policy-statement GEN_DEFAULT {
+          term 1 {
+              from {
+                  protocol bgp;
+                  neighbor 10.100.3.2;
+              }
+              then accept;
+          }
+          term FINAL {
+              then reject;
+          }
+      }
+      policy-statement IMPORT_VRF_C3_S1_SPOKE {
+          term 1 {                     
+              from {
+                  protocol bgp;
+                  community C3_SPOKE;
+              }
+              then accept;
+          }
+          term final {
+              then reject;
+          }
+      }
+      policy-statement REJECT {
+          term final {
+              then reject;
+          }
+      }
+      community C3_HUB members target:123:31;
+      community C3_ORIGIN_R1 members origin:10.210.1.1:1;
+      community C3_SPOKE members target:123:32;
+  }
+  routing-instances {
+      C3-hub {
+          instance-type vrf;
+          interface ge-0/0/5.31;       
+          route-distinguisher 10.210.1.1:31;
+          vrf-import REJECT;
+          vrf-export EXPORT_VRF_C3_S1_HUB;
+          vrf-table-label;
+          routing-options {
+              generate {
+                  route 0.0.0.0/0 policy GEN_DEFAULT;
+              }
+          }
+          protocols {
+              bgp {
+                  group C3_S1 {
+                      type external;
+                      peer-as 45543;
+                      neighbor 10.100.3.2;
+                  }
+              }
+          }
+      }
+      C3-spoke {
+          instance-type vrf;
+          interface ge-0/0/5.32;
+          route-distinguisher 10.210.1.1:32;
+          vrf-import IMPORT_VRF_C3_S1_SPOKE;
+          vrf-export REJECT;
+          vrf-table-label;
+          protocols {
+              bgp {
+                  group C3_S1 {
+                      type external;
+                      peer-as 45543;
+                      as-override;
+                      neighbor 10.100.3.6;
+                  }
+              }
+          }
+      }
+  }
```

- **R2:**

```
[edit interfaces]
+   ge-0/0/5 {
+       apply-groups-except interface-family;
+       flexible-vlan-tagging;
+       encapsulation flexible-ethernet-services;
+       unit 33 {
+           vlan-id 33;
+           family inet {
+               address 10.100.3.9/30;
+           }
+       }
+       unit 34 {
+           vlan-id 34;
+           family inet {
+               address 10.100.3.13/30;
+           }
+       }
+   }
[edit]
+  policy-options {
+      policy-statement EXPORT_BGP_C3_S1_2 {
+          term 1 {
+              from protocol bgp;
+              then {                   
+                  as-path-prepend 123;
+                  accept;
+              }
+          }
+      }
+      policy-statement EXPORT_VRF_C3_S1_HUB {
+          term 1 {
+              then {
+                  community add C3_HUB;
+                  community add C3_ORIGIN_R2;
+                  accept;
+              }
+          }
+          term final {
+              then reject;
+          }
+      }
+      policy-statement GEN_DEFAULT {
+          term 1 {
+              from {
+                  protocol bgp;
+                  neighbor 10.100.3.10;
+              }                        
+              then accept;
+          }
+          term FINAL {
+              then reject;
+          }
+      }
+      policy-statement IMPORT_VRF_C3_S1_SPOKE {
+          term 1 {
+              from {
+                  protocol bgp;
+                  community C3_SPOKE;
+              }
+              then accept;
+          }
+          term final {
+              then reject;
+          }
+      }
+      policy-statement REJECT {
+          term final {
+              then reject;
+          }
+      }                                
+      community C3_HUB members target:123:31;
+      community C3_ORIGIN_R2 members origin:10.210.1.2:1;
+      community C3_SPOKE members target:123:32;
+  }
+  routing-instances {
+      C3-hub {
+          instance-type vrf;
+          interface ge-0/0/5.33;
+          route-distinguisher 10.210.1.2:31;
+          vrf-import REJECT;
+          vrf-export EXPORT_VRF_C3_S1_HUB;
+          vrf-table-label;
+          routing-options {
+              generate {
+                  route 0.0.0.0/0 policy GEN_DEFAULT;
+              }
+          }
+          protocols {
+              bgp {
+                  group C3_S1 {
+                      type external;
+                      peer-as 45543;
+                      neighbor 10.100.3.10;
+                  }
+              }
+          }
+      }
+      C3-spoke {
+          instance-type vrf;
+          interface ge-0/0/5.34;
+          route-distinguisher 10.210.1.2:32;
+          vrf-import IMPORT_VRF_C3_S1_SPOKE;
+          vrf-export REJECT;
+          vrf-table-label;
+          protocols {
+              bgp {
+                  group C3_S1 {
+                      type external;
+                      export EXPORT_BGP_C3_S1_2;
+                      peer-as 45543;
+                      as-override;
+                      neighbor 10.100.3.14;
+                  }
+              }
+          }
+      }                                
+  }
```

- **R4:**

```
[edit interfaces ge-0/0/5]
+    unit 37 {
+        vlan-id 37;
+        family inet {
+            address 10.100.3.25/30;
+        }
+    }
[edit policy-options]
+   policy-statement EXPORT_VRF_C3_SPOKE {
+       term 1 {
+           then {
+               community add C3_SPOKE;
+               community add C3_ORIGIN_R4;
+               accept;
+           }
+       }
+       term final {
+           then reject;
+       }
+   }
+   policy-statement IMPORT_VRF_C3_SPOKE {
+       term 1 {
+           from {
+               protocol bgp;           
+               community C3_HUB;
+           }
+           then accept;
+       }
+       term final {
+           then reject;
+       }
+   }
[edit policy-options]
+   community C3_HUB members target:123:31;
+   community C3_ORIGIN_R4 members origin:10.210.1.4:1;
+   community C3_SPOKE members target:123:32;
[edit routing-instances]
+   C3 {
+       instance-type vrf;
+       interface ge-0/0/5.37;
+       route-distinguisher 10.210.1.4:32;
+       vrf-import IMPORT_VRF_C3_SPOKE;
+       vrf-export EXPORT_VRF_C3_SPOKE;
+       vrf-table-label;
+       protocols {
+           bgp {
+               group C3_S2 {           
+                   type external;
+                   peer-as 45543;
+                   as-override;
+                   neighbor 10.100.3.26;
+               }
+           }
+       }
+   }
```

- **R5:**

```
[edit interfaces ge-0/0/5]
+    unit 36 {
+        vlan-id 36;
+        family inet {
+            address 10.100.3.21/30;
+        }
+    }
[edit policy-options]
+   policy-statement EXPORT_VRF_C3_SPOKE {
+       term 1 {
+           then {
+               community add C3_SPOKE;
+               community add C3_ORIGIN_R5;
+               accept;
+           }
+       }
+       term final {
+           then reject;
+       }
+   }
+   policy-statement IMPORT_VRF_C3_SPOKE {
+       term 1 {
+           from {
+               protocol bgp;           
+               community C3_HUB;
+           }
+           then accept;
+       }
+       term final {
+           then reject;
+       }
+   }
[edit policy-options]
+   community C3_HUB members target:123:31;
+   community C3_ORIGIN_R5 members origin:10.210.1.5:1;
+   community C3_ORIGIN_R6 members origin:10.210.1.6:1;
+   community C3_SPOKE members target:123:32;
[edit routing-instances]
+   C3 {
+       instance-type vrf;
+       interface ge-0/0/5.36;
+       route-distinguisher 10.210.1.5:32;
+       vrf-import IMPORT_VRF_C3_SPOKE;
+       vrf-export EXPORT_VRF_C3_SPOKE;
+       vrf-table-label;
+       protocols {
+           bgp {                       
+               group C3_S2_2 {
+                   type external;
+                   peer-as 45543;
+                   as-override;
+                   neighbor 10.100.3.22;
+               }
+           }
+       }
+   }
```

- **R6:**

```
[edit interfaces ge-0/0/5]
+    unit 35 {
+        vlan-id 35;
+        family inet {
+            address 10.100.3.17/30;
+        }
+    }
[edit policy-options]
+   policy-statement EXPORT_VRF_C3_SPOKE {
+       term 1 {
+           then {
+               community add C3_SPOKE;
+               community add C3_ORIGIN_R6;
+               accept;
+           }
+       }
+       term final {
+           then reject;
+       }
+   }
+   policy-statement IMPORT_VRF_C3_SPOKE {
+       term 1 {
+           from {
+               protocol bgp;           
+               community C3_HUB;
+           }
+           then accept;
+       }
+       term final {
+           then reject;
+       }
+   }
[edit policy-options]
+   community C3_HUB members target:123:31;
+   community C3_ORIGIN_R5 members origin:10.210.1.5:1;
+   community C3_ORIGIN_R6 members origin:10.210.1.6:1;
+   community C3_SPOKE members target:123:32;
[edit routing-instances]
+   C3 {
+       instance-type vrf;
+       interface ge-0/0/5.35;
+       route-distinguisher 10.210.1.6:32;
+       vrf-import IMPORT_VRF_C3_SPOKE;
+       vrf-export EXPORT_VRF_C3_SPOKE;
+       vrf-table-label;
+       protocols {
+           bgp {                       
+               group C3_S2_1 {
+                   type external;
+                   peer-as 45543;
+                   as-override;
+                   neighbor 10.100.3.18;
+               }
+           }
+       }
+   }
```

- **RR**:

```
[edit protocols bgp group ibgp family inet-vpn unicast]
+        loops 2;
```

**Task 7:**

- **R1**:

```
[edit policy-options]
+   policy-statement EXPORT_VRF_C3_S1_SPOKE {
+       term 1 {
+           from protocol direct;
+           then {
+               community add C3_ORIGIN_R1;
+               community add C3_HUB;
+               accept;
+           }
+       }
+       term final {
+           then reject;
+       }
+   }
+   policy-statement IMPORT_BGP_C3 {
+       term 1 {
+           from {
+               route-filter 10.100.3.0/24 orlonger;
+               route-filter 192.168.3.12/32 exact;
+               route-filter 192.168.3.11/32 exact;
+           }
+           then accept;                
+       }
+       term final {
+           then reject;
+       }
+   }
[edit routing-instances C3-hub protocols bgp group C3_S1]
+      keep all;
+      import IMPORT_BGP_C3;
+      family inet {
+          unicast {
+              loops 2;
+          }
+      }
[edit routing-instances C3-spoke]
-   vrf-export REJECT;
+   vrf-export EXPORT_VRF_C3_S1_SPOKE;
```

- **R2**:

```
[edit policy-options]
+   policy-statement EXPORT_VRF_C3_S1_SPOKE {
+       term 1 {
+           from protocol direct;
+           then {
+               community add C3_ORIGIN_R2;
+               community add C3_HUB;
+               accept;
+           }
+       }
+       term final {
+           then reject;
+       }
+   }
[edit routing-instances C3-spoke]
-   vrf-export REJECT;
+   vrf-export EXPORT_VRF_C3_S1_SPOKE;
```

- **R4**:

```
[edit protocols bgp group ibgp family inet-vpn unicast]
+        loops 2;
```

- **R5**:

```
[edit protocols bgp group ibgp family inet-vpn unicast]
+        loops 2;
[edit policy-options policy-statement IMPORT_VRF_C3_SPOKE]
+    term 0 {
+        from {
+            protocol bgp;
+            community C3_ORIGIN_R6;
+        }
+        then reject;
+    }
     term 1 { ... }
```

- **R6**:

```
[edit protocols bgp group ibgp family inet-vpn unicast]
+        loops 2;
[edit policy-options policy-statement IMPORT_VRF_C3_SPOKE]
+    term 0 {
+        from {
+            protocol bgp;
+            community C3_ORIGIN_R5;
+        }
+        then reject;
+    }
     term 1 { ... }
```

**Task 8:**

- **R1**:

```
[edit protocols bgp group ibgp]
+      family route-target;
```

- **R2**:

```
[edit protocols bgp group ibgp]
+      family route-target;
```

- **R3**:

```
[edit routing-options]
+   rib bgp.rtarget.0 {
+       static {
+           route-target-filter 123:2/64 local;
+       }
+   }
[edit protocols bgp group ibgp]
+      family route-target {
+          external-paths 1;
+      }
```

- **R4**:

```
[edit protocols bgp group ibgp]
+      family route-target;
```

- **R5**:

```
[edit routing-options]
+   resolution {
+       rib bgp.rtarget.0 {
+           resolution-ribs inet.0;
+       }
+   }
[edit protocols bgp group ibgp]
+      family route-target;
[edit protocols ldp]
+   egress-policy EGRESS_POLICY_LDP;
[edit policy-options]
+   policy-statement EGRESS_POLICY_LDP {
+       term 1 {
+           from {
+               route-filter 10.210.1.5/32 exact;
+               route-filter 10.210.1.10/32 exact;
+           }
+           then accept;
+       }
+   }
```

- **R6**:

```
[edit protocols bgp group ibgp]
+      family route-target;
```

- **RR**:

```
[edit protocols bgp group ibgp]
+      family route-target {
+          advertise-default;
+      } 
```

**Task 9:**

- done in Task 1

**Task 10:**

- **R6**:

```
[edit policy-options policy-statement EXPORT_VRF_C3_SPOKE term 1 then]
       community add C3_ORIGIN_R6 { ... }
+      community add C3_R6;
[edit policy-options policy-statement IMPORT_VRF_C1]
     term 1 { ... }
+    term 2 {
+        from {
+            interface ge-0/0/5.35;
+            community C3_R6;
+        }
+        then accept;
+    }
     term final { ... }
[edit policy-options policy-statement IMPORT_VRF_C3_SPOKE]
     term 1 { ... }
+    term 2 {
+        from {                         
+            interface ge-0/0/5.11;
+            community target:123:1;
+        }
+        then accept;
+    }
     term final { ... }
[edit policy-options]
+   community C3_R6 members target:123:36;
[edit routing-instances C1]
+    routing-options {
+        auto-export;
+    }
[edit routing-instances C3]
+    routing-options {
+        auto-export;
+    }
```

---

**FULL CONFIGURATION**

---

- **R1**:

```
groups {
    interface-family {
        interfaces {
            <ge-0/0/*> {
                unit 0 {
                    family iso;
                    family mpls;
                }
            }
        }
    }
}
apply-groups interface-family;
system {
    host-name R1;
    time-zone Asia/Saigon;
    root-authentication {
        encrypted-password "$6$KQfP9GYY$0meQNT1L3.bxlLOtvOL4bejHPFfWVQDAU9RhJcE2pROP.hmzTHKRVO1cgFwqs6miracC.XOlH4oJPSwqwCYlH0"; ## SECRET-DATA
    }
    login {
        user lab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$/WgLGrDM$0tn6F8h6QGG0CC8KbIpAeV6v35maKmNouxNYaK1vIS6PhO9dYrV0vDnG4gqFty1UDfbRSR1z3KGGIx8l6wt4r."; ## SECRET-DATA
            }
        }
        user labsvtech {
            uid 2001;
            class super-user;
            authentication {
                encrypted-password "$6$SL/eyx1r$Y9lehX2oBKHEEH55H2FDBYXlKo4QKd/TJakrbqUqDJCW0Vbp0Q05GWlk0HOVZmwICbISkhM53uf1RzCLAdIDV0"; ## SECRET-DATA
            }
        }
    }
    services {
        ssh;
        telnet;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    ge-0/0/1 {
        description to-r2;
        unit 0 {
            family inet {
                address 10.10.1.1/24;
            }
        }
    }
    ge-0/0/2 {
        description to-r6;
        unit 0 {
            family inet {
                address 10.10.6.1/24;
            }
        }
    }
    ge-0/0/3 {
        description to-r4;
        unit 0 {
            family inet {
                address 10.10.7.1/24;
            }
        }
    }
    ge-0/0/5 {
        apply-groups-except interface-family;
        flexible-vlan-tagging;
        encapsulation flexible-ethernet-services;
        unit 31 {
            vlan-id 31;
            family inet {
                address 10.100.3.1/30;
            }
        }
        unit 32 {
            vlan-id 32;
            family inet {
                address 10.100.3.5/30;
            }
        }
    }
    em0 {
        unit 0 {
            family inet {
                address 10.200.1.1/24;
            }
        }
    }
    lo0 {
        unit 0 {
            family inet {
                address 10.210.1.1/32;
            }
            family iso {
                address 49.1111.0102.1000.1001.00;
            }
        }
    }
}
routing-options {
    autonomous-system 123;
}
protocols {
    rsvp {
        interface ge-0/0/1.0;
        interface ge-0/0/3.0;
    }
    mpls {
        label-switched-path to-r2 {
            to 10.210.1.2;
            ldp-tunneling;
        }
        label-switched-path to-r4 {
            to 10.210.1.4;
            ldp-tunneling;
        }
        interface ge-0/0/2.0;
        interface ge-0/0/3.0;
        interface ge-0/0/1.0;
    }
    bgp {
        group ibgp {
            type internal;
            local-address 10.210.1.1;
            family inet {
                unicast;
            }
            family inet-vpn {
                unicast;
            }
            family inet6-vpn {
                unicast;
            }
            family route-target;
            neighbor 10.210.1.10;
        }
    }
    isis {
        level 1 disable;
        interface ge-0/0/1.0 {
            point-to-point;
        }
        interface ge-0/0/2.0 {
            point-to-point;
        }
        interface ge-0/0/3.0 {
            point-to-point;
        }
        interface lo0.0;
    }
    ldp {
        interface ge-0/0/2.0;
        interface lo0.0;
    }
}
policy-options {
    policy-statement EXPORT_VRF_C3_S1_HUB {
        term 1 {
            then {
                local-preference 600;
                community add C3_HUB;
                community add C3_ORIGIN_R1;
                accept;
            }
        }
        term final {
            then reject;
        }
    }
    policy-statement EXPORT_VRF_C3_S1_SPOKE {
        term 1 {
            from protocol direct;
            then {
                community add C3_ORIGIN_R1;
                community add C3_HUB;
                accept;
            }
        }
        term final {
            then reject;
        }
    }
    policy-statement GEN_DEFAULT {
        term 1 {
            from {
                protocol bgp;
                neighbor 10.100.3.2;
            }
            then accept;
        }
        term FINAL {
            then reject;
        }
    }
    policy-statement IMPORT_BGP_C3 {
        term 1 {
            from {
                route-filter 10.100.3.0/24 orlonger;
                route-filter 192.168.3.12/32 exact;
                route-filter 192.168.3.11/32 exact;
            }
            then accept;
        }
        term final {
            then reject;
        }
    }
    policy-statement IMPORT_VRF_C3_S1_SPOKE {
        term 1 {
            from {
                protocol bgp;
                community C3_SPOKE;
            }
            then accept;
        }
        term final {
            then reject;
        }
    }
    policy-statement REJECT {
        term final {
            then reject;
        }
    }
    community C3_HUB members target:123:31;
    community C3_ORIGIN_R1 members origin:10.210.1.1:1;
    community C3_SPOKE members target:123:32;
}
routing-instances {
    C3-hub {
        instance-type vrf;
        interface ge-0/0/5.31;
        route-distinguisher 10.210.1.1:31;
        vrf-import REJECT;
        vrf-export EXPORT_VRF_C3_S1_HUB;
        vrf-table-label;
        routing-options {
            generate {
                route 0.0.0.0/0 policy GEN_DEFAULT;
            }
        }
        protocols {
            bgp {
                group C3_S1 {
                    type external;
                    keep all;
                    import IMPORT_BGP_C3;
                    family inet {
                        unicast {
                            loops 2;
                        }
                    }
                    peer-as 45543;
                    neighbor 10.100.3.2;
                }
            }
        }
    }
    C3-spoke {
        instance-type vrf;
        interface ge-0/0/5.32;
        route-distinguisher 10.210.1.1:32;
        vrf-import IMPORT_VRF_C3_S1_SPOKE;
        vrf-export EXPORT_VRF_C3_S1_SPOKE;
        vrf-table-label;
        protocols {
            bgp {
                group C3_S1 {
                    type external;
                    peer-as 45543;
                    as-override;
                    neighbor 10.100.3.6;
                }
            }
        }
    }
}
```

- **R2**:

```
groups {
    interface-family {
        interfaces {
            <ge-0/0/*> {
                unit 0 {
                    family iso;
                    family mpls;
                }
            }
        }
    }
}
apply-groups interface-family;
system {
    host-name R2;
    time-zone Asia/Saigon;
    root-authentication {
        encrypted-password "$6$KQfP9GYY$0meQNT1L3.bxlLOtvOL4bejHPFfWVQDAU9RhJcE2pROP.hmzTHKRVO1cgFwqs6miracC.XOlH4oJPSwqwCYlH0"; ## SECRET-DATA
    }
    login {
        user lab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$/WgLGrDM$0tn6F8h6QGG0CC8KbIpAeV6v35maKmNouxNYaK1vIS6PhO9dYrV0vDnG4gqFty1UDfbRSR1z3KGGIx8l6wt4r."; ## SECRET-DATA
            }
        }
        user labsvtech {
            uid 2001;
            class super-user;
            authentication {
                encrypted-password "$6$SL/eyx1r$Y9lehX2oBKHEEH55H2FDBYXlKo4QKd/TJakrbqUqDJCW0Vbp0Q05GWlk0HOVZmwICbISkhM53uf1RzCLAdIDV0"; ## SECRET-DATA
            }
        }
    }
    services {
        ssh;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    ge-0/0/1 {
        unit 0 {
            family inet {
                address 10.10.1.2/24;
            }
        }
    }
    ge-0/0/2 {
        unit 0 {
            family inet {
                address 10.10.2.2/24;
            }
        }
    }
    ge-0/0/4 {
        unit 0 {
            family inet {
                address 10.10.8.2/24;
            }
        }
    }
    ge-0/0/5 {
        apply-groups-except interface-family;
        flexible-vlan-tagging;
        encapsulation flexible-ethernet-services;
        unit 33 {
            vlan-id 33;
            family inet {
                address 10.100.3.9/30;
            }
        }
        unit 34 {
            vlan-id 34;
            family inet {
                address 10.100.3.13/30;
            }
        }
    }
    em0 {
        unit 0 {
            family inet {
                address 10.200.1.2/24;
            }
        }
    }
    lo0 {
        unit 0 {
            family inet {
                address 10.210.1.2/32;
            }
            family iso {
                address 49.1111.0102.1000.1002.00;
            }
        }
    }
}
routing-options {
    autonomous-system 123;
}
protocols {
    rsvp {
        interface ge-0/0/4.0;
        interface ge-0/0/1.0;
    }
    mpls {
        label-switched-path to-r5 {
            to 10.210.1.5;
            ldp-tunneling;
        }
        label-switched-path to-r1 {
            to 10.210.1.1;
            ldp-tunneling;
        }
        interface ge-0/0/1.0;
        interface ge-0/0/2.0;
        interface ge-0/0/4.0;
    }
    bgp {
        group ibgp {
            type internal;
            local-address 10.210.1.2;
            family inet {
                unicast;
            }
            family inet-vpn {
                unicast;
            }
            family inet6-vpn {
                unicast;
            }
            family route-target;
            neighbor 10.210.1.10;
        }
    }
    isis {
        level 1 disable;
        interface ge-0/0/1.0 {
            point-to-point;
        }
        interface ge-0/0/2.0 {
            point-to-point;
        }
        interface ge-0/0/4.0 {
            point-to-point;
        }
        interface lo0.0;
    }
    ldp {
        interface ge-0/0/2.0;
        interface lo0.0;
    }
}
policy-options {
    policy-statement EXPORT_BGP_C3_S1_2 {
        term 1 {
            from protocol bgp;
            then {
                as-path-prepend 123;
                accept;
            }
        }
    }
    policy-statement EXPORT_VRF_C3_S1_HUB {
        term 1 {
            then {
                community add C3_HUB;
                community add C3_ORIGIN_R2;
                accept;
            }
        }
        term final {
            then reject;
        }
    }
    policy-statement EXPORT_VRF_C3_S1_SPOKE {
        term 1 {
            from protocol direct;
            then {
                community add C3_ORIGIN_R2;
                community add C3_HUB;
                accept;
            }
        }
        term final {
            then reject;
        }
    }
    policy-statement GEN_DEFAULT {
        term 1 {
            from {
                protocol bgp;
                neighbor 10.100.3.10;
            }
            then accept;
        }
        term FINAL {
            then reject;
        }
    }
    policy-statement IMPORT_VRF_C3_S1_SPOKE {
        term 1 {
            from {
                protocol bgp;
                community C3_SPOKE;
            }
            then accept;
        }
        term final {
            then reject;
        }
    }
    policy-statement REJECT {
        term final {
            then reject;
        }
    }
    community C3_HUB members target:123:31;
    community C3_ORIGIN_R2 members origin:10.210.1.2:1;
    community C3_SPOKE members target:123:32;
}
routing-instances {
    C3-hub {
        instance-type vrf;
        interface ge-0/0/5.33;
        route-distinguisher 10.210.1.2:31;
        vrf-import REJECT;
        vrf-export EXPORT_VRF_C3_S1_HUB;
        vrf-table-label;
        routing-options {
            generate {
                route 0.0.0.0/0 policy GEN_DEFAULT;
            }
        }
        protocols {
            bgp {
                group C3_S1 {
                    type external;
                    peer-as 45543;
                    neighbor 10.100.3.10;
                }
            }
        }
    }
    C3-spoke {
        instance-type vrf;
        interface ge-0/0/5.34;
        route-distinguisher 10.210.1.2:32;
        vrf-import IMPORT_VRF_C3_S1_SPOKE;
        vrf-export EXPORT_VRF_C3_S1_SPOKE;
        vrf-table-label;
        protocols {
            bgp {
                group C3_S1 {
                    type external;
                    export EXPORT_BGP_C3_S1_2;
                    peer-as 45543;
                    as-override;
                    neighbor 10.100.3.14;
                }
            }
        }
    }
}
```

- **R3**:

```
groups {
    interface-family {
        interfaces {
            <ge-0/0/*> {
                unit 0 {
                    family iso;
                    family mpls;
                }
            }
        }
    }
}
apply-groups interface-family;
system {
    host-name R3;
    time-zone Asia/Saigon;
    root-authentication {
        encrypted-password "$6$KQfP9GYY$0meQNT1L3.bxlLOtvOL4bejHPFfWVQDAU9RhJcE2pROP.hmzTHKRVO1cgFwqs6miracC.XOlH4oJPSwqwCYlH0"; ## SECRET-DATA
    }
    login {
        user lab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$/WgLGrDM$0tn6F8h6QGG0CC8KbIpAeV6v35maKmNouxNYaK1vIS6PhO9dYrV0vDnG4gqFty1UDfbRSR1z3KGGIx8l6wt4r."; ## SECRET-DATA
            }
        }
        user labsvtech {
            uid 2001;
            class super-user;
            authentication {
                encrypted-password "$6$SL/eyx1r$Y9lehX2oBKHEEH55H2FDBYXlKo4QKd/TJakrbqUqDJCW0Vbp0Q05GWlk0HOVZmwICbISkhM53uf1RzCLAdIDV0"; ## SECRET-DATA
            }
        }
    }
    services {
        ssh;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    ge-0/0/1 {
        unit 0 {
            family inet {
                address 10.10.3.3/24;
            }
        }
    }
    ge-0/0/2 {
        unit 0 {
            family inet {
                address 10.10.2.3/24;
            }
        }
    }
    ge-0/0/3 {
        apply-groups-except interface-family;
        unit 0 {
            family inet {
                address 10.100.1.5/30;
            }
        }
    }
    ge-0/0/5 {
        apply-groups-except interface-family;
        flexible-vlan-tagging;
        encapsulation flexible-ethernet-services;
        unit 100 {
            vlan-id 100;
            family inet {
                address 10.10.11.3/24;
            }
            family mpls;
        }
    }
    em0 {
        unit 0 {
            family inet {
                address 10.200.1.3/24;
            }
        }
    }
    lo0 {
        unit 0 {
            family inet {
                address 10.210.1.3/32;
            }
            family iso {
                address 49.1111.0102.1000.1003.00;
            }
        }
    }
}
routing-options {
    rib bgp.rtarget.0 {
        static {
            route-target-filter 123:2/64 local;
        }
    }
    autonomous-system 123;
}
protocols {
    rsvp {
        disable;
    }
    mpls {
        interface ge-0/0/2.0;
        interface ge-0/0/1.0;
    }
    bgp {
        group ibgp {
            type internal;
            local-address 10.210.1.3;
            family inet {
                unicast;
            }
            family inet-vpn {
                unicast;
            }
            family inet6-vpn {
                unicast;
            }
            family route-target {
                external-paths 1;
            }
            neighbor 10.210.1.10;
        }
        group ebgp_R11 {
            type external;
            import IMPORT_BGP_R11;
            family inet-vpn {
                unicast;
            }
            export EXPORT_BGP_R11;
            vpn-apply-export;
            neighbor 10.10.11.11 {
                peer-as 567;
            }
        }
    }
    isis {
        level 1 disable;
        interface ge-0/0/1.0 {
            point-to-point;
        }
        interface ge-0/0/2.0 {
            point-to-point;
        }
        interface lo0.0;
    }
    ldp {
        interface ge-0/0/1.0;
        interface ge-0/0/2.0;
        interface lo0.0;
    }
}
policy-options {
    policy-statement EXPORT_BGP_R11 {
        term ALLOW_C2 {
            from community target:123:2;
            then {
                community add target:567:2222;
                accept;
            }
        }
        term FINAL {
            then reject;
        }
    }
    policy-statement EXPORT_OSPF_CE_C1 {
        term 1 {
            from protocol bgp;
            then accept;
        }
    }
    policy-statement EXPORT_VRF_C1 {
        term 1 {
            then {
                community add target:123:1;
                accept;
            }
        }
        term final {
            then reject;
        }
    }
    policy-statement IMPORT_BGP_R11 {
        term CHANGE_COMM_C2 {
            from community target:567:2222;
            then {
                community add target:123:2;
                accept;
            }
        }
        term FINAL {
            then reject;
        }
    }
    policy-statement IMPORT_VRF_C1 {
        term 1 {
            from {
                protocol bgp;
                community target:123:1;
            }
            then accept;
        }
        term final {
            then reject;
        }
    }
    community target:123:1 members target:123:1;
    community target:123:2 members target:123:2;
    community target:567:2222 members target:567:2222;
}
routing-instances {
    C1 {
        instance-type vrf;
        interface ge-0/0/3.0;
        route-distinguisher 10.210.1.3:1;
        vrf-import IMPORT_VRF_C1;
        vrf-export EXPORT_VRF_C1;
        inactive: vrf-target target:123:1;
        vrf-table-label;
        protocols {
            ospf {
                inactive: domain-id disable;
                domain-vpn-tag 0;
                export EXPORT_OSPF_CE_C1;
                area 0.0.0.0 {
                    interface ge-0/0/3.0 {
                        interface-type p2p;
                    }
                }
            }
        }
    }
}

```

- **R4**:

```
groups {
    interface-family {
        interfaces {
            <ge-0/0/*> {
                unit 0 {
                    family iso;
                    family mpls;
                }
            }
        }
    }
}
apply-groups interface-family;
system {
    host-name R4;
    time-zone Asia/Saigon;
    root-authentication {
        encrypted-password "$6$KQfP9GYY$0meQNT1L3.bxlLOtvOL4bejHPFfWVQDAU9RhJcE2pROP.hmzTHKRVO1cgFwqs6miracC.XOlH4oJPSwqwCYlH0"; ## SECRET-DATA
    }
    login {
        user lab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$/WgLGrDM$0tn6F8h6QGG0CC8KbIpAeV6v35maKmNouxNYaK1vIS6PhO9dYrV0vDnG4gqFty1UDfbRSR1z3KGGIx8l6wt4r."; ## SECRET-DATA
            }
        }
        user labsvtech {
            uid 2001;
            class super-user;
            authentication {
                encrypted-password "$6$SL/eyx1r$Y9lehX2oBKHEEH55H2FDBYXlKo4QKd/TJakrbqUqDJCW0Vbp0Q05GWlk0HOVZmwICbISkhM53uf1RzCLAdIDV0"; ## SECRET-DATA
            }
        }
    }
    services {
        ssh;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    ge-0/0/1 {
        unit 0 {
            family inet {
                address 10.10.3.4/24;
            }
        }
    }
    ge-0/0/2 {
        unit 0 {
            family inet {
                address 10.10.4.4/24;
            }
        }
    }
    ge-0/0/3 {
        unit 0 {
            family inet {
                address 10.10.7.4/24;
            }
        }
    }
    ge-0/0/5 {
        apply-groups-except interface-family;
        flexible-vlan-tagging;
        encapsulation flexible-ethernet-services;
        unit 22 {
            vlan-id 22;
            family inet {
                address 10.100.2.5/30;
            }
        }
        unit 37 {
            vlan-id 37;
            family inet {
                address 10.100.3.25/30;
            }
        }
    }
    em0 {
        unit 0 {
            family inet {
                address 10.200.1.4/24;
            }
        }
    }
    lo0 {
        unit 0 {
            family inet {
                address 10.210.1.4/32;
            }
            family iso {
                address 49.1111.0102.1000.1004.00;
            }
        }
        unit 2 {
            family inet {
                address 192.168.2.14/32;
            }
        }
    }
}
routing-options {
    autonomous-system 123;
}
protocols {
    rsvp {
        interface ge-0/0/2.0;
        interface ge-0/0/3.0;
    }
    mpls {
        label-switched-path to-r1 {
            to 10.210.1.1;
            ldp-tunneling;
        }
        label-switched-path to-r5 {
            to 10.210.1.5;
            ldp-tunneling;
        }
        interface ge-0/0/1.0;
        interface ge-0/0/2.0;
        interface ge-0/0/3.0;
    }
    bgp {
        group ibgp {
            type internal;
            local-address 10.210.1.4;
            family inet {
                unicast;
            }
            family inet-vpn {
                unicast {
                    loops 2;
                }
            }
            family inet6-vpn {
                unicast;
            }
            family route-target;
            neighbor 10.210.1.10;
        }
    }
    isis {
        level 1 disable;
        interface ge-0/0/1.0 {
            point-to-point;
        }
        interface ge-0/0/2.0 {
            point-to-point;
        }
        interface ge-0/0/3.0 {
            point-to-point;
        }
        interface lo0.0;
    }
    ldp {
        interface ge-0/0/1.0;
        interface lo0.0;
    }
}
policy-options {
    policy-statement EXPORT_OSPF_C2_S2 {
        term 1 {
            from protocol bgp;
            then accept;
        }
    }
    policy-statement EXPORT_VRF_C3_SPOKE {
        term 1 {
            then {
                community add C3_SPOKE;
                community add C3_ORIGIN_R4;
                accept;
            }
        }
        term final {
            then reject;
        }
    }
    policy-statement IMPORT_VRF_C3_SPOKE {
        term 1 {
            from {
                protocol bgp;
                community C3_HUB;
            }
            then accept;
        }
        term final {
            then reject;
        }
    }
    community C3_HUB members target:123:31;
    community C3_ORIGIN_R4 members origin:10.210.1.4:1;
    community C3_SPOKE members target:123:32;
}
routing-instances {
    C2 {
        instance-type vrf;
        interface ge-0/0/5.22;
        interface lo0.2;
        route-distinguisher 10.210.1.4:2;
        vrf-target target:123:2;
        vrf-table-label;
        routing-options {
            router-id 192.168.2.14;
        }
        protocols {
            ospf {
                export EXPORT_OSPF_C2_S2;
                sham-link local 192.168.2.14;
                area 0.0.0.0 {
                    sham-link-remote 192.168.2.15;
                    interface ge-0/0/5.22 {
                        interface-type p2p;
                    }
                    interface lo0.2 {
                        passive;
                    }
                }
            }
        }
    }
    C3 {
        instance-type vrf;
        interface ge-0/0/5.37;
        route-distinguisher 10.210.1.4:32;
        vrf-import IMPORT_VRF_C3_SPOKE;
        vrf-export EXPORT_VRF_C3_SPOKE;
        vrf-table-label;
        protocols {
            bgp {
                group C3_S2 {
                    type external;
                    peer-as 45543;
                    as-override;
                    neighbor 10.100.3.26;
                }
            }
        }
    }
}
```

- **R5**:

```
groups {
    interface-family {
        interfaces {
            <ge-0/0/*> {
                unit 0 {
                    family iso;
                    family mpls;
                }
            }
        }
    }
}
apply-groups interface-family;
system {
    host-name R5;
    time-zone Asia/Saigon;
    root-authentication {
        encrypted-password "$6$KQfP9GYY$0meQNT1L3.bxlLOtvOL4bejHPFfWVQDAU9RhJcE2pROP.hmzTHKRVO1cgFwqs6miracC.XOlH4oJPSwqwCYlH0"; ## SECRET-DATA
    }
    login {
        user lab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$/WgLGrDM$0tn6F8h6QGG0CC8KbIpAeV6v35maKmNouxNYaK1vIS6PhO9dYrV0vDnG4gqFty1UDfbRSR1z3KGGIx8l6wt4r."; ## SECRET-DATA
            }
        }
        user labsvtech {
            uid 2001;
            class super-user;
            authentication {
                encrypted-password "$6$SL/eyx1r$Y9lehX2oBKHEEH55H2FDBYXlKo4QKd/TJakrbqUqDJCW0Vbp0Q05GWlk0HOVZmwICbISkhM53uf1RzCLAdIDV0"; ## SECRET-DATA
            }
        }
    }
    services {
        ssh;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    ge-0/0/1 {
        description to-rr;
        unit 0 {
            family inet {
                address 10.10.10.5/24;
            }
        }
    }
    ge-0/0/2 {
        unit 0 {
            family inet {
                address 10.10.4.5/24;
            }
        }
    }
    ge-0/0/3 {
        unit 0 {
            family inet {
                address 10.10.5.5/24;
            }
        }
    }
    ge-0/0/4 {
        unit 0 {
            family inet {
                address 10.10.8.5/24;
            }
        }
    }
    ge-0/0/5 {
        apply-groups-except interface-family;
        flexible-vlan-tagging;
        encapsulation flexible-ethernet-services;
        unit 21 {
            vlan-id 21;
            family inet {
                address 10.100.2.1/30;
            }
        }
        unit 36 {
            vlan-id 36;
            family inet {
                address 10.100.3.21/30;
            }
        }
    }
    em0 {
        unit 0 {
            family inet {
                address 10.200.1.5/24;
            }
        }
    }
    lo0 {
        unit 0 {
            family inet {
                address 10.210.1.5/32;
            }
            family iso {
                address 49.1111.0102.1000.1005.00;
            }
        }
        unit 2 {
            family inet {
                address 192.168.2.15/32;
            }
        }
    }
}
routing-options {
    autonomous-system 123;
    resolution {
        rib bgp.rtarget.0 {
            resolution-ribs inet.0;
        }
    }
}
protocols {
    rsvp {
        interface ge-0/0/2.0;
        interface ge-0/0/4.0;
    }
    mpls {
        label-switched-path to-r4 {
            to 10.210.1.4;
            ldp-tunneling;
        }
        label-switched-path to-r2 {
            to 10.210.1.2;
            ldp-tunneling;
        }
        interface ge-0/0/2.0;
        interface ge-0/0/3.0;
        interface ge-0/0/4.0;
    }
    bgp {
        group ibgp {
            type internal;
            local-address 10.210.1.5;
            family inet {
                unicast;
            }
            family inet-vpn {
                unicast {
                    loops 2;
                }
            }
            family inet6-vpn {
                unicast;
            }
            family route-target;
            neighbor 10.210.1.10;
        }
    }
    isis {
        level 1 disable;
        interface ge-0/0/1.0 {
            point-to-point;
        }
        interface ge-0/0/2.0 {
            point-to-point;
        }
        interface ge-0/0/3.0 {
            point-to-point;
        }
        interface ge-0/0/4.0 {
            point-to-point;
        }
        interface lo0.0;
    }
    ldp {
        egress-policy EGRESS_POLICY_LDP;
        interface ge-0/0/3.0;
        interface lo0.0;
    }
}
policy-options {
    policy-statement EGRESS_POLICY_LDP {
        term 1 {
            from {
                route-filter 10.210.1.5/32 exact;
                route-filter 10.210.1.10/32 exact;
            }
            then accept;
        }
    }
    policy-statement EXPORT_OSPF_C2_S1 {
        term 1 {
            from protocol bgp;
            then accept;
        }
    }
    policy-statement EXPORT_VRF_C3_SPOKE {
        term 1 {
            then {
                community add C3_SPOKE;
                community add C3_ORIGIN_R5;
                accept;
            }
        }
        term final {
            then reject;
        }
    }
    policy-statement IMPORT_VRF_C3_SPOKE {
        term 0 {
            from {
                protocol bgp;
                community C3_ORIGIN_R6;
            }
            then reject;
        }
        term 1 {
            from {
                protocol bgp;
                community C3_HUB;
            }
            then accept;
        }
        term final {
            then reject;
        }
    }
    community C3_HUB members target:123:31;
    community C3_ORIGIN_R5 members origin:10.210.1.5:1;
    community C3_ORIGIN_R6 members origin:10.210.1.6:1;
    community C3_SPOKE members target:123:32;
}
routing-instances {
    C2 {
        instance-type vrf;
        interface ge-0/0/5.21;
        interface lo0.2;
        route-distinguisher 10.210.1.5:2;
        vrf-target target:123:2;
        vrf-table-label;
        routing-options {
            router-id 192.168.2.15;
        }
        protocols {
            ospf {
                export EXPORT_OSPF_C2_S1;
                sham-link local 192.168.2.15;
                area 0.0.0.0 {
                    sham-link-remote 192.168.2.14;
                    interface ge-0/0/5.21 {
                        interface-type p2p;
                    }
                    interface lo0.2 {
                        passive;
                    }
                }
            }
        }
    }
    C3 {
        instance-type vrf;
        interface ge-0/0/5.36;
        route-distinguisher 10.210.1.5:32;
        vrf-import IMPORT_VRF_C3_SPOKE;
        vrf-export EXPORT_VRF_C3_SPOKE;
        vrf-table-label;
        protocols {
            bgp {
                group C3_S2_2 {
                    type external;
                    peer-as 45543;
                    as-override;
                    neighbor 10.100.3.22;
                }
            }
        }
    }
}
```

- **R6**:

```
groups {
    interface-family {
        interfaces {
            <ge-0/0/*> {
                unit 0 {
                    family iso;
                    family mpls;
                }
            }
        }
    }
}
apply-groups interface-family;
system {
    host-name R6;
    time-zone Asia/Saigon;
    root-authentication {
        encrypted-password "$6$KQfP9GYY$0meQNT1L3.bxlLOtvOL4bejHPFfWVQDAU9RhJcE2pROP.hmzTHKRVO1cgFwqs6miracC.XOlH4oJPSwqwCYlH0"; ## SECRET-DATA
    }
    login {
        user lab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$/WgLGrDM$0tn6F8h6QGG0CC8KbIpAeV6v35maKmNouxNYaK1vIS6PhO9dYrV0vDnG4gqFty1UDfbRSR1z3KGGIx8l6wt4r."; ## SECRET-DATA
            }
        }
        user labsvtech {
            uid 2001;
            class super-user;
            authentication {
                encrypted-password "$6$SL/eyx1r$Y9lehX2oBKHEEH55H2FDBYXlKo4QKd/TJakrbqUqDJCW0Vbp0Q05GWlk0HOVZmwICbISkhM53uf1RzCLAdIDV0"; ## SECRET-DATA
            }
        }
    }
    services {
        ssh;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    ge-0/0/2 {
        unit 0 {
            family inet {
                address 10.10.6.6/24;
            }
        }
    }
    ge-0/0/3 {
        unit 0 {
            family inet {
                address 10.10.5.6/24;
            }
        }
    }
    ge-0/0/5 {
        apply-groups-except interface-family;
        flexible-vlan-tagging;
        encapsulation flexible-ethernet-services;
        unit 11 {
            vlan-id 11;
            family inet {
                address 10.100.1.1/30;
            }
        }
        unit 35 {
            vlan-id 35;
            family inet {
                address 10.100.3.17/30;
            }
        }
    }
    em0 {
        unit 0 {
            family inet {
                address 10.200.1.6/24;
            }
        }
    }
    lo0 {
        unit 0 {
            family inet {
                address 10.210.1.6/32;
            }
            family iso {
                address 49.1111.0102.1000.1006.00;
            }
        }
    }
}
routing-options {
    autonomous-system 123;
}
protocols {
    rsvp {
        disable;
    }
    mpls {
        interface ge-0/0/2.0;
        interface ge-0/0/3.0;
    }
    bgp {
        group ibgp {
            type internal;
            local-address 10.210.1.6;
            family inet {
                unicast;
            }
            family inet-vpn {
                unicast {
                    loops 2;
                }
            }
            family inet6-vpn {
                unicast;
            }
            family route-target;
            neighbor 10.210.1.10;
        }
    }
    isis {
        level 1 disable;
        interface ge-0/0/2.0 {
            point-to-point;
        }
        interface ge-0/0/3.0 {
            point-to-point;
        }
        interface lo0.0;
    }
    ldp {
        interface ge-0/0/2.0;
        interface ge-0/0/3.0;
        interface lo0.0;
    }
}
policy-options {
    policy-statement EXPORT_OSPF_C1 {
        term 1 {
            from protocol bgp;
            then accept;
        }
    }
    policy-statement EXPORT_VRF_C1 {
        term 1 {
            then {
                community add target:123:1;
                community add domain-id:192.168.1.1:0;
                accept;
            }
        }
        term final {
            then reject;
        }
    }
    policy-statement EXPORT_VRF_C3_SPOKE {
        term 1 {
            then {
                community add C3_SPOKE;
                community add C3_ORIGIN_R6;
                community add C3_R6;
                accept;
            }
        }
        term final {
            then reject;
        }
    }
    policy-statement IMPORT_VRF_C1 {
        term 1 {
            from {
                protocol bgp;
                community target:123:1;
            }
            then accept;
        }
        term 2 {
            from {
                interface ge-0/0/5.35;
                community C3_R6;
            }
            then accept;
        }
        term final {
            then reject;
        }
    }
    policy-statement IMPORT_VRF_C3_SPOKE {
        term 0 {
            from {
                protocol bgp;
                community C3_ORIGIN_R5;
            }
            then reject;
        }
        term 1 {
            from {
                protocol bgp;
                community C3_HUB;
            }
            then accept;
        }
        term 2 {
            from {
                interface ge-0/0/5.11;
                community target:123:1;
            }
            then accept;
        }
        term final {
            then reject;
        }
    }
    community C3_HUB members target:123:31;
    community C3_ORIGIN_R5 members origin:10.210.1.5:1;
    community C3_ORIGIN_R6 members origin:10.210.1.6:1;
    community C3_R6 members target:123:36;
    community C3_SPOKE members target:123:32;
    community domain-id:192.168.1.1:0 members domain-id:192.168.1.1:0;
    community target:123:1 members target:123:1;
}
routing-instances {
    C1 {
        instance-type vrf;
        interface ge-0/0/5.11;
        route-distinguisher 10.210.1.6:1;
        vrf-import IMPORT_VRF_C1;
        vrf-export EXPORT_VRF_C1;
        inactive: vrf-target target:123:1;
        routing-options {
            auto-export;
        }
        protocols {
            ospf {
                domain-id 192.168.1.1;
                export EXPORT_OSPF_C1;
                area 0.0.0.0 {
                    interface ge-0/0/5.11;
                }
            }
        }
    }
    C3 {
        instance-type vrf;
        interface ge-0/0/5.35;
        route-distinguisher 10.210.1.6:32;
        vrf-import IMPORT_VRF_C3_SPOKE;
        vrf-export EXPORT_VRF_C3_SPOKE;
        vrf-table-label;
        routing-options {
            auto-export;
        }
        protocols {
            bgp {
                group C3_S2_1 {
                    type external;
                    peer-as 45543;
                    as-override;
                    neighbor 10.100.3.18;
                }
            }
        }
    }
}
```

- **R7**:

```
system {
    host-name R7;
    time-zone Asia/Saigon;
    root-authentication {
        encrypted-password "$6$KQfP9GYY$0meQNT1L3.bxlLOtvOL4bejHPFfWVQDAU9RhJcE2pROP.hmzTHKRVO1cgFwqs6miracC.XOlH4oJPSwqwCYlH0"; ## SECRET-DATA
    }
    login {
        user lab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$/WgLGrDM$0tn6F8h6QGG0CC8KbIpAeV6v35maKmNouxNYaK1vIS6PhO9dYrV0vDnG4gqFty1UDfbRSR1z3KGGIx8l6wt4r."; ## SECRET-DATA
            }
        }
        user labsvtech {
            uid 2001;
            class super-user;
            authentication {
                encrypted-password "$6$SL/eyx1r$Y9lehX2oBKHEEH55H2FDBYXlKo4QKd/TJakrbqUqDJCW0Vbp0Q05GWlk0HOVZmwICbISkhM53uf1RzCLAdIDV0"; ## SECRET-DATA
            }
        }
    }
    services {
        ssh;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    ge-0/0/1 {
        unit 0 {
            family inet {
                address 10.10.9.7/24;
            }
            family mpls;
        }
    }
    ge-0/0/3 {
        apply-groups-except interface-family; ## 'interface-family' is not defined
        description to-r3;
        unit 0 {
            family inet {
                address 10.100.1.6/30;
            }
        }
    }
    em0 {
        unit 0 {
            family inet {
                address 10.200.1.7/24;
            }
        }
    }
    lo0 {
        unit 0 {
            family inet {
                address 10.210.1.7/32;
            }
        }
    }
}
routing-options {
    autonomous-system 345;
}
protocols {
    mpls {
        interface ge-0/0/1.0;
    }
    bgp {
        group ibgp {
            type internal;
            local-address 10.210.1.7;
            family inet {
                unicast;
            }
            family inet-vpn {
                unicast;
            }
            family inet6-vpn {
                unicast;
            }
            neighbor 10.210.1.8;
        }
    }
    ospf {
        area 0.0.0.0 {
            interface lo0.0;
            interface ge-0/0/1.0 {
                interface-type p2p;
            }
        }
    }
    ldp {
        interface ge-0/0/1.0;
        interface lo0.0;
    }
}
policy-options {
    policy-statement EXPORT_OSPF_CE_C1 {
        term 1 {
            from protocol bgp;
            then accept;
        }
    }
}
routing-instances {
    C1 {
        instance-type vrf;
        interface ge-0/0/3.0;
        route-distinguisher 10.210.1.7:1;
        vrf-target target:345:1;
        vrf-table-label;
        protocols {
            ospf {
                domain-id disable;
                domain-vpn-tag 0;
                export EXPORT_OSPF_CE_C1;
                area 0.0.0.0 {
                    interface ge-0/0/3.0 {
                        interface-type p2p;
                    }
                }
            }
        }
    }
}
```

- **R8**:

```
system {
    host-name R8;
    time-zone Asia/Saigon;
    root-authentication {
        encrypted-password "$6$KQfP9GYY$0meQNT1L3.bxlLOtvOL4bejHPFfWVQDAU9RhJcE2pROP.hmzTHKRVO1cgFwqs6miracC.XOlH4oJPSwqwCYlH0"; ## SECRET-DATA
    }
    login {
        user lab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$/WgLGrDM$0tn6F8h6QGG0CC8KbIpAeV6v35maKmNouxNYaK1vIS6PhO9dYrV0vDnG4gqFty1UDfbRSR1z3KGGIx8l6wt4r."; ## SECRET-DATA
            }
        }
        user labsvtech {
            uid 2001;
            class super-user;
            authentication {
                encrypted-password "$6$SL/eyx1r$Y9lehX2oBKHEEH55H2FDBYXlKo4QKd/TJakrbqUqDJCW0Vbp0Q05GWlk0HOVZmwICbISkhM53uf1RzCLAdIDV0"; ## SECRET-DATA
            }
        }
    }
    services {
        ssh;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    ge-0/0/1 {
        unit 0 {
            family inet {
                address 10.10.9.8/24;
            }
            family mpls;
        }
    }
    ge-0/0/5 {
        apply-groups-except interface-family; ## 'interface-family' is not defined
        flexible-vlan-tagging;
        encapsulation flexible-ethernet-services;
        unit 12 {
            vlan-id 12;
            family inet {
                address 10.100.1.9/30;
            }
        }
    }
    em0 {
        unit 0 {
            family inet {
                address 10.200.1.8/24;
            }
        }
    }
    lo0 {
        unit 0 {
            family inet {
                address 10.210.1.8/32;
            }
        }
    }
}
routing-options {
    autonomous-system 345;
}
protocols {
    mpls {
        interface ge-0/0/1.0;
    }
    bgp {
        group ibgp {
            type internal;
            local-address 10.210.1.8;
            family inet {
                unicast;
            }
            family inet-vpn {
                unicast;
            }
            family inet6-vpn {
                unicast;
            }
            neighbor 10.210.1.7;
        }
    }
    ospf {
        area 0.0.0.0 {
            interface lo0.0;
            interface ge-0/0/1.0 {
                interface-type p2p;
            }
        }
    }
    ldp {
        interface ge-0/0/1.0;
        interface lo0.0;
    }
}
policy-options {
    policy-statement EXPORT_OSPF_C1 {
        term 1 {
            from protocol bgp;
            then accept;
        }
    }
}
routing-instances {
    C1 {
        instance-type vrf;
        interface ge-0/0/5.12;
        route-distinguisher 10.210.1.8:1;
        vrf-target target:345:1;
        vrf-table-label;
        protocols {
            ospf {
                export EXPORT_OSPF_C1;
                area 0.0.0.0 {
                    interface ge-0/0/5.12 {
                        interface-type p2p;
                    }
                }
            }
        }
    }
}
```

- **RR**:

```
groups {
    nhs {
        protocols {
            bgp {
                export nhs;
            }
        }
    }
}
system {
    host-name RR;
    time-zone Asia/Saigon;
    root-authentication {
        encrypted-password "$6$KQfP9GYY$0meQNT1L3.bxlLOtvOL4bejHPFfWVQDAU9RhJcE2pROP.hmzTHKRVO1cgFwqs6miracC.XOlH4oJPSwqwCYlH0"; ## SECRET-DATA
    }
    login {
        user lab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$/WgLGrDM$0tn6F8h6QGG0CC8KbIpAeV6v35maKmNouxNYaK1vIS6PhO9dYrV0vDnG4gqFty1UDfbRSR1z3KGGIx8l6wt4r."; ## SECRET-DATA
            }
        }
        user labsvtech {
            uid 2001;
            class super-user;
            authentication {
                encrypted-password "$6$SL/eyx1r$Y9lehX2oBKHEEH55H2FDBYXlKo4QKd/TJakrbqUqDJCW0Vbp0Q05GWlk0HOVZmwICbISkhM53uf1RzCLAdIDV0"; ## SECRET-DATA
            }
        }
    }
    services {
        ssh;
        telnet;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    ge-0/0/1 {
        description to-r5;
        unit 0 {
            family inet {
                address 10.10.10.10/24;
            }
            family iso;
        }
    }
    em0 {
        unit 0 {
            family inet {
                address 10.200.1.10/24;
            }
        }
    }
    lo0 {
        unit 0 {
            family inet {
                address 10.210.1.10/32;
            }
            family iso {
                address 49.1111.0102.1000.1010.00;
            }
        }
    }
}
routing-options {
    rib inet.3 {
        static {
            route 0.0.0.0/0 discard;
        }
    }
    rib inet6.3 {
        static {
            route ::/0 discard;
        }
    }
    autonomous-system 123;
}
protocols {
    bgp {
        keep all;
        group ibgp {
            type internal;
            local-address 10.210.1.10;
            family inet {
                unicast;
            }
            family inet-vpn {
                unicast {
                    loops 2;
                }
            }
            family inet6-vpn {
                unicast;
            }
            family route-target {
                advertise-default;
            }
            cluster 10.210.1.10;
            neighbor 10.210.1.1;
            neighbor 10.210.1.2;
            neighbor 10.210.1.3;
            neighbor 10.210.1.4;
            neighbor 10.210.1.5;
            neighbor 10.210.1.6;
        }
    }
    isis {
        level 1 disable;
        interface ge-0/0/1.0 {
            point-to-point;
        }
        interface lo0.0;
    }
}
policy-options {
    policy-statement nhs {
        term 1 {
            from protocol bgp;
            then {
                next-hop self;
            }
        }
    }
}
```
