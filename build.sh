#!/bin/bash
# Vercel build script

# Install Hugo
apt-get update
apt-get install -y hugo

# Build the site
hugo --environment production --destination public

echo "Hugo build completed successfully"
