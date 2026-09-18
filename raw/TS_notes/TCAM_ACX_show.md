# TCAM ACX show

In order to check the state of the TCAM, it is recommended to run the following CLI commands periodically as a health check of the system:

> show pfe tcam usage all-tcam-stages
> 
> show pfe tcam usage all-tcam-stages detail
> 
> show pfe tcam usage tcam-stage <ingress|egress|pre-ingress>
> 
> show pfe tcam usage tcam-stage <ingress|egress|pre-ingress> app ?
> 
> show pfe tcam usage app <fw-ccc-in>
> 
> show pfe tcam errors
> 
> show pfe tcam errors <all-tcam-stages|tcam-stage|app> <detail>
> 
> show pfe tcam app ?
