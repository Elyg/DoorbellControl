# Project Service Start

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

other cmd
```
sudo systemctl restart doorbell.service
sudo systemctl restart doorbell_telegram.service
sudo systemctl restart doorbell_calendar_sync.service

sudo systemctl stop doorbell.service
sudo systemctl stop doorbell_telegram.service
sudo systemctl stop doorbell_calendar_sync.service

sudo systemctl start doorbell.service
sudo systemctl start doorbell_telegram.service
sudo systemctl start doorbell_calendar_sync.service

journalctl -u doorbell.service -f
journalctl -u doorbell_telegram.service -f
journalctl -u doorbell_calendar_sync.service -f
```
