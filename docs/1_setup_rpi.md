## Setup raspberry pi
[Back to Table of contents](0_index.md)

#### 1. RPI image
1. install rpi lite (rpi imager)
2. enable ssh
3. setup wifi (keyboard, screen or via config if that works)
4. update pi
```
sudo apt update
sudo apt upgrade
```

#### 2. router set persistant ip
1. navigate to modem page
2. find ip of the rpi and set to be static

#### 3. git setup

1. install git
```
sudo apt install git
```
2. create ssh key local
```
ssh-keygen
<enter>
<enter>
<enter>

cat .pub file
```
3. paste the .pub contents to ssh key
4. initialize empty repo in github
5. git clone <repo>
6. config git
```
git config --global user.email "<user>@gmail.com"
git config --global user.name "<name>"
```
7. git sync cmd
```
git add --all && git commit -am "updated" && git push
```