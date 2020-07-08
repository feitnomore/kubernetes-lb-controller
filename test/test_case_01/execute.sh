#!/bin/sh
alias kubectl="kubectl --insecure-skip-tls-verify"
MY_POD=`kubectl get pods -n kube-system --insecure-skip-tls-verify | grep kubernetes-lb-controller | awk '{print $1}'`
KUBE_CMD="kubectl exec $MY_POD -n kube-system cat /var/run/routes --insecure-skip-tls-verify"
#KUBE_CMD="docker exec -it kubernetes-lb-controller sh -c 'cat /var/run/routes'"

for i in 01.yaml 02.yaml 03.yaml 04.yaml 05.yaml
do
	kubectl apply -f $i
done

echo "Added the initial services:"
kubectl get services --all-namespaces -o wide

$KUBE_CMD

echo "****************************************"
echo "****************************************"

kubectl apply -f 06.yaml
kubectl apply -f 07.yaml

echo ""
echo "Added the other two"

kubectl get services --all-namespaces -o wide

$KUBE_CMD

echo "Services should be pending"
