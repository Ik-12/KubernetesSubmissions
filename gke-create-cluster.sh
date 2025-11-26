#!/bin/sh
gcloud container clusters create dwk-cluster --zone=europe-north1-b --cluster-version=1.32 --gateway-api=standard --disk-size=32 --num-nodes=3 --machine-type=e2-medium
