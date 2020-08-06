#!/usr/bin/env bash
set -e
kubectl apply -f kubernetes/postgres.yml
kubectl apply -f kubernetes/web.yml