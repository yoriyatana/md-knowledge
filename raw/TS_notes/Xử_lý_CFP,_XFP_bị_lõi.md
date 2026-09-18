# Xử lý CFP, XFP bị lõi

**1. Thực hiện soft-loop & hard-loop (loop local), thu thập thông tin sau:**

```
show chassis hardware
show interfaces diagnostics optics (et-… / xe-…)
show interfaces (et-… / xe-…)
```

- Note câu lệnh soft-loop: 

```
set interfaces <et-… | xe-…> gigether-options loopback
```

 

**2. Thu thập tập lệnh output sau trong 2 trường hợp** **soft-loop** **v�**� **hard-loop**

**Note đối với module** **_CFP 100Gig_:**

```
> start shell pfe network fpc#
# show syslog messages
# show cfp list                 ### get the cfp id from here and below outputs  
# show cfp <index> alarms
# show cfp <index> diagnostics
# show cfp <index> identifier
# show cfp <index> info   
# show cfp <index> mdio-bus-error-count
# show cmic 0 info
# show cmic 0 interrupts
# show mtip-cgpcs summary  
# show mtip-cgpcs <index> registers
# show mtip-cgpcs <index> errors
# show mtip-cgpcs <index> error-count
# show mtip-cgpcs <index> block-lock
# show mtip-cgpcs <index> fault-condition
# show mtip-cgpcs <index> high-BER
# show mtip-cgpcs <index> link-status
# show syslog messages
# show nvram
```

 

**Note đối với module** **_SFP+_** **_10Gig_:**

```
> start shell pfe network fpc#
# show syslog messages
# show sfp list ### get the cfp id from here and below outputs  
# show sfp <index> alarms
# show sfp <index> diagnostics
# show sfp <index> identifier
# show sfp <index> info   
# show sfp <index> mdio-bus-error-count
# show mic 0 info
# show mic 0 interrupts
# show mtip-cgpcs summary  
# show mtip-cgpcs <index> registers
# show mtip-cgpcs <index> errors
# show mtip-cgpcs <index> error-count
# show mtip-cgpcs <index> block-lock
# show mtip-cgpcs <index> fault-condition
# show mtip-cgpcs <index> high-BER
# show mtip-cgpcs <index> link-status
# show syslog messages
# show nvram
```

**Note đối với module** **_XFP 10Gig_:**

```
> start shell pfe network fpc#
# show xfp list ### get the xfp id from here and below outputs  
# show xfp <index> alarms
# show xfp <index> diagnostics
# show xfp <index> identifier
# show xfp <index> info   
# show xfp <index> mdio-bus-error-count
# show mic 0 info
# show mic 0 interrupts
# show mtip-cgpcs summary
# show mtip-cgpcs <index> registers
# show mtip-cgpcs <index> errors
# show mtip-cgpcs <index> error-count
# show mtip-cgpcs <index> block-lock
# show mtip-cgpcs <index> fault-condition
# show mtip-cgpcs <index> high-BER
# show mtip-cgpcs <index> link-status
# show syslog messages
# show nvram
```

# Check với QSFP 100G:

```
1. Thực hiện soft-loop, hard-loop (local loop):
> show chassis hardware
> show interfaces diagnostics optics (et-… / xe-…)
> show interfaces (et-… / xe-…)

2. Thu thập RSI, var/log.
3. Gửi hình ảnh của moudule đang bị lỗi.
4. Thu thập các tập lệnh output sau trong trường hợp hard-loop:
> start shell pfe network fpc#
# show syslog messages
# show cfp list ### get the cfp id from here and below outputs
# show cfp <index> alarms
# show cfp <index> diagnostics
# show cfp <index> identifier
# show cfp <index> info
# show cfp <index> mdio-bus-error-count
# show cmic 0 info
# show cmic 0 interrupts
# show mtip-cgpcs summary
# show mtip-cgpcs <index> registers
# show mtip-cgpcs <index> errors
# show mtip-cgpcs <index> error-count
# show mtip-cgpcs <index> block-lock
# show mtip-cgpcs <index> fault-condition
# show mtip-cgpcs <index> high-BER
# show mtip-cgpcs <index> link-status
# show syslog messages
# show nvram
```

---

The 'PCI Fatal' errors seen above do not represent an actual hardware issue with the MIC or router. The following commands may help identify the presence of any faulty SFPs:

|# show sfp list

# show sfp <index from show sfp list> info

Check i2c failure count on each SFP. If the SFP shows a non-zero i2c failure count, replace that specific SFP.

# show sfp 3 info

show sfp 3 info

index: 0x03

sfp name: MIC(0/1)

pic context: 0x4CD44248

id mem scanned: false

linkstate: Up

sfp_present: false

sfp_changed: false

i2c failure count: 0x3C <<<--- non-zero

diag polling count: 0x8D42

no diag polling from RE:0x1

run_periodic: false
> start shell pfe network afeb0|
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
