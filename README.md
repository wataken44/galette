# galette
> home gateway build playbooks 

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Features](#features)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

## General info

Ansible playbooks and related script to build Linux router for PPPoE providers in Japan.

日本のPPPoEプロバイダ用のLinuxルータを構築するためのansible playbookと関連スクリプト。


## Setup

### prerequisites

Hardware
* 2 NICs (for WAN and LAN)

OS
* Debian Testing (developer use this)
    * Maybe this project works with Debian Stable, but not tested... 

### installation

install least packages if not installed

```
# apt install git-core ansible sudo openssh-server
```

clone this repository

```
$ git clone 'https://github.com/wataken44/galette.git'
```

### check sudo

check that sudo REQUESTS PASSWORD and command succeed

```
$ sudo hostname
[sudo] password for user:
router
```


### edit and run

check basic ansible succeed

```
$ command/show_hostname.py
...
BECOME password:
...
127.0.0.1                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

install packages

```
$ command/install_packages.py
```

edit vars

configure


## Features

features:

* feature 1
* feature 2
* feature 3

todos:

* todo 1
* todo 2

## Acknowledgements

* credits
* inspired by

## Contact

* [wataken44(twitter)](https://twitter.com/wataken44)
* [wataken44(github)](https://github.com/wataken44/)
