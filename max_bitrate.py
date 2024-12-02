# max_bitrate.py
#
# Usage: python3 max_bitrate.py tx_w tx_gain_db freq_hz dist_km rx_gain_db n0_j bw_hz
# Calculates the maximum achievable bitrate using the Shannon-Hartley theorem.
# Assumptions:
#  - Transmitter-to-antenna line loss is -1 dB.
#  - Atmospheric loss is 0 dB.
#  - Received noise power is calculated using the noise spectral density N0 and bandwidth B.
#  - The speed of light is 2.99792458e8 m/s.
#
# Parameters:
#  tx_w: Transmitter power in watts.
#  tx_gain_db: Transmitter antenna gain in decibels (dB).
#  freq_hz: Carrier frequency in hertz.
#  dist_km: Distance between transmitter and receiver in kilometers.
#  rx_gain_db: Receiver antenna gain in decibels (dB).
#  n0_j: Noise spectral density in joules.
#  bw_hz: Bandwidth in hertz.
# Output:
#  Prints the maximum achievable bitrate in bits per second (bps) rounded down to the nearest integer.
#
# Written by Nick Davis
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0

# Import necessary modules
import math
import sys

# Constants
c = 2.99792458e8  # Speed of light in m/s

# Parse script arguments
if len(sys.argv) == 8:
    tx_w = float(sys.argv[1])       # Transmitter power in watts
    tx_gain_db = float(sys.argv[2]) # Transmitter antenna gain in dB
    freq_hz = float(sys.argv[3])    # Carrier frequency in Hz
    dist_km = float(sys.argv[4])    # Distance between transmitter and receiver in km
    rx_gain_db = float(sys.argv[5]) # Receiver antenna gain in dB
    n0_j = float(sys.argv[6])       # Noise spectral density in joules
    bw_hz = float(sys.argv[7])      # Bandwidth in Hz

    # Validate inputs
    if any(v <= 0 for v in [tx_w, freq_hz, dist_km, bw_hz, n0_j]):
        print("Error: All input parameters must be positive numbers.")
        exit()

    dist_m = dist_km * 1000
    fspl_db = 20 * math.log10(dist_m) + 20 * math.log10(freq_hz) - 20 * math.log10(c)
    pr_db = 10 * math.log10(tx_w) + tx_gain_db - 1 - fspl_db + rx_gain_db
    pr_w = 10**(pr_db / 10)
    pn_w = n0_j * bw_hz
    r_max = bw_hz * math.log2(1 + (pr_w / pn_w))

    print(math.floor(r_max)) # Rounded down to the nearest integer

else:
    print("Usage: python3 max_bitrate.py tx_w tx_gain_db freq_hz dist_km rx_gain_db n0_j bw_hz")
    exit()
