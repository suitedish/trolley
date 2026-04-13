#!/usr/bin/env python3
"""Terminal script to read the SCL3300‑D01 inclinometer on a BeagleBone Black.

Pinout (BBB → SCL3300 Sensor):
- J1 Pin 1 (AVSS/GND)   → P9-1 (GND)
- J1 Pin 2 (AVDD)       → P9-33 (3.3V)
- J1 Pin 3 (VOUT)       → P9-40 (AIN1) -> /sys/bus/iio/devices/iio:device0/in_voltage1_raw
- J1 Pin 4 (DVSS)       → P9-1 (GND)
- J1 Pin 5 (DVDD)       → P9-33 (3.3V)

The script polls the ADC every 200 ms and prints live inclination values.
"""
import sys, time

# ---------- Configuration ----------
ADC_PATH_INCL = "/sys/bus/iio/devices/iio:device0/in_voltage1_raw"  # inclinometer (AIN1)
POLL_INTERVAL = 0.2  # seconds
# -----------------------------------

def read_adc(path):
    """Read the raw ADC value and convert to voltage (1.8 V reference)."""
    try:
        with open(path) as f:
            raw = int(f.read().strip())
        voltage = raw * 1.8 / 4095  # 12‑bit ADC, 1.8 V reference
        return voltage
    except Exception:
        return None

def main():
    print("[INFO] Starting SCL3300 Inclinometer monitor (Ctrl‑C to stop)")
    try:
        while True:
            # ---- Inclinometer ----
            voltage = read_adc(ADC_PATH_INCL)
            if voltage is not None:
                # SCL3300: 0 V = -45°, 1.8 V = +45° (approx., based on specific model scaling setup)
                # Ensure we handle edge cases nicely
                voltage = max(0.0, min(1.8, voltage))
                angle = (voltage / 1.8) * 90 - 45
                print(f"Inclinometer: {voltage:.3f} V → {angle:.2f}°", end="\r")
            else:
                print("Inclinometer: error (cannot read ADC)", end="\r")

            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
