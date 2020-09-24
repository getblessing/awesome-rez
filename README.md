# awesome-rez

Better use Python 3.7

### Deploy

```
git clone https://github.com/getblessing/awesome-rez.git
cd awesome-rez
```

#### Install Rez

This will install Rez from [getblessing/rez](https://github.com/getblessing/rez). Not much difference between latest official Rez ([nerdvegas/rez](https://github.com/nerdvegas/rez)), just a few changes for fixing some issues that I encountered on Windows and not yet been merged.

```shell
python ./install.py
```

#### Setup `awesome-rez/rezconfig.py`

This is optional.

```batch
:: rezin.bat
:: For entering Rez
@echo off
set PATH=%YOUR_REZ_LOCATION%\Scripts\rez;%PATH%
set REZ_CONFIG_FILE=%YOUR_PATH_TO%\awesome-rez\rezconfig.py
rez --version
```

#### Install packages

This will install package `ozark` from [getblessing/rez-ozark](https://github.com/getblessing/rez-ozark), and all the required packages.

```shell
python ./deploy.py ozark
```

Essential packages will also be installed: `os`, `arch`.. and `rez`.

### Topics

* [getblessing-base](https://github.com/topics/getblessing-base)
* [getblessing-util](https://github.com/topics/getblessing-util)
* [getblessing-pipeline](https://github.com/topics/getblessing-pipeline)
* [getblessing-usd](https://github.com/topics/getblessing-usd)
* [getblessing-dcc](https://github.com/topics/getblessing-dcc)
* [getblessing-ide](https://github.com/topics/getblessing-ide)
* [getblessing-pip](https://github.com/topics/getblessing-pip)
* [getblessing-cxx](https://github.com/topics/getblessing-cxx)
