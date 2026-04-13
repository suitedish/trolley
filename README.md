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
