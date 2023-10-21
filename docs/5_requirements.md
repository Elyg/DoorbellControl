## requirements
[Back to Table of contents](0_index.md)
___
install pip
```
sudo apt install python3-pip
```
install venv
```
sudo apt install python3-venv
```

### after sourceing .venv

#### install gpiozero 
```
sudo apt install python3-gpiozero
```
___

for rpi pins
```
pip install gpiozero
```

for google calendar
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

for firebase
```
pip install firabase_admin
```

for timezones
```
pip install pytz
pip install tzlocal
```

for telegram
```
pip install python-telegram-bot --upgrade
```

### other info
___
```
secret.json - for firebase
credentials.sjon - for google calendar
toekn.json - for google calendar
```


### How to run project
___
```
sudo systemctl start doorbell.service
sudo systemctl start doorbell_telegram.service
```

