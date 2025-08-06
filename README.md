![Device](https://img.shields.io/badge/Device-Ricoh%20Printer-red.svg)   
![Protocol](https://img.shields.io/badge/Protocol-SNMP-blue.svg)   

# 🖨️ HPZ Ricoh Printer Monitor
Monitorize e gere impressoras Ricoh via SNMP com uma interface gráfica moderna em Python.

## 📌 Descrição
O HPZ Ricoh Printer Monitor é uma aplicação desktop desenvolvida em Python que permite monitorizar impressoras Ricoh compatíveis via SNMP. Através de uma interface gráfica intuitiva, é possível:

Adicionar e remover impressoras por IP e comunidade SNMP.

Visualizar informações como modelo, número de série, firmware e níveis de toner.

Gerar relatórios mensais automáticos com contadores de impressão.

Enviar relatórios por e-mail automaticamente.

Agendar tarefas no Windows para execução periódica.

## ⚙️ Funcionalidades
Interface gráfica moderna com o tema ttkbootstrap.

Gestão de impressoras: adicione, remova e visualize impressoras.

Relatórios automáticos: contadores de impressão por cor e tipo.

Envio de e-mails: relatórios enviados automaticamente para o suporte.

Agendamento de tarefas: configure execução mensal automática no Windows.

## 🛠️ Pré-requisitos
Python 3.6 ou superior

Bibliotecas Python:

ttkbootstrap

pysnmp

smtplib

json

os

datetime

threading

email.mime

Conta de e-mail (por exemplo, Gmail) para envio de relatórios

## 📥 Instalação
Clone o repositório:

bash
Copiar
Editar
```
git clone https://github.com/SAW1L/HPZ-Ricoh-Monitor.git
cd HPZ-Ricoh-Monitor
```
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Execute a aplicação:

bash
Copiar
Editar
python printer_monitor.py

## 📧 Configuração de E-mail
No arquivo printer_monitor.py, configure as credenciais de e-mail para envio de relatórios:

python
Copiar
Editar
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
Nota: Para contas Gmail, pode ser necessário gerar uma senha de aplicativo nas configurações de segurança.

## 📆 Agendamento de Tarefas no Windows
A aplicação permite agendar a execução mensal automática utilizando o agendador de tarefas do Windows:

Execute a aplicação e clique em "Agendar".

A tarefa será configurada para execução no dia 1 de cada mês às 08:00.

## 🖌️ Temas Disponíveis
O ttkbootstrap oferece diversos temas para personalizar a aparência da aplicação. Alguns dos temas disponíveis incluem:

Temas claros:

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

Temas escuros:

darkly

cyborg

superhero

solar

