SCL3300‑D01   BBB (P9 header)                Notes
--------------------------------------------------------------
J1 Pin 1  →  AVSS  →  GND (P9‑1)               Analog ground
J1 Pin 2  →  AVDD  →  3.3 V (P9‑33)            Analog supply
J1 Pin 3  →  VOUT  →  AIN1 (P9‑40)            Analog tilt voltage (read by ADC)
J1 Pin 4  →  DVSS  →  GND (P9‑1)               Digital ground (tied to AVSS)
J1 Pin 5  →  DVDD  →  3.3 V (P9‑33)            Digital supply (tied to AVDD)
J1 Pin 6‑8 →  NC    →  –                       Not used
J2 Pin 1  →  CSB   →  SPI0_CS0 (P9‑17)        Chip‑select (active‑low) – only if you use SPI mode
J2 Pin 2  →  SCK   →  SPI0_SCLK (P9‑22)       Clock
J2 Pin 3  →  MOSI  →  SPI0_D1 (P9‑18)         Master‑out (commands)
J2 Pin 4  →  MISO  →  SPI0_D0 (P9‑21)         Master‑in (data)
J2 Pin 5‑8 →  NC    →  –                       Not used

chmod +x setup_inclinometer.sh

#!/usr/bin/env bash
set -e

# 1. System packages
sudo apt-get update
sudo apt-get install -y build-essential python3-dev python3-pip \
    libgpiod2 gpiod i2c-tools libi2c-dev spi-tools libspi-dev git

# 2. Load ADC overlay permanently
echo "am335x_adc" | sudo tee /etc/modules-load.d/adc.conf
sudo modprobe ti_am335x_adc

# 3. (Optional) Enable SPI0 overlay – uncomment if you need SPI
# echo "dtoverlay=spi0" | sudo tee -a /boot/uEnv.txt
# sudo reboot   # reboot required for overlay to take effect

# 4. Python requirements
pip3 install --upgrade pip
pip3 install -r "$(dirname "$0")/../requirements.txt"

echo "✅ All dependencies installed. You can now run:"
echo "   python3 ~/Desktop/antiG/karlo/scl3300_terminal.py"
echo "   python3 ~/Desktop/antiG/karlo/integrated_rail_scl3300_gui.py"
