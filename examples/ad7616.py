# Copyright (C) 2021 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Set up AD7616
ad7616 = adi.ad7616(uri="ip:analog")
ad_channel = 0

ad7616.rx_output_type = "SI"
ad7616.rx_enabled_channels = [ad_channel]
ad7616.rx_buffer_size = 2 ** 16

raw = ad7616.channel[0].raw
data = ad7616.rx()

print(data)
