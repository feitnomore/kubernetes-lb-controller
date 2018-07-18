#!/bin/sh
alias kubectl="kubectl --insecure-skip-tls-verify"
MY_POD=`kubectl get pods -n kube-system --insecure-skip-tls-verify | grep kubernetes-lb-controller | awk '{print $1}'`
KUBE_CMD="kubectl exec $MY_POD -n kube-system cat /routes --insecure-skip-tls-verify"
#KUBE_CMD="docker exec -it kubernetes-lb-controller sh -c 'cat /routes'"

kubectl delete -f 02.yaml
