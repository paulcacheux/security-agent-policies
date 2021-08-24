#!/usr/bin/env bash

# auditd
sudo apt-get install auditd
cat ./testdata/audit_docker.rules | sudo tee /etc/audit/rules.d/docker.rules
sudo systemctl restart auditd

# Docker
cat ./testdata/daemon_config.json | sudo tee /etc/docker/daemon.json
echo "DOCKER_CONTENT_TRUST=1" >> $GITHUB_ENV
sudo systemctl restart docker
