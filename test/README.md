# kubernetes-lb-controller


**Maintainers:** [feitnomore](https://github.com/feitnomore/)

This is a simple weekend hack to implement a controller for [Kubernetes](https://kubernetes.io) responsible for assigning External IPs to `Services` of type `LoadBalancer` on a Bare Metal/Traditional VM environment.
In my case, I do this through aliases on the public interface, but can be done on multi-home environments as well.

*WARNING:* Use it at your own risk.

## TESTS

Tests were performed on 2 cluster environments as well as a minikube deployment running on a VM.  
The test cases performed can be found here.  
The Controller Deploypment file is also available here.  
  
List of test scripts:

```
test_case_01: Add more than 5 IPs on the same namespace with only 5 IPs available.
test_case_02: Add more than 10 services, 5 in each namespace, and 1 on each while we have only 5 ips available for namespace.
test_case_03: Add services on a different namespace than available
test_case_04: Add services, remove one from the middle, and add back
test_case_05: Add services, remove all, add 2 in the middle
test_case_06: Add services with IPs that are not on database
test_case_07: Modify service without IP (that was added before without IP)
test_case_08: Modify service with invalid IP (that was added before without IP)
test_case_09: Modify service without IP (that was added before with IP)
test_case_10: Modify service with valid IP (that was added before without IP)
test_case_11: Modify service with valid IP (that was added before with invalid IP)
test_case_12: Modify service with valid IP (that was added before with different valid IP)
test_case_13: Delete without IP (that was added without IP)
test_case_14: Delete without IP (that was added with valid IP before)
test_case_15: Delete without IP (that was added with invalid IP before)
test_case_16: Delete with valid IP (that was added without IP)
test_case_17: Delete with invalid IP (that was added with invalid IP)
test_case_18: Delete with valid IP (that was added with valid IP)
``` 
