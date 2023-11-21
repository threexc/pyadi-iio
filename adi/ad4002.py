# Copyright (C) 2022-2023 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

import numpy as np
from adi.context_manager import context_manager
from adi.rx_tx import rx


class ad4002(rx, context_manager):
    """AD4002 device"""

    _device_name = "ad4002"
    _rx_data_type = np.int32
    _complex_data = False
    _rx_channel_names = ["voltage0"]

    def __init__(self, uri=""):

        context_manager.__init__(self, uri, self._device_name)

        self._rxadc = self._ctx.find_device("ad4002")
        self._ctrl = self._ctx.find_device("ad4002")
        self._device_name = "ad4002"
        rx.__init__(self)

        if not self._ctrl:
            raise Exception("Error in selecting matching device")

        if not self._rxadc:
            raise Exception("Error in selecting matching device")

        rx.__init__(self)

    @property
    def sampling_frequency(self):
        """sample_rate: Only readable
        """
        return self._get_iio_dev_attr("sampling_frequency")

    @sampling_frequency.setter
    def sampling_frequency(self, value):
        """Set the sampling frequency."""
        self._set_iio_dev_attr("sampling_frequency", str(value))

    @property
    def raw(self):
        """AD4002 channel raw value."""
        return self._get_iio_attr(self._rx_channel_names[0], "raw", False)

    @property
    def offset(self):
        """AD4002 channel offset value."""
        return self._get_iio_attr(self._rx_channel_names[0], "offset", False)

    @offset.setter
    def offset(self, value):
        self._set_iio_attr(self._rx_channel_names[0], "offset", False, str(value))

    @property
    def scale(self):
        """AD4002 channel scale value."""
        return self._get_iio_attr(self._rx_channel_names[0], "scale", False)

    @scale.setter
    def scale(self, value):
        self._set_iio_attr(self._rx_channel_names[0], "scale", False, str(value))
