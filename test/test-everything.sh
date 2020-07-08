#!/bin/sh
# Too lazy to run each test by hand

kubectl delete -f test-ConfigMap.yaml
sleep 15s
kubectl apply -f test-ConfigMap.yaml
sleep 15s
MY_POD=`kubectl get pods -n kube-system | grep kubernetes-lb-controller | awk '{print $1}'`
kubectl delete pod $MY_POD -n kube-system
sleep 120s

for i in *
do
	if [ -d $i ]
	then
		$i/execute.sh
		sleep 15s
		if [ -f $i/cleanup.sh ]
		then
			$i/cleanup.sh
			sleep 15s
		fi
	fi
done