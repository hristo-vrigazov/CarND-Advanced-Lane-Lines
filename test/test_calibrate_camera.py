import unittest
import os

from calibrate_camera import CalibratedCamera

class Test(unittest.TestCase):

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
		c = CalibratedCamera()
		c.undistort("camera_cal/calibration1.jpg", "output_images/undistorted_example.jpg")