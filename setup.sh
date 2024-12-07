#!/usr/bin/env bash

# Configure Streamlit
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"fernandonakamuta@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

# Install the Guardrails validator from the hub
guardrails configure
guardrails hub install hub://tryolabs/restricttotopic