#!/bin/sh
alias kubectl="kubectl --insecure-skip-tls-verify"
MY_POD=`kubectl get pods -n kube-system --insecure-skip-tls-verify | grep kubernetes-lb-controller | awk '{print $1}'`
KUBE_CMD="kubectl exec $MY_POD -n kube-system cat /routes --insecure-skip-tls-verify"
#KUBE_CMD="docker exec -it kubernetes-lb-controller sh -c 'cat /routes'"

for i in 01.yaml 02.yaml 03.yaml 04.yaml 05.yaml
do
	kubectl apply -f $i
done

kubectl get services --all-namespaces -o wide

$KUBE_CMD

echo "Should see all 05 services added"
echo "****************************************"
echo "****************************************"

kubectl delete -f 02.yaml

kubectl get services --all-namespaces -o wide

$KUBE_CMD

echo "Should see service 02 removed"
echo "****************************************"
echo "****************************************"

kubectl apply -f 02.yaml

kubectl get services --all-namespaces -o wide

$KUBE_CMD

echo "Should see service 02 on the same as before..."

