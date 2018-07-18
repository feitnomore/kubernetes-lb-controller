# kubernetes-lb-controller


**Maintainers:** [feitnomore](https://github.com/feitnomore/)

This is a simple weekend hack to implement a controller for [Kubernetes](https://kubernetes.io) responsible for assigning External IPs to `Services` of type `LoadBalancer` on a Bare Metal/Traditional VM environment.
In my case, I do this through aliases on the public interface, but can be done on multi-home environments as well.

*WARNING:* Use it at your own risk.

## BUILD

Here you can find some simple information on how to build this project by yourself.

### Clone the Repository
```
git clone https://github.com/feitnomore/kubernetes-lb-controller.git
```

### Make your changes

*Note:* Remember to edit `Dockerfile` according to your changes. 

### Build the Image
```
cd kubernetes-lb-controller
docker build -t kubernetes-lb-controller .
```

### Push the image to the Repository
````
export MY_REPO="feitnomore"
docker tag kubernetes-lb-controller:latest $MY_REPO/kubernetes-lb-controller:latest
docker push $MY_REPO/kubernetes-lb-controller:latest
````

### Execute the controller
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
              default:192.168.55.10
              default:192.168.55.11
              default:192.168.55.12"
      serviceAccountName: kubernetes-lb-controller
      restartPolicy: Always
```
*Note:* Remember to point the `image` to the repository you are using. 
*Note:* Remember to create the `ServiceAccount` and `ClusterRole` before creating the `Deployment`. 