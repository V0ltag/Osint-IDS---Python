import sys
import matplotlib
matplotlib.use('Qt5Agg')  # Ensure the correct backend is set
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QHBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPalette
import threading
from ids_tool import capture_packets
from osint_tools import get_whois_info, ip_geolocation
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class IDSApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('IDS & OSINT Toolkit')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        
        # Setup UI components
        self.setup_ui()

        # Start packet capture after some time for demo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_ids)
        self.timer.start(3000)  # Start IDS capture after 3 seconds

        # Set up real-time packet count visualization
        self.fig, self.ax = plt.subplots()
        self.x_vals = []
        self.y_vals = []

        self.ani = animation.FuncAnimation(self.fig, self.update_graph, interval=1000)
        plt.show()

    def setup_ui(self):
        # Main Layout
        main_layout = QVBoxLayout()

        # IDS Section
        ids_button = QPushButton('Start IDS Monitoring')
        ids_button.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; border-radius: 5px;")
        ids_button.clicked.connect(self.start_ids)

        # OSINT Section
        osint_layout = QVBoxLayout()
        osint_label = QLabel('Enter Domain for WHOIS Lookup:')
        osint_label.setStyleSheet("font-size: 14px; color: #ffffff;")
        self.domain_entry = QLineEdit(self)
        self.domain_entry.setPlaceholderText('Example: example.com')
        self.domain_entry.setStyleSheet("background-color: #2e2e2e; color: white; padding: 5px; border-radius: 5px;")
        
        whois_button = QPushButton('WHOIS Lookup')
        whois_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        whois_button.clicked.connect(self.whois_lookup)
        
        # IP Geolocation Section
        ip_label = QLabel('Enter IP for Geolocation:')
        ip_label.setStyleSheet("font-size: 14px; color: #ffffff;")
        self.ip_entry = QLineEdit(self)
        self.ip_entry.setPlaceholderText('Example: 8.8.8.8')
        self.ip_entry.setStyleSheet("background-color: #2e2e2e; color: white; padding: 5px; border-radius: 5px;")
        
        ip_button = QPushButton('IP Geolocation')
        ip_button.setStyleSheet("background-color: #FF9800; color: white; padding: 10px; border-radius: 5px;")
        ip_button.clicked.connect(self.ip_lookup)

        # Result display area
        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("background-color: #2e2e2e; color: white; padding: 10px; border-radius: 5px;")

        # Adding widgets to layout
        main_layout.addWidget(ids_button)
        main_layout.addLayout(osint_layout)
        osint_layout.addWidget(osint_label)
        osint_layout.addWidget(self.domain_entry)
        osint_layout.addWidget(whois_button)
        main_layout.addWidget(ip_label)
        main_layout.addWidget(self.ip_entry)
        main_layout.addWidget(ip_button)
        main_layout.addWidget(self.result_text)

        self.setLayout(main_layout)

    def start_ids(self):
        self.result_text.append("Starting IDS Monitoring...\n")
        # Use threading to run the capture in the background
        ids_thread = threading.Thread(target=capture_packets)
        ids_thread.start()
        self.result_text.append("IDS Monitoring Started.\n")

    def whois_lookup(self):
        domain = self.domain_entry.text()
        result = get_whois_info(domain)
        self.result_text.append(f"WHOIS Result for {domain}:\n{result}\n")
        
    def ip_lookup(self):
        ip = self.ip_entry.text()
        result = ip_geolocation(ip)
        self.result_text.append(f"Geolocation for {ip}:\n{result}\n")

    def update_graph(self, i):
        self.x_vals.append(i)
        self.y_vals.append(i * 2)  # Replace with real IDS data
        
        self.ax.clear()
        self.ax.plot(self.x_vals, self.y_vals)
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("Packet Count")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IDSApp()
    window.show()
    sys.exit(app.exec_())
