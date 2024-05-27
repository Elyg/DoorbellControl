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
```
Stop services
```
sudo systemctl stop doorbell.service
```
Start services
```
sudo systemctl start doorbell.service
```
See logs of services
```
journalctl -u doorbell.service -f
```

show colored logs
```
journalctl -u doorbell.service -f -o cat
```

show running services
```
systemctl --type=service --state=running
```

