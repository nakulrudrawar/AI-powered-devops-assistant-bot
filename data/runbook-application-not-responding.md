# Runbook: Application Not Responding

## Cause

The application may be stopped, crashed, overloaded, or unable to connect to required services.

## Steps

* [ ] Check whether the application process is running.
* [ ] Check application logs for errors.
* [ ] Verify the application port using `ss -tulpn`.
* [ ] Restart the application service if required.
* [ ] Test the application using `curl http://localhost:<port>`.
