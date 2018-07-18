#!/bin/sh
alias kubectl="kubectl --insecure-skip-tls-verify"

for i in 01.yaml 02.yaml 03.yaml 04.yaml 05.yaml
do
	kubectl delete -f $i
done

