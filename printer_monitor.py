# printer_monitor.py

import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Treeview, Entry, Button, Label, Frame
from tkinter import messagebox
import json
import os
import datetime
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pysnmp.hlapi import *

CONFIG_FILE = 'printers_config.json'

OIDS = {
    "Model Name": "1.3.6.1.4.1.367.3.2.1.1.1.1.0",
    "Serial Number": "1.3.6.1.4.1.367.3.2.1.2.1.4.0",
    "Firmware": "1.3.6.1.4.1.367.3.2.1.1.1.2.0",
    "Contador": "1.3.6.1.4.1.367.3.2.1.2.19.1.0",
    "Total Preto": "",
    "Total Cor": "",
    "Black Toner Level %": "1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.1",
    "Cyan Toner Level %": "1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.2",
    "Magenta Toner Level %": "1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.3",
    "Yellow Toner Level %": "1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.4",
    "Error Status": "1.3.6.1.4.1.367.3.2.1.2.2.13.0",
    "Cor": "1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.13",
    "Preto": "1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.14",
    "Duas Cores": "1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.10"
}

EMAIL_CONFIG = {
    "smtp_server": "your.smtp.server",
    "smtp_port": 587,
    "username": "your@email.com",
    "password": "your-app-password",
    "from": "your@email.com",
    "to": "recipient1@email.com"
}

def load_config():
    """Carrega a configuração das impressoras do ficheiro JSON."""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump([], f)
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(data):
    """Guarda a configuração das impressoras no ficheiro JSON."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def snmp_get(ip, community, oid):
    """Consulta SNMP e retorna o valor do OID."""
    if not oid:
        return "N/A"
    try:
        iterator = getCmd(SnmpEngine(),
                          CommunityData(community),
                          UdpTransportTarget((ip, 161), timeout=2.0, retries=3),
                          ContextData(),
                          ObjectType(ObjectIdentity(oid)))
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication or errorStatus:
            return "Unavailable"
        else:
            return str(varBinds[0][1])
    except Exception:
        return "Unavailable"

def collect_printer_data(printers):
    """Recolhe os dados SNMP de todas as impressoras configuradas."""
    data = []
    for printer in printers:
        ip = printer['IP']
        community = printer['Community']
        result = {'IP Address': ip}
        for key, oid in OIDS.items():
            result[key] = snmp_get(ip, community, oid)
        model = result.get("Model Name", "Unreachable")
        result['Printer Name'] = model if model != "Unavailable" else f"Unreachable ({ip})"
        data.append(result)
    return data

def send_email(printers_data):
    """Envia um email com o relatório dos contadores das impressoras."""
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    subject = f"Ricoh Contadores - {now}"
    html = f"<h2>HPZ Ricoh - {now}</h2>"

    for p in printers_data:
        html += f"<h3>{p['Printer Name']} ({p['IP Address']})</h3>"

        # Tenta converter valores em inteiros para cálculo
        try:
            preto = int(p.get("Preto", "0"))
        except:
            preto = 0

        try:
            cor = int(p.get("Cor", "0"))
        except:
            cor = 0

        try:
            duas_cores = int(p.get("Duas Cores", "0"))
        except:
            duas_cores = 0

        total_preto = max(preto - duas_cores, 0)
        total_cor = cor + duas_cores

        for field in OIDS.keys():
            if field == "Total Preto":
                value = total_preto
            elif field == "Total Cor":
                value = total_cor
            else:
                value = p.get(field, "Unavailable")
            html += f"<p><b>{field}:</b> {value}</p>"

        html += "<hr>"

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = EMAIL_CONFIG['from']
    msg['To'] = EMAIL_CONFIG['to']

    part = MIMEText(html, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

class PrinterMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HPZ - Ricoh IMC")
        self.root.geometry("540x300")
        self.root.resizable(False, False)

        # Estilo Bootstrap
        self.style = Style(theme="journal") #journal 
        self.root.configure(bg=self.style.colors.bg)

        self.data = load_config()

        # Frame principal
        main_frame = Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Treeview para mostrar IPs e comunidades
        self.tree = Treeview(main_frame,
                             columns=("IP", "Community"),
                             show="headings",
                             height=10,
                             bootstyle="info")
        self.tree.heading("IP", text="Endereço IP")
        self.tree.heading("Community", text="Community")
        self.tree.column("IP", width=250)
        self.tree.column("Community", width=250)
        self.tree.pack(pady=(10, 5), fill="x")

        self.load_tree()

        # Botões para interações
        btn_frame = Frame(main_frame)
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Adicionar", command=self.add_entry,
               bootstyle="success-outline", width=12).grid(row=0, column=0, padx=5)
        Button(btn_frame, text="Remover", command=self.remove_entry,
               bootstyle="danger-outline", width=12).grid(row=0, column=1, padx=5)
        Button(btn_frame, text="Executar", command=self.run_now,
               bootstyle="info-outline", width=12).grid(row=0, column=2, padx=5)
        Button(btn_frame, text="Agendar", command=self.schedule_task,
               bootstyle="primary-outline", width=12).grid(row=0, column=3, padx=5)

    def load_tree(self):
        """Carrega a lista de impressoras no Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for entry in self.data:
            self.tree.insert('', 'end', values=(entry['IP'], entry['Community']))

    def add_entry(self):
        """Popup para adicionar uma nova impressora."""
        def save_and_close():
            ip = ip_entry.get().strip()
            community = community_entry.get().strip() or "public"
            if ip:
                self.data.append({'IP': ip, 'Community': community})
                save_config(self.data)
                self.load_tree()
                popup.destroy()
            else:
                messagebox.showerror("Erro", "O IP é obrigatório.")

        popup = tk.Toplevel(self.root)
        popup.title("Adicionar Impressora")
        popup.geometry("400x200")
        popup.configure(bg=self.style.colors.bg)

        Label(popup, text="Endereço IP:", bootstyle="info").pack(pady=(10, 0))
        ip_entry = Entry(popup, width=40)
        ip_entry.pack(pady=5)

        Label(popup, text="Community (default: public):", bootstyle="info").pack(pady=(5, 0))
        community_entry = Entry(popup, width=40)
        community_entry.pack(pady=5)

        Button(popup, text="Guardar", command=save_and_close,
               bootstyle="success").pack(pady=15)

        popup.grab_set()
        popup.transient(self.root)

    def remove_entry(self):
        """Remove as impressoras selecionadas da lista."""
        selected = self.tree.selection()
        if not selected:
            return
        for item in selected:
            values = self.tree.item(item, 'values')
            self.data = [d for d in self.data if d['IP'] != values[0]]
        save_config(self.data)
        self.load_tree()

    def run_now(self):
        """Executa a recolha e envio do relatório imediatamente."""
        def task():
            try:
                result = collect_printer_data(self.data)
                success = send_email(result)
                msg = "Relatório enviado com sucesso!" if success else "Falha ao enviar o email!"
                self.root.after(0, lambda: messagebox.showinfo("Execução", msg))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Erro", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def schedule_task(self):
        """Cria ou atualiza uma tarefa agendada mensal no Windows para executar o script."""
        # Caminho absoluto do script Python atual
        python_exe = os.sys.executable
        script_path = os.path.abspath(__file__)
        bat_path = os.path.abspath("run_printer_monitor.bat")

        # Cria/reescreve o ficheiro .bat que executa o script com python
        with open(bat_path, 'w') as f:
            f.write(f'@echo off\n"{python_exe}" "{script_path}"\n')

        # Comando para criar ou substituir a tarefa agendada no Windows
        # Agendamento: mensal, dia 1, às 08:00
        task_name = "HPZ_Ricoh_Report"
        cmd = f'schtasks /Create /SC MONTHLY /D 1 /TN "{task_name}" /TR "{bat_path}" /ST 08:00 /F'

        # Executa o comando

        os.system(cmd)
