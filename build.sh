#!/bin/sh
# Build and Exec
# I am too tired of doing this by hand

docker rm kubernetes-lb-controller
docker rmi kubernetes-lb-controller --force
docker build -t kubernetes-lb-controller .

# Pushing to remote repository
export MY_REPO="feitnomore"
docker tag kubernetes-lb-controller:latest $MY_REPO/kubernetes-lb-controller:latest
docker push $MY_REPO/kubernetes-lb-controller:latest