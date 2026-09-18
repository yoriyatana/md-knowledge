# Check ddos-protection param on QFX5K

To check  the internal control protocol/exception traffic mapped to the internal DDOS queues, the command below can be collected from shell (choosing the proper FPC):

`cprod -A fpc0 -c "show halp-pkt asic-queues"`
