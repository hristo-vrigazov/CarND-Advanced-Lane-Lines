import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class ImageBinarizer:

	def binarize(self, image):
	    S = self.thresholded_s_channel(image)
	    sobel_img = self.sobelx(image)
	    combined_binary = np.zeros_like(S)
	    combined_binary[(sobel_img == 1) & (S == 1)] = 1
	    return combined_binary


	def binarize_file(self, source_image_file, destination_image_file):
		image = mpimg.imread(source_image_file)
		binarized = self.binarize(image)
		plt.imsave(destination_image_file, binarized, cmap='gray')


	def thresholded_s_channel(self, image, thresh=(90, 255)):
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