# Copyright (C) 2019 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

import time

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

import adi


def measure_phase(chan0, chan1):
    errorV = np.angle(chan0 * np.conj(chan1)) * 180 / np.pi
    error = np.mean(errorV)
    return error


# Plot config
plot_time_domain = False

# Create radio
sdr = adi.adrv9009_zu11eg(uri="ip:192.168.86.57")
sdr._rxadc.set_kernel_buffers_count(1)

# Configure properties
sdr.rx_enabled_channels = [0, 1, 2, 3]
sdr.tx_enabled_channels = [0, 1]
sdr.trx_lo = 2000000000
sdr.trx_lo_chip_b = 2000000000
sdr.tx_hardwaregain_chan0 = -10
sdr.tx_hardwaregain_chan1 = -10
sdr.tx_hardwaregain_chan0_chip_b = -10
sdr.tx_hardwaregain_chan1_chip_b = -10
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.gain_control_mode_chan0_chip_b = "slow_attack"
sdr.gain_control_mode_chan1_chip_b = "slow_attack"
sdr.rx_buffer_size = 2 ** 17

# Read properties
print("TRX LO %s" % (sdr.trx_lo))
print("TRX LO %s" % (sdr.trx_lo_chip_b))

sdr.dds_single_tone(200000, 0.8)

# Collect data
M = 30
N = 30
p1 = np.zeros(M)
p2 = np.zeros(M)
p1v = np.zeros(M)
p2v = np.zeros(M)
for k in range(M):
    pf1 = np.zeros(N)
    pf2 = np.zeros(N)

    print("Off tune")
    sdr.trx_lo = 3000000000
    sdr.trx_lo_chip_b = 3000000000
    time.sleep(1)
    print("Tune back")
    sdr.trx_lo = 2000000000
    sdr.trx_lo_chip_b = 2000000000
    time.sleep(1)
    print("Syncing")
    sdr.mcs_chips()
    print("Done syncing")
    print("Calibrating")
    sdr.calibrate_rx_qec_en = 1
    sdr.calibrate_rx_qec_en_chip_b = 1
    sdr.calibrate_tx_qec_en = 1
    sdr.calibrate_tx_qec_en_chip_b = 1
    sdr.calibrate_rx_phase_correction_en_chip_b = 1
    sdr.calibrate_rx_phase_correction_en = 1
    sdr.calibrate = 1
    sdr.calibrate_chip_b = 1
    print("Done calibrating")

    # Flush
    for r in range(N):
        x = sdr.rx()

    for r in range(N):
        x = sdr.rx()
        pf1[r] = measure_phase(x[0], x[1])
        pf2[r] = measure_phase(x[0], x[2])

    if plot_time_domain:
        plt.clf()
        plt.plot(np.real(x[0][:1000]))
        plt.plot(np.real(x[1][:1000]))
        plt.plot(np.real(x[2][:1000]))
        plt.show()
        plt.draw()
        plt.pause(2)

    p1[k] = np.mean(pf1)
    p2[k] = np.mean(pf2)
    p1v[k] = np.var(pf1)
    p2v[k] = np.var(pf2)
    print("Phases", p1[k], p2[k])
    print("Variances", p1v[k], p2v[k])
    plt.clf()
    x = np.array(range(0, k + 1))
    plt.errorbar(x, p1[x], yerr=p1v[x], label="Channel 0/1)")
    plt.errorbar(x, p2[x], yerr=p2v[x], label="Channel 0/2")
    plt.xlim([-1, x[-1] + 1])
    plt.xlabel("Measurement Index")
    plt.ylabel("Phase Difference (Degrees)")
    plt.legend()
    plt.draw()
    plt.pause(0.05)


plt.show()
