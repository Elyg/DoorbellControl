# Project Folder Structure

[Back to Table of contents](0_index.md)

### The folder structure to be used

Generic examples
```
gits
└── ProjectName
    ├── docs
    │   ├── 0_index.md
    │   ├── images
    │   │   └── images.png
    ├── python
    │   └── projectname
    │       ├── config
    │       │   └── config.json
    │       └── main.py
    ├── README.md
    ├── requirements.txt
    ├── scripts
    │   └── script.sh
    └── tests
        └── test.py
```
Final Example
```
gits
└── DoorbellControl
    ├── docs
    │   ├── 0_index.md
    │   ├── 1_step.md
    │   ├── 2_1_sub_step.md
    │   ├── images
    │   │   └── images.png
    ├── python
    │   └── doorbellcontrol
    │       ├── config
    │       │   ├── credentials.json
    │       │   ├── secret.json
    │       │   └── token.json
    │       ├── database.py
    │       ├── google_calendar.py
    │       ├── google_calendar_sync.py
    │       ├── main.py
    │       ├── telegram_basic.py
    │       └── telegram_bot.py
    ├── README.md
    ├── requirements.txt
    ├── scripts
    │   ├── doorbell_calendar_sync.service
    │   ├── doorbell.service
    │   ├── doorbell.sh
    │   ├── doorbell_telegram.service
    │   ├── google_calendar_sync.sh
    │   └── telegram_bot.sh
    └── tests
        └── test.py
```

