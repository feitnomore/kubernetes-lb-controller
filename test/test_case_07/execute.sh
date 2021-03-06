#!/bin/sh
alias kubectl="kubectl --insecure-skip-tls-verify"
MY_POD=`kubectl get pods -n kube-system --insecure-skip-tls-verify | grep kubernetes-lb-controller | awk '{print $1}'`
KUBE_CMD="kubectl exec $MY_POD -n kube-system cat /var/run/routes --insecure-skip-tls-verify"
#KUBE_CMD="docker exec -it kubernetes-lb-controller sh -c 'cat /var/run/routes'"

kubectl apply -f 01.yaml

kubectl get services --all-namespaces -o wide

$KUBE_CMD

echo "Should see service 01 added"
echo "****************************************"
echo "****************************************"

kubectl apply -f 02.yaml

kubectl get services --all-namespaces -o wide

$KUBE_CMD

echo "Should see service 01 updated on the same IP"
