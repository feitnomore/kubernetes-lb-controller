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
        cd $i/
		./execute.sh
		sleep 15s
		if [ -f ./cleanup.sh ]
		then
			./cleanup.sh
			sleep 15s
		fi
        cd ..
	fi
done