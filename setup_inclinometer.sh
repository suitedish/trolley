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
