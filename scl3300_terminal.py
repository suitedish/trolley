#!/usr/bin/env python3
"""Terminal script to read the SCL3300‑D01 inclinometer and a rotary encoder on a BeagleBone Black.

Pinout (BBB → Sensor/Encoder):
- Inclinometer analog output → ADC channel 1 (AIN1) = /sys/bus/iio/devices/iio:device0/in_voltage1_raw
- Encoder CLK → GPIO1_13 (P8.11) → sysfs GPIO 525
- Encoder DT  → GPIO1_12 (P8.12) → sysfs GPIO 524
- Encoder SW  → GPIO0_26 (P8.14) → sysfs GPIO 634

The script polls the ADC and encoder every 200 ms and prints live values.
"""
import os, sys, time

# ---------- Configuration ----------
ADC_PATH_INCL = "/sys/bus/iio/devices/iio:device0/in_voltage1_raw"  # inclinometer (AIN1)
ENC_CLK_GPIO = 525   # P8_11 (GPIO1_13)
ENC_DT_GPIO = 524    # P8_12 (GPIO1_12)
ENC_SW_GPIO = 634    # P8_14 (GPIO0_26)
GPIO_BASE = "/sys/class/gpio"
POLL_INTERVAL = 0.2  # seconds
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
        voltage = raw * 1.8 / 4095  # 12‑bit ADC, 1.8 V reference
        return voltage
    except Exception:
        return None

def main():
    # Export GPIOs once
    for g in (ENC_CLK_GPIO, ENC_DT_GPIO, ENC_SW_GPIO):
        export_gpio(g)

    last_clk = read_gpio(ENC_CLK_GPIO)
    position = 0
    print("[INFO] Starting SCL3300 & Encoder monitor (Ctrl‑C to stop)")
    try:
        while True:
            # Inclinometer
            voltage = read_adc(ADC_PATH_INCL)
            if voltage is not None:
                angle = (voltage / 1.8) * 90 - 45  # map 0‑1.8 V → -45°…+45°
                print(f"Inclinometer: {voltage:.3f} V → {angle:.2f}°", end="  ")
            else:
                print("Inclinometer: error", end="  ")

            # Encoder
            clk = read_gpio(ENC_CLK_GPIO)
            dt = read_gpio(ENC_DT_GPIO)
            if clk != last_clk:
                if dt != clk:
                    position += 1
                else:
                    position -= 1
                print(f"Encoder pos: {position}", end="  ")
                last_clk = clk
            else:
                print("Encoder pos: unchanged", end="  ")

            # Switch (active‑low)
            sw = read_gpio(ENC_SW_GPIO)
            print(f"Switch: {'PRESSED' if sw == 0 else 'released'}")

            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
