# Project Service Setup
[Back to Table of contents](0_index.md)
___
Setting up services so they autostart when rpi reboots

1. create .service file
2. define rules and path to script to run inside
3. copy service file to /etc/systemd/system
   ```
   sudo cp ~/gits/DoorbellControl/scripts/doorbell_telegram.service .
   ```
4. start service
   ```
   sudo systemctl start doorbell_telegram.service
   ```
5. make sure that scripts have executable rights
   ```
   chmod 775 ./scripts/script.sh
   ```

## Other cmds

Restart service
```
sudo systemctl restart doorbell.service
sudo systemctl restart doorbell_telegram.service
sudo systemctl restart doorbell_calendar_sync.service
```

Stop services
```
sudo systemctl stop doorbell.service
sudo systemctl stop doorbell_telegram.service
sudo systemctl stop doorbell_calendar_sync.service
```
Start services
```
sudo systemctl start doorbell.service
sudo systemctl start doorbell_telegram.service
sudo systemctl start doorbell_calendar_sync.service
```
See logs of services
```
journalctl -u doorbell.service -f
journalctl -u doorbell_telegram.service -f
journalctl -u doorbell_calendar_sync.service -f
```

Restart all services
```
sudo systemctl restart doorbell.service && sudo systemctl restart doorbell_telegram.service && sudo systemctl restart doorbell_calendar_sync.service
```

stop all services
```
sudo systemctl stop doorbell.service && sudo systemctl stop doorbell_telegram.service && sudo systemctl stop doorbell_calendar_sync.service
```

start all services
```
sudo systemctl start doorbell.service && sudo systemctl start doorbell_telegram.service && sudo systemctl start doorbell_calendar_sync.service
```