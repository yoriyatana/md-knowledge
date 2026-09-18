# Delay thời gian up time của CE interfaces

để optimize down time do bi core isolation: sẽ delay thời gian up time của CE interfaces:

```text
lab@mx480-re0# show protocols network-isolation
```

```text
group hoo {
```

detection {

hold-time up 60000;

service-tracking {

core-isolation;

}

}

service-tracking-action link-down;

}

```text
lab@mx480-re0# show interfaces ae0
```

flexible-vlan-tagging;

mtu 9216;

encapsulation flexible-ethernet-services;

network-isolation-profile hoo;
