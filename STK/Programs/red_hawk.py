import sys
import socket
import requests
import whois
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread

class ReconThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, url, action):
        super().__init__()
        self.url = url
        self.action = action

    def run(self):
        try:
            if self.action == "whois":
                domain = self.url.replace("http://", "").replace("https://", "").split('/')[0]
                w = whois.whois(domain)
                self.result_signal.emit(str(w))
            elif self.action == "headers":
                r = requests.get(self.url)
                headers = "\n".join([f"{k}: {v}" for k, v in r.headers.items()])
                self.result_signal.emit(headers)
            elif self.action == "portscan":
                domain = self.url.replace("http://", "").replace("https://", "").split('/')[0]
                ports = [21, 22, 80, 443, 8080]
                result = ""
                for port in ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        conn = sock.connect_ex((domain, port))
                        if conn == 0:
                            result += f"Port {port}: Open\n"
                        else:
                            result += f"Port {port}: Closed\n"
                        sock.close()
                    except Exception as e:
                        result += f"Port {port}: Error ({e})\n"
                self.result_signal.emit(result)
            else:
                self.result_signal.emit("Unknown action.")
        except Exception as e:
            self.result_signal.emit(f"Error: {e}")

class RedHawkGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RED_HAWK Python GUI")
        self.setGeometry(300, 200, 700, 500)
        self.initUI()

    def initUI(self):
        title = QLabel("<h2><font color='red'>RED_HAWK</font> - Recon GUI</h2>")
        target_label = QLabel("Target Site (URL):")
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("https://example.com")

        self.btn_whois = QPushButton("WHOIS Info")
        self.btn_headers = QPushButton("HTTP Headers")
        self.btn_portscan = QPushButton("Port Scan")

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.btn_whois.clicked.connect(lambda: self.recon('whois'))
        self.btn_headers.clicked.connect(lambda: self.recon('headers'))
        self.btn_portscan.clicked.connect(lambda: self.recon('portscan'))

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_whois)
        btn_layout.addWidget(self.btn_headers)
        btn_layout.addWidget(self.btn_portscan)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(target_label)
        layout.addWidget(self.target_input)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self.output)
        self.setLayout(layout)

    def recon(self, action):
        url = self.target_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a target URL.")
            return
        self.output.clear()
        self.output.append(f"Running {action} on {url} ...")
        self.thread = ReconThread(url, action)
        self.thread.result_signal.connect(self.show_result)
        self.thread.start()

    def show_result(self, result):
        self.output.append(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RedHawkGUI()
    window.show()
    sys.exit(app.exec_())
