#!/bin/sh

if [ "$#" -ne 1 ]; then
  echo "Usage $0 BASENAME"
  exit 1
fi

rm -rf .terraform
terraform init -backend-config="bucket=$1-terraform" -backend-config="key=ssl.state"
