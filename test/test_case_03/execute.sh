#!/bin/sh
alias kubectl="kubectl --insecure-skip-tls-verify"
MY_POD=`kubectl get pods -n kube-system --insecure-skip-tls-verify | grep kubernetes-lb-controller | awk '{print $1}'`
KUBE_CMD="kubectl exec $MY_POD -n kube-system cat /routes --insecure-skip-tls-verify"
#KUBE_CMD="docker exec -it kubernetes-lb-controller sh -c 'cat /routes'"

for i in namespace.yaml 01.yaml 02.yaml 03.yaml 04.yaml
do
	kubectl apply -f $i
done

kubectl get services --all-namespaces -o wide

$KUBE_CMD

echo "Should see services in peding"
