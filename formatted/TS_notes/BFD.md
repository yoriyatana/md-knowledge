# BFD

```
run show bfd session
run show bfd session detail
run show ppm adjacencies protocol bfd detail
run request pfe execute command "show ppm adjacencies protocol bfd" target fpc7
run show chassis fabric fpcs

run request chassis fabric pfe 0 fpc 7 offline
run show bfd session
run show ppm adjacencies protocol bfd detail
run request pfe execute command "show ppm adjacencies protocol bfd" target fpc7
```

show ppm transmissions protocol bfd detail

show ppm adjacencies protocol bfd detail

show ppm dfw-statistics

show ppm distribution-statistics

show ppm request-queue

show ppm rpc-statistics

PFE:

show syslog messages

show ppm adjacencies protocol bfd

show ppm transmits protocol bfd

show ppm statistics protocol bfd

show pfe statistics traffic

show pfe statistics errors

show pfe statistics notification

show pfe manager session statistics

show pfe manager queue

show threads

clear threads max-time

show threads verbose

show pfe bfdsession all

show pfe bfdsession id <session_id> extensive

show filter

show filter index <ppmd_filter> program

show packet

show ttp statistics

###### #####################

### RPD

set cli timestamp

show chassis hardware

show chassis routing-engine

show system processes extensive no-forwarding | except 0.00

show system processes memory <pid|process-name>

show system virtual-memory | no-more

show task memory detail | no-more

show log messages | no-more

show log messages | match RPD_SCHED_SLIP

show task accounting

show krt queue

show krt state

show task io

show task jobs

show task accounting detail

show task summary

show system processes extensive no-forwarding | except 0.00

show chassis routing-engine

show chassis fpc

show chassis fpc details

show system resource-monitor fpc

- -----

request pfe execute command "show heap 0" target fpc0

request pfe execute command "show nhdb summary detail" target fpc0

request pfe execute command "show nhdb sizes" target fpc0

request pfe execute command "show heap 0 sanity" target fpc0

request pfe execute command "show jnh 0 pool summary" target fpc0

request pfe execute command "show jnh 0 pool" target fpc0

request pfe execute command "show jnh 0 pool usage" target fpc0

request pfe execute command "show jnh 0 pool detail" target fpc0

request pfe execute command "show jnh 0 pool layout" target fpc0

request pfe execute command "show jnh 0 pool layout verbose" target fpc0

request pfe execute command "show jnh 0 pool composition" target fpc0

request pfe execute command "show jnh 0 pool stats nh" target fpc0

request pfe execute command "show jnh 0 pool stats fw" target fpc0

request pfe execute command "show jnh 0 pool stats cnt" target fpc0

request pfe execute command "show cassis_alloc" target fpc0

request pfe execute command "show sample-rr summary" target fpc0

request pfe execute command "show resmon summary" target fpc0

request pfe execute command "show nhdb summary detail" target fpc0
