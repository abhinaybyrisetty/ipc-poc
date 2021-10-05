# ipc-poc
Micro Services to monitor device registrations and notify the changes

## Run the notifications service first in a separate tab using below command
`python notify.py`

## Run monitoring service using below command
`python monitor.py`


### Limitations:
1. When the changes are too quick, it might not be able to detect the changes
2. Addition of entries other than ssid, snr and channel will not be identified
