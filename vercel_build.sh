#!/bin/bash
echo "=== VERCEL BUILD STARTED ===" > /tmp/vercel_build.log
echo "Date: $(date)" >> /tmp/vercel_build.log
echo "PWD: $(pwd)" >> /tmp/vercel_build.log

echo "=== LISTING FILES ===" >> /tmp/vercel_build.log
ls -la >> /tmp/vercel_build.log

echo "=== CHECKING THEMES ===" >> /tmp/vercel_build.log
if [ -d "themes/dream" ]; then
    echo "Theme exists" >> /tmp/vercel_build.log
    ls themes/dream/ | head -5 >> /tmp/vercel_build.log
else
    echo "Theme NOT found, initializing..." >> /tmp/vercel_build.log
    git submodule update --init --recursive >> /tmp/vercel_build.log 2>&1
fi

echo "=== INSTALLING HUGO ===" >> /tmp/vercel_build.log
apt-get update >> /tmp/vercel_build.log 2>&1
apt-get install -y hugo >> /tmp/vercel_build.log 2>&1

echo "=== RUNNING HUGO ===" >> /tmp/vercel_build.log
hugo --environment production >> /tmp/vercel_build.log 2>&1

echo "=== DONE ===" >> /tmp/vercel_build.log
cat /tmp/vercel_build.log
