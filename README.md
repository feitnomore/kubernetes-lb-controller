# kubernetes-lb-controller


**Maintainers:** [feitnomore](https://github.com/feitnomore/)

This is a simple weekend hack to implement a controller for [Kubernetes](https://kubernetes.io) responsible for assigning External IPs to `Services` of type `LoadBalancer` on a Bare Metal/Traditional VM environment.
In my case, I do this through aliases on the public interface, but can be done on multi-home environments as well.

*WARNING:* Use it at your own risk.

## INTRODUCTION

The idea of this Controller is to be able to provide Extenal IPs to Services of type LoadBalancer on traditional environments like Bare Metal or VMs. This Controller simulates the idea of the cloud plugins that can assign an IP to a Service of type LoadBalancer in a dynamic way.  
In order for this to work, the IPs that are going to be used needs to be available on the nodes that executes the `kube-proxy`. In my environments I do this by adding them to the `master` node.  
The Controller can keep track of which IPs are in use, by which Services, and in case a new Service shows up and there are no free IPs, the Controller will leave the Service in pending status.
It is possible to assign different IPs for different namespaces as well, and remember, the aliases doesn't need to be in the same interface, for example, you can have some IP addresses on interface 1 for testing environemnt and some other IP addresses on interface 2 for development environment.  
The Controller takes the Namespace and the IP that will be available as parameter. 

## HOW TO INSTALL IT

The details below assume you are creating a `ServiceAccount`, a `ClusterRoleBinding`, a `Deployment` and a `Pod`, all on the *kube-system* `Namespace`. Please, adjust as necessary.  
*Note:* We are adding `cluster-admin` as the `ClusterRole` for the `ServiceAccount`.

### Create a Service Account
```
kubectl apply -f https://adjust/kubernetes-lb-controller_ServiceAccount.yaml
```
### Create the Cluster Role Binding
```
kubectl apply -f https://adjust/kubernetes-lb-controller_ClusterRoleBinding.yaml
```
### Add IPs on your kubemaster node
```
ifconfig eth0:0 192.168.55.10 netmask 255.255.255.0
ifconfig eth0:1 192.168.55.11 netmask 255.255.255.0
ifconfig eth0:1 192.168.55.12 netmask 255.255.255.0
```
*Note:* Assuming your public interface is `eth0`.   
*Note:* Assuming you are using network interface `aliases`.  
*Note:* Assuming your public netword CIDR is `192.168.55.0/24`.  

### Create the Deployment Descriptor
Create the kubernetes-lb-controller_Deployment.yaml using the IPs that were added before. The list of IPs needs to be in the format `namespace:IP` , like the example below:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubernetes-lb-controller
  namespace: kube-system
  labels:
    k8s-app: kubernetes-lb-controller
spec:
  selector:
    matchLabels:
      k8s-app: kubernetes-lb-controller
  replicas: 1
  template:
    metadata:
      labels:
        k8s-app: kubernetes-lb-controller
    spec:
      containers:
        - name: kubernetes-lb-controller
          image: feitnomore/kubernetes-lb-controller:latest
          imagePullPolicy: Always
          env:
          - name: IP_LIST
            value: "
              default:192.168.55.11
              default:192.168.55.12
              default:192.168.55.13"
      serviceAccountName: kubernetes-lb-controller
      restartPolicy: Always
```
*Note:* The IPs are being added to the `default` namespace.  
*Note:* Not much test has been done on the environment formatting, so please, try to respect the formatting above.  

### Apply the Deployment
```
kubectl apply -f kubernetes-lb-controller_Deployment.yaml
```
## HOW TO USE IT

The details below assumes you are creating a `Service`, of type `LoadBalancer` on the *default* `Namespace`. It also assumes you followed the previous steps and is running our controller on the *kube-system* `Namespace`. Please, adjust as necessary.

### Deploy a Service with type LoadBalancer
Create a service with `type: LoadBalancer` without specifying the external IP, like for example:
```
apiVersion: v1
kind: Service
metadata:
  name: my-testing-service
  namespace: default
  labels:
    app: my-testing-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: my-testing-app
status:
  loadBalancer: {}
```
*Note:* The service is being created on the `default` namespace.

### Verify the Service got created and got an IP assigned to it
```
kubectl get services -n default -o wide
```
*Note:* We are checking the `default` namespace.

### Verify the Controller Routing Table
```
LB_CONTROLLER=`kubectl get pods -n kube-system | grep kubernetes-lb-controller | awk '{print $1}'`
kubectl exec $LB_CONTROLLER -n kube-system cat /routes
```
*Note:* Although our service is on *default* `Namespace`, the Controller is running on *kube-system*.  
*Note:* The route table is being written to a text file called *routes* on */*.  

## REFERENCES AND IDEAS

1. [Kubernetes](https://kubernetes.io/)
2. [Python 2.7](https://www.python.org/)
3. [Kubernetes Python Client](https://github.com/kubernetes-client/python)
4. [Python SQLite 3](https://docs.python.org/2/library/sqlite3.html)
5. [Docker Hub](https://hub.docker.com/r/feitnomore/kubernetes-lb-controller/)

## DOCUMENTATION

1. [Building](https://github.com/feitnomore/BUILD.md)
2. [Examples](https://github.com/feitnomore/examples/README.md)
3. [Tests](https://github.com/feitnomore/tests/README.md)

