#!/bin/sh
# Build and Exec
# I am too lazy to do this by hand

docker rm kubernetes-lb-controller:2.1
docker rmi kubernetes-lb-controller:2.1 --force
docker build -t kubernetes-lb-controller:2.1 .

# Pushing to remote repository
export MY_REPO="feitnomore"
docker tag kubernetes-lb-controller:2.1 $MY_REPO/kubernetes-lb-controller:2.1
docker push $MY_REPO/kubernetes-lb-controller:2.1

docker tag kubernetes-lb-controller:2.1 $MY_REPO/kubernetes-lb-controller:latest
docker push $MY_REPO/kubernetes-lb-controller:latest
