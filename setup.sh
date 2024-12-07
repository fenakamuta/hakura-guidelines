#!/usr/bin/env bash

mkdir -p ~/.streamlit
echo "[general]
email = \"fernandonakamuta@gmail.com\"
" > ~/.streamlit/credentials.toml

echo "[server]
headless = true
enableCORS=false
port = $PORT
" > ~/.streamlit/config.toml

# Non-interactive guardrails configuration
guardrails hub install hub://tryolabs/restricttotopic