![Device](https://img.shields.io/badge/Device-Ricoh%20Printer-red.svg)   
![Protocol](https://img.shields.io/badge/Protocol-SNMP-blue.svg)   
![Python](https://img.shields.io/badge/python-3.6%2B-blue)

# 🖨️ HPZ Ricoh Printer Monitor
A Python application to monitor Ricoh printers via SNMP and send monthly reports via email.

<img width="864" height="487" alt="image" src="https://github.com/user-attachments/assets/ef24db3d-9cf2-433f-a635-7d5aa793d49a" />


## 📌 Descrição

- **Printer Monitoring**: Collects toner levels, page counts, and device status via SNMP
- **Automated Reporting**: Sends formatted HTML email reports with printer statistics
- **Easy Management**: Simple interface to add/remove printers and configure monitoring
- **Scheduling**: Option to run reports immediately or set up monthly automated reports

## Features

- 📊 SNMP monitoring of Ricoh printers
- 🖨️ Collects toner levels, page counters, and status information
- ✉️ Generates HTML email reports
- 🖥️ Simple GUI for managing printer configurations
- ⏱️ Option to run reports immediately or schedule monthly reports

## Requirements

- Python 3.6+
- Windows OS (for scheduled tasks)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/S4W1L/Ricoh-IMC-Monitor.git
   cd hpz-printer-monitor
   
Install Dependenciess:

pip install -r requirements.txt

## 📧 Email Configuration
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


## 📆 Scheduled Task
The application creates a Windows task that:

Runs monthly on the 1st

At 8:00 AM


### Manual task creation:
```
schtasks /Create /SC MONTHLY /D 1 /TN "HPZ_Ricoh_Report" /TR "run_printer_monitor.bat" /ST 08:00 /F
```

Executes the report automatically



### Light Themes:
```
cosmo
flatly
journal
litera
lumen
minty
pulse
sandstone
united
yeti
morph
simplex
cerulean
```
## Dark Themes:
```
darkly
cyborg
superhero
solar
```



