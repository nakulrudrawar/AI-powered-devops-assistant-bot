# Runbook: Disk Space Full

## Cause

Disk space can become full because of application logs, temporary files, or old unused files.

## Steps

* [ ] Run `df -h` to check disk usage.
* [ ] Run `du -sh /var/log/*` to find large log directories.
* [ ] Remove unnecessary temporary or old log files.
* [ ] Restart the application if required.
* [ ] Verify disk usage again using `df -h`.
