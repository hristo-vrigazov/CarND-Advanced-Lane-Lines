import unittest
from transform_perspective import PerspectiveTransformer
import matplotlib.image as mpimg
import numpy as np

class PerspectiveTransorferTest(unittest.TestCase):

	def setUp(self):
		self.src = np.float32([
		    (200, 800),
		    (640, 400),
		    (740, 400),
		    (1150, 800)])

		self.dst = np.float32([
			(450, 800),
       		(450, 0),
       		(900, 0),
       		(900, 800)])

	def test_pespective_transormer_transform(self):
		perspective_transformer = PerspectiveTransformer(self.src, self.dst)
		input_file = "./test_images/test1.jpg"
		img = mpimg.imread(input_file)

		warped = perspective_transformer.transform(img)

		self.assertTrue(warped.shape == img.shape)


	def test_perspective_transformer_inverse_transform(self):
		perspective_transformer = PerspectiveTransformer(self.src, self.dst)
		input_file = "./test_images/test1.jpg"
		img = mpimg.imread(input_file)

		warped = perspective_transformer.inverse_transform(img)

		self.assertTrue(warped.shape == img.shape)

