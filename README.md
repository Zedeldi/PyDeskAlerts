# PyDeskAlerts

[![GitHub license](https://img.shields.io/github/license/Zedeldi/PyDeskAlerts?style=flat-square)](https://github.com/Zedeldi/PyDeskAlerts/blob/master/LICENSE) [![GitHub last commit](https://img.shields.io/github/last-commit/Zedeldi/PyDeskAlerts?style=flat-square)](https://github.com/Zedeldi/PyDeskAlerts/commits) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

Synchronised desktop notifications, written in Python.

## Description

Send desktop notifications to multiple devices, specified by username.
Alerts are stored in an SQL database, and retrieved via an HTTP interface provided by `Flask`.
The client periodically checks for new alerts, and displays them using `plyer`.
Once a user has seen an alert, a reference is stored in the `seen` table.

This project was inspired by [DeskAlerts](https://www.alert-software.com/).

## Installation

1. Clone: `git clone https://github.com/Zedeldi/PyDeskAlerts.git`
2. Install dependencies: `pip3 install -r requirements.txt`
3. Run: `python3 -m deskalerts.[client|server]`

### Libraries:

Client:

 - [requests](https://pypi.org/project/requests/) - Get alerts from server
 - [plyer](https://pypi.org/project/plyer/) - Display notifications
 - [dbus-python](https://pypi.org/project/dbus-python/) - Dependency, Python binding for `dbus`

Server:

 - [Flask](https://pypi.org/project/Flask/) - HTTP interface

## Credits

 - Bootstrap = <https://getbootstrap.com/>
 - Icon = <https://feathericons.com>
