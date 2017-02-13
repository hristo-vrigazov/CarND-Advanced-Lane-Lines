import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class ImageBinarizer:

    def binarize(self, image):
        hsv_thresholded = self.hsv_thresholding(image)
        graysaled_thresholded = self.grayscale_thresholded(image)
        combined_binary = cv2.bitwise_or(hsv_thresholded, graysaled_thresholded)
        return combined_binary
    
    
    def grayscale_thresholded(self, image, T=190):
        grayscaled = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        thresh = grayscaled.copy()
        thresh[thresh > T] = 255
        thresh[thresh < 255] = 0
        return thresh
    

    def hsv_thresholding(self, image, up_thresholds=(20, 60, 50), down_thresholds=(40, 255, 255)):
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, up_thresholds, down_thresholds)
        return mask
    

    def binarize_file(self, source_image_file, destination_image_file):
        image = mpimg.imread(source_image_file)
        binarized = self.binarize(image)
        plt.imsave(destination_image_file, binarized, cmap='gray')


    def thresholded_s_channel(self, image, thresh=(90, 240)):
        hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
        S = hls[:,:,2]
        binary = np.zeros_like(S)
        binary[(S > thresh[0]) & (S <= thresh[1])] = 1
        return binary


    def sobelx(self, image, thresh=(5, 200)):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
        abs_sobelx = np.absolute(sobelx)
        scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
        sxbinary = np.zeros_like(scaled_sobel)
        sxbinary[(scaled_sobel >= thresh[0]) & (scaled_sobel <= thresh[1])] = 1
        return sxbinary