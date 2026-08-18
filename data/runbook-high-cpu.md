# Runbook: High EC2 CPU Usage

## Cause

High CPU usage can happen because of heavy application traffic, background processes, or a resource-intensive process.

## Steps

* [ ] Check CPU utilization in AWS CloudWatch.
* [ ] Connect to the EC2 instance using SSH.
* [ ] Run `top` or `htop` to find the process using high CPU.
* [ ] Stop or restart the problematic process if required.
* [ ] If CPU remains high, consider scaling up the instance.
