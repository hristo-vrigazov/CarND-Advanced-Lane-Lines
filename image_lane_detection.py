from calibrate_camera import CalibratedCamera
from binarize_image import ImageBinarizer
from transform_perspective import PerspectiveTransformer
from src_dst_supplier import get_src_dst
from curvature_finder import CurvatureFinder

import matplotlib.pyplot as plt
import numpy as np
import cv2


class ImageLaneDetector:

    def __init__(self, img_size=(1280, 720)):
        self.camera = CalibratedCamera()
        self.binarizer = ImageBinarizer()
        src, dst = get_src_dst(img_size)
        self.warper = PerspectiveTransformer(src, dst)
        self.curvature_finder = CurvatureFinder()


    def detect_lanes(self, img, show_fit=False):
        undistored_image = self.camera.undistort(img)
        binarized_image = self.binarizer.binarize(undistored_image)
        binary_warped = self.warper.transform(binarized_image)
        curvature_radius, road_offset, warped_lanes_image = self.curvature_finder.fit(binary_warped, show_fit=show_fit)
        lanes_image = self.warper.inverse_transform(warped_lanes_image)
        return self.draw_results(img, lanes_image, curvature_radius, road_offset)

    def draw_results(self, source_img, lanes_image, curvature_radius, road_offset):
        result = cv2.addWeighted(source_img, 1, lanes_image, 0.3, 0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(result, 'Radius of Curvature = %d(m)' % curvature_radius, (50, 50), font, 1, (255, 255, 255), 2)
        left_or_right = 'left' if road_offset < 0 else 'right'
        cv2.putText(result, 'Vehicle is %.2fm %s of center' % (np.abs(road_offset), left_or_right), (50, 100), font, 1,
                    (255, 255, 255), 2)
        return result





