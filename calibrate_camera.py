import numpy as np
import cv2
import glob
import pickle
import os
import matplotlib.pyplot as plt


class CalibratedCamera:

    def __init__(self, camera_calibration_pickle="camera_calibration_pickle.p", 
        calibration_images_pattern="camera_cal/calibration*.jpg"):
        if os.path.exists(camera_calibration_pickle):
            self._calibrate_camera_by_pickle(camera_calibration_pickle)
        else:
            self._calibrate_camera_by_chessboard_images(9, 6, 
                camera_calibration_pickle, calibration_images_pattern)

    def _calibrate_camera_by_pickle(self, camera_calibration_pickle):
        print('Reading calibrated camera parameters from pickle file')
        with open(camera_calibration_pickle,"rb") as pickle_in:
            dist_pickle = pickle.load(pickle_in)

        self.mtx = dist_pickle["mtx"]
        self.dist = dist_pickle["dist"]


    def _calibrate_camera_by_chessboard_images(self, nx, ny, 
            camera_calibration_pickle, calibration_images_pattern):
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        print('Calibrating camera')
        objp = np.zeros((nx * ny, 3), np.float32)
        objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d points in real world space
        imgpoints = [] # 2d points in image plane.

        # Make a list of calibration images
        images = glob.glob(calibration_images_pattern)

        # Step through the list and search for chessboard corners
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

            # If found, add object points, image points
            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)

        img = cv2.imread("camera_cal/calibration1.jpg")
        img_size = (img.shape[1], img.shape[0])

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size,None,None)
        dist_pickle = {}
        dist_pickle["mtx"] = mtx
        dist_pickle["dist"] = dist

        with open(camera_calibration_pickle, "wb") as pickle_file: 
            pickle.dump(dist_pickle, pickle_file)

        self.mtx = mtx
        self.dist = dist