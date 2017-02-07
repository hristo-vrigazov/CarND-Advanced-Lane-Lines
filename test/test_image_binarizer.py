import os
import unittest
import cv2
import numpy as np

from binarize_image import ImageBinarizer

class ImageBinarizerTest(unittest.TestCase):
	
	def test_image_binarizer_returns_binarized_image(self):
		input_file = "./test_images/test1.jpg"
		image = cv2.imread(input_file)
		imageBinarizer = ImageBinarizer()

		binarized_image = imageBinarizer.binarize(image)
		self.assertTrue(self._is_binary(binarized_image))


	def test_binarize_file(self):
		input_file = 'test_images/test5.jpg'
		output_file = 'output_images/binarized.jpg'

		imageBinarizer = ImageBinarizer()
		imageBinarizer.binarize_file(input_file, output_file)
		self.assertTrue(os.path.exists(output_file))


	def _is_binary(self, image):
		return np.array_equal(image, image.astype(bool))


