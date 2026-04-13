#!/usr/bin/env python3
"""Simple PyQt5 GUI for the SCL3300-D01 inclinometer and a rotary encoder on a BeagleBone Black.

Only the inclinometer (ADC channel 1) and the rotary encoder are used. The GUI shows:
- Current inclination angle (°)
- Encoder position (steps)
- Switch state (pressed/released)

Pinout (same as the terminal script):
- Inclinometer analog output → ADC channel 1 (AIN1) = /sys/bus/iio/devices/iio:device0/in_voltage1_raw
- Encoder CLK → GPIO1_13 (P8.11) → sysfs GPIO number 525
- Encoder DT  → GPIO1_12 (P8.12) → sysfs GPIO number 524
- Encoder SW  → GPIO0_26 (P8.14) → sysfs GPIO number 634

Dependencies: PyQt5 (or PySide2), python3.
"""
import os, sys, time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer

# ---------- Configuration ----------
ADC_PATH_INCL = "/sys/bus/iio/devices/iio:device0/in_voltage1_raw"
ENC_CLK_GPIO = 525
ENC_DT_GPIO = 524
ENC_SW_GPIO = 634
GPIO_BASE = "/sys/class/gpio"
POLL_MS = 200  # update interval in ms
# -----------------------------------

def export_gpio(num):
    val_path = f"{GPIO_BASE}/gpio{num}/value"
    if not os.path.exists(val_path):
        try:
            with open(f"{GPIO_BASE}/export", "w") as f:
                f.write(str(num))
            with open(f"{GPIO_BASE}/gpio{num}/direction", "w") as f:
                f.write("in")
        except Exception as e:
            print(f"[GPIO] Export error for {num}: {e}")

def read_gpio(num):
    try:
        with open(f"{GPIO_BASE}/gpio{num}/value") as f:
            return int(f.read().strip())
    except Exception:
        return 0

def read_adc(path):
    try:
        with open(path) as f:
            raw = int(f.read().strip())
        voltage = raw * 1.8 / 4095
        return voltage
    except Exception:
        return None

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SCL3300 & Encoder Monitor")
        self.layout = QVBoxLayout()
        self.lbl_incl = QLabel("Inclinometer: -- °")
        self.lbl_encoder = QLabel("Encoder position: 0")
        self.lbl_sw = QLabel("Switch: released")
        self.layout.addWidget(self.lbl_incl)
        self.layout.addWidget(self.lbl_encoder)
        self.layout.addWidget(self.lbl_sw)
        self.setLayout(self.layout)

        # Export GPIOs once
        for g in (ENC_CLK_GPIO, ENC_DT_GPIO, ENC_SW_GPIO):
            export_gpio(g)
        self.last_clk = read_gpio(ENC_CLK_GPIO)
        self.position = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(POLL_MS)

    def update_values(self):
        # Inclinometer
        voltage = read_adc(ADC_PATH_INCL)
        if voltage is not None:
            angle = (voltage / 1.8) * 90 - 45
            self.lbl_incl.setText(f"Inclinometer: {angle:.2f} ° (V={voltage:.3f})")
        else:
            self.lbl_incl.setText("Inclinometer: error")

        # Encoder
        clk = read_gpio(ENC_CLK_GPIO)
        dt = read_gpio(ENC_DT_GPIO)
        if clk != self.last_clk:
            if dt != clk:
                self.position += 1
            else:
                self.position -= 1
            self.last_clk = clk
        self.lbl_encoder.setText(f"Encoder position: {self.position}")

        # Switch
        sw = read_gpio(ENC_SW_GPIO)
        self.lbl_sw.setText(f"Switch: {'PRESSED' if sw == 0 else 'released'}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
