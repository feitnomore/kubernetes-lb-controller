# kubernetes-lb-controller


**Maintainers:** [feitnomore](https://github.com/feitnomore/)

This is a simple weekend hack to implement a controller for [Kubernetes](https://kubernetes.io) responsible for assigning External IPs to `Services` of type `LoadBalancer` on a Bare Metal/Traditional VM environment.
In my case, I do this through aliases on the public interface, but can be done on multi-home environments as well.

*WARNING:* Use it at your own risk.

## TESTS

Tests were performed on 2 cluster environments as well as a minikube deployment running on a VM.  
The test cases performed can be found here.  
The Controller ConfigMap file used to execute the tests is also available here.  
  
List of test scripts:

* [test_case_01](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_01): Add more than 5 IPs on the same Namespace with only 5 IPs available on the Namespace in the YAML.  
* [test_case_02](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_02): Add 10 services, 5 in each Namespace, and after that, 1 on each while we have only 5 ips available for each Namespace in the YAML.  
* [test_case_03](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_03): Add services on a different Namespace than available the one with IPs available on the YAML.  
* [test_case_04](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_04): Add services, remove one from the middle, and add back, to see if it comes back on the old IP.  
* [test_case_05](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_05): Add services, remove all, add 2 back from the middle, to see if they come back with their old IP.  
* [test_case_06](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_06): Add services with IPs that are not on the YAML file.  
* [test_case_07](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_07): Modify service, that was added before without specifying IP, without specifying IP again.  
* [test_case_08](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_08): Modify service, that was added before without specifying IP, with IP that is not in the YAML.  
* [test_case_09](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_09): Modify service, that was added before specifying IP that is not on YAML, without specifying IP.  
* [test_case_10](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_10): Modify service, that was added before without specifying IP, with valid IP from the YAML.  
* [test_case_11](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_11): Modify service, that was added before with IP that is on YAML, with a IP that is on YAML.  
* [test_case_12](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_12): Modify service, that was added before with IP that is on YAML, with a different IP that is on the YAML.  
* [test_case_13](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_13): Delete service, that was added before without specifying IP, without specifying IP.  
* [test_case_14](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_14): Delete service, that was added before specifying IP that is on YAML, without specifying IP.  
* [test_case_15](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_15): Delete service, that was added before specifying IP that is not on YAML, without specifying IP.  
* [test_case_16](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_16): Delete service, that was added before without specifying IP, specifying the IP assigned by Controller.  
* [test_case_17](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_17): Delete service, that was added before specifying IP that is not on YAML, using the same IP.  
* [test_case_18](https://github.com/feitnomore/kubernetes-lb-controller/tree/master/test/test_case_18): Delete service, that was added before specifying IP that is on YAML, using the same IP.  

