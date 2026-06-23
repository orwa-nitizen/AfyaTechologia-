#!/usr/bin/env bash
set -euo pipefail

IMAGE=afyatech:latest

docker build -t ${IMAGE} .
echo "Built ${IMAGE}. Push and deploy per your environment (this script is a placeholder)."
