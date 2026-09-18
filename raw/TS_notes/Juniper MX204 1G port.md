# Juniper MX204 1G port

lab@MX-204-01> show configuration interfaces xe-0/1/5

speed 1g;

gigether-options {

auto-negotiation;

speed 1g;

}

--

Juniper MX204 1G port auto negotiate

Thought this would save some people a bit of grief in case you need any 1G ports on the MX204 (and possibly other MX series with rate selectability).

Example of a **non-functioning 1G** port (note, from my understanding speed 1G does not mean hard coded speed/duplex, this is required on MX204 because of the 10G ports for some reason):

xe-0/1/0 {

gigether-options {

speed 1g;

}

}

Example of a **functioning 1G port** (assuming you want auto-negotiation):

xe-0/1/0 {

gigether-options {

auto-negotiation;

speed 1g;

}

}
