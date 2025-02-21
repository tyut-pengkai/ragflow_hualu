#!/bin/bash

# Clear all proxy settings
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY socks_proxy SOCKS_PROXY
export no_proxy="*"
export NO_PROXY="*"

# Activate virtual environment and set PYTHONPATH
source .venv/bin/activate
export PYTHONPATH=$(pwd)

# Launch the service
bash docker/launch_backend_service.sh
