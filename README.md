# DoorbellControl

## How it all works

1. RPI is installed above the bell chime in a plastic housing and is powered over POE ethernet cable
2. RPI is setup and wired based on the circuit diagram
   1. Bell chime ring button is wired to the rpi
   2. rpi is wired to a relay
   4. Once the button is pressed rpi is activating the relay
   5. A telegram notification is sent
3. Relay activation is determined by settings defined by user
4. User changes settings via telegram chat bot
5. User settings gets saved to firecloud realtime database
   1. mode: on/off - to ring chime or not
   2. phrase: what telegram message says when bell rings
   3. calendar: on/off - whether block the ring chime based on a calendar schedule
   4. events: the calendar events when to block the door chime
   
* RPI is running 3 services
    1. doorbell.service - for relay activation
    2. doorbell_telegram.service - for telegram bot communication
    3. doorbell_calendar_sync.service - for calendar sync (9:00 and 23:00 everyday runs a sync between 2 calendars and saves the events to firecloud db)

## Project Workflow/Setup

[Project Setup Table of Contents](docs/0_index.md)