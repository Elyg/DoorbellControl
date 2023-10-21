# Install pip and venv

[Back to Table of contents](0_index.md)
___

Basics on pip and venv

#### 1. install pip
```
sudo apt install pip
```

#### 2. install venv
```
pip install virtualenv
```

# How to use pip and venv

### virtualenv

#### 1. Create virtualenv
```
cd ~/gits/<project_name> && python -m venv ./.venv
```
#### Activate virtualenv (linux)
```
source ./.venv/bin/activate 
```
#### Activate virtualenv (windows)
```
.\.vnev\Scripts\activate
```
___
### Pip usage (all done from activated .venv)

#### 1. install python modules
```
pip install <module name>
```

#### 2. to freeze pip installs from .venv into txt file
```
pip freeze -l > requirements.txt 
```

#### 3. to install requirements
```
pip install -r requirements.txt
```

### Pipreq alternative (all done from activated .venv)

#### 1. install pipreqs
```
pip install pipreqs
```
#### 2. generate pipreqs requirements
```
pipreqs ./python --savepath ./requirements.txt  --force
```