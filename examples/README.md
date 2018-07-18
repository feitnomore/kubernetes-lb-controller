# kubernetes-lb-controller


**Maintainers:** [feitnomore](https://github.com/feitnomore/)

This is a simple weekend hack to implement a controller for [Kubernetes](https://kubernetes.io) responsible for assigning External IPs to `Services` of type `LoadBalancer` on a Bare Metal/Traditional VM environment.
In my case, I do this through aliases on the public interface, but can be done on multi-home environments as well.

*WARNING:* Use it at your own risk.

## EXAMPLES

Here are some example *YAML* files for reference when working with the Controller.