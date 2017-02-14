import numpy as np

class RoadOffsetFinder:
    def __init__(self, xm_per_pix=3.7/700):
        self.xm_per_pix = xm_per_pix


    def get_offset(self, lanes_image):
        only_green_channel = lanes_image[:, :, 1]
        last_row = only_green_channel[719, :]
        nonzero = np.nonzero(last_row)[0]
        first = nonzero[0]
        last = nonzero[-1]
        middle = (first + last) / 2.0
        center = lanes_image.shape[1] / 2.0
        return (middle - center) * self.xm_per_pix
