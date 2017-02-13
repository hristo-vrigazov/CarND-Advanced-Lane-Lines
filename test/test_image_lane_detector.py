import unittest
import cv2
from image_lane_detection import ImageLaneDetector

class ImageLaneDetectorTest(unittest.TestCase):

	def test_detect_lanes_returns_image_with_the_same_shape(self):
		image_lane_detector = ImageLaneDetector()

		input_file = "./test_images/test1.jpg"
		img = cv2.imread(input_file)

		output_img = image_lane_detector.detect_lanes(img)

		self.assertTrue(output_img.shape == img.shape)