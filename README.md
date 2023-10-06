# DoorbellControl

## General Workflow process

## RPI imagin
1. install rpi lite (rpi imager)
2. enable ssh
3. setup wifi (keyboard, screen or via config if that works)
4. update pi
```
sudo apt update
sudo apt upgrade
```
## git setup

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
git config --global user.email "etitas@gmail.com"
git config --global user.name "Elyg"
```


## setup python

1. install python pip
```
sudo apt install python3-pip
pip --version
```
2. install python virtual env
```
sudo apt install python3-venv
```

## project setup
1. create folder structure
```
mkdir python
cd ./python
mkdir <project_name>
cd .<project_name>
touch main.py
```

2. create virtual env
```
python -m venv .venv
```
3. source virtual env
```
source .venv/bin/activate
```
4. git sync
```
git add --all
git commit -am "setup"
git push
```

## Begin to code