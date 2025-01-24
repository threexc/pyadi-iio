import pytest

hardware = "ad4003"
classname = "adi.ad4003"


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize(
    "attr, val, tol, repeats, sleep, sub_channel",
    [
        (
            "sampling_frequency",
            [10000, 50000, 100000, 200000, 500000, 1000000, 2000000],
            1,
            1,
            0,
            "_channel",
        ),
    ],
)
def test_ad4003_attr(
    test_attribute_multiple_values,
    iio_uri,
    classname,
    attr,
    val,
    tol,
    repeats,
    sleep,
    sub_channel,
):
    test_attribute_multiple_values(
        iio_uri, classname, attr, val, 1, repeats, sleep, sub_channel
    )


#########################################
@pytest.mark.iio_hardware(hardware, True)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0])
def test_ad4003_rx_data(test_dma_rx, iio_uri, classname, channel):
    test_dma_rx(iio_uri, classname, channel, buffer_size=2 ** 15)
