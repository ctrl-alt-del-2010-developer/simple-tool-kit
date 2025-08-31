import sys
import socket
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QListWidget, QLabel
)
from PyQt5.QtCore import Qt

class PortScannerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Port Scanner")
        self.setGeometry(300, 300, 400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Enter IP Address:")
        layout.addWidget(self.label)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("e.g. 192.168.1.1")
        layout.addWidget(self.ip_input)

        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        self.setLayout(layout)

    def start_scan(self):
        ip = self.ip_input.text().strip()
        if not ip:
            self.result_list.addItem("Please enter a valid IP address.")
            return

        self.result_list.clear()
        self.result_list.addItem(f"Scanning {ip}...")

        scan_thread = threading.Thread(target=self.scan_ports, args=(ip,))
        scan_thread.start()

    def scan_ports(self, ip):
        open_ports = []
        for port in range(1, 1025):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        open_ports.append(port)
                        self.result_list.addItem(f"Port {port} is open.")
            except socket.error:
                self.result_list.addItem(f"Error: Could not connect to {ip}.")
                break

        if not open_ports:
            self.result_list.addItem("No open ports found.")
        else:
            self.result_list.addItem("Scan complete.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PortScannerApp()
    window.show()
    sys.exit(app.exec_())
