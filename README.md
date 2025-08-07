![Device](https://img.shields.io/badge/Device-Ricoh%20Printer-red.svg)
![Protocol](https://img.shields.io/badge/Protocol-SNMP-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

# 🖨️ HPZ Ricoh Printer Monitor

A Python GUI application for monitoring Ricoh printers via SNMP with automated email reporting.

<img src="https://github.com/user-attachments/assets/ef24db3d-9cf2-433f-a635-7d5aa793d49a" alt="Application Screenshot">

## 📋 Table of Contents
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Email](#-Email).
- [Scheduled](#-Scheduled).
- [Themes](#-Themes)

## ✨ Features

<div align="left">

| Feature Category | Details |
|-----------------|---------|
| **Monitoring** | Toner levels, Page counts, Device status |
| **Reporting** | HTML email reports, Scheduled delivery |
| **Management** | Add/remove printers, Configure alerts |
| **Automation** | Monthly reports, Immediate execution |

</div>

## 📦 Requirements

- Python 3.6+
- Windows OS (for scheduled tasks)
- Network access to printers
- SNMP enabled on devices

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/S4W1L/Ricoh-IMC-Monitor.git

cd Ricoh-IMC-Monitor
   
Install Dependenciess:

pip install -r requirements.txt
```
## 📧 Email

```
EMAIL_CONFIG = {
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "username": "seu-email@gmail.com",
  "password": "sua-senha",
  "from": "seu-email@gmail.com",
  "to": "suporte@empresa.com"
}
```
Note: For gmail needs to activate double authentication and create a app password..


## 📆 Scheduled
The application creates a Windows task that:

Runs monthly on the 1st

At 8:00 AM


### Manual task creation:
```
schtasks /Create /SC MONTHLY /D 1 /TN "HPZ_Ricoh_Report" /TR "run_printer_monitor.bat" /ST 08:00 /F
```

Executes the report automatically

## Themes

<div align="left">

| Light | Dark |
|-----------------|---------|
| cosmo | darkly |
| flatly | cyborg |
| journal | superhero |
| litera | solar |
| lumen |  |
| minty |  |
| pulse |  |
| sandstone |  |
| united |  |
| yeti |  |
| morph |  |
| simplex |  |
| cerulean |  |

</div>


