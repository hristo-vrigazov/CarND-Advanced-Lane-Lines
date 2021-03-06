import unittest
import os
import cv2

from calibrate_camera import CalibratedCamera

class CalibratedCameraTest(unittest.TestCase):

	def test_constuctor_sets_mtx_dist_if_pickle_is_not_available(self):
		pickle_file_name = "something.p"
		images_pattern = "camera_cal/calibration*.jpg"

		os.remove(pickle_file_name)
		calibrated_camera = CalibratedCamera(pickle_file_name, images_pattern)

		self.assertIsNotNone(calibrated_camera.mtx)
		self.assertIsNotNone(calibrated_camera.dist)


	def test_constuctor_set_mtx_dist_from_pickle_if_available(self):
		pickle_file_name = "something.p"
		images_pattern = "camera_cal/calibration*.jpg"

		os.remove(pickle_file_name)

		# create the pickle
		CalibratedCamera(pickle_file_name, images_pattern)

		# now calibrated camera sets those from pickle
		calibrated_camera = CalibratedCamera(pickle_file_name, images_pattern)
		self.assertIsNotNone(calibrated_camera.mtx)
		self.assertIsNotNone(calibrated_camera.dist)


	def test_calibrated_camera_can_undistort_image(self):
		input_file = "./test_images/test1.jpg"
		output_file = "output_images/undistorted_example.jpg"
		c = CalibratedCamera()
		c.undistort_file(input_file, output_file)

		self.assertTrue(os.path.exists(output_file))


	def test_undistort_image(self):
		input_file = "./test_images/test1.jpg"
		image = cv2.imread(input_file)

		c = CalibratedCamera()
		undistorted_image = c.undistort(image)

		self.assertTrue(undistorted_image.shape == image.shape)