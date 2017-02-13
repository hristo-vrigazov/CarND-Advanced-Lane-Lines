import numpy as np
import matplotlib.pyplot as plt
import cv2

class CurvatureFinder:
	def __init__(self):
		pass
		

	def fit(self, binary_warped, show_fit=False):
		# Assuming you have created a warped binary image called "binary_warped"
		# Take a histogram of the bottom half of the image
		histogram = np.sum(binary_warped[binary_warped.shape[0]//2:,:], axis=0)
		# Create an output image to draw on and  visualize the result
		out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255
		# Find the peak of the left and right halves of the histogram
		# These will be the starting point for the left and right lines
		midpoint = np.int(histogram.shape[0]/2)
		leftx_base = np.argmax(histogram[:midpoint])
		rightx_base = np.argmax(histogram[midpoint:]) + midpoint

		# Choose the number of sliding windows
		nwindows = 9
		# Set height of windows
		window_height = np.int(binary_warped.shape[0]/nwindows)
		# Identify the x and y positions of all nonzero pixels in the image
		nonzero = binary_warped.nonzero()
		nonzeroy = np.array(nonzero[0])
		nonzerox = np.array(nonzero[1])
		# Current positions to be updated for each window
		leftx_current = leftx_base
		rightx_current = rightx_base
		# Set the width of the windows +/- margin
		margin = 100
		# Set minimum number of pixels found to recenter window
		minpix = 50
		# Create empty lists to receive left and right lane pixel indices
		left_lane_inds = []
		right_lane_inds = []

		# Step through the windows one by one
		for window in range(nwindows):
		    # Identify window boundaries in x and y (and right and left)
		    win_y_low = binary_warped.shape[0] - (window+1)*window_height
		    win_y_high = binary_warped.shape[0] - window*window_height
		    win_xleft_low = leftx_current - margin
		    win_xleft_high = leftx_current + margin
		    win_xright_low = rightx_current - margin
		    win_xright_high = rightx_current + margin
		    # Draw the windows on the visualization image
		    cv2.rectangle(out_img,(win_xleft_low,win_y_low),(win_xleft_high,win_y_high),(0,255,0), 2) 
		    cv2.rectangle(out_img,(win_xright_low,win_y_low),(win_xright_high,win_y_high),(0,255,0), 2) 
		    # Identify the nonzero pixels in x and y within the window
		    good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
		    good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]
		    # Append these indices to the lists
		    left_lane_inds.append(good_left_inds)
		    right_lane_inds.append(good_right_inds)
		    # If you found > minpix pixels, recenter next window on their mean position
		    if len(good_left_inds) > minpix:
		        leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
		    if len(good_right_inds) > minpix:        
		        rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

		# Concatenate the arrays of indices
		left_lane_inds = np.concatenate(left_lane_inds)
		right_lane_inds = np.concatenate(right_lane_inds)

		# Extract left and right line pixel positions
		leftx = nonzerox[left_lane_inds]
		lefty = nonzeroy[left_lane_inds] 
		rightx = nonzerox[right_lane_inds]
		righty = nonzeroy[right_lane_inds] 

		# Fit a second order polynomial to each
		left_fit = np.polyfit(lefty, leftx, 2)
		right_fit = np.polyfit(righty, rightx, 2)

		ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0])

		# Generate x and y values for plotting
		left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
		right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]

		out_img[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [255, 0, 0]
		out_img[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [0, 0, 255]
			
		if show_fit:
			print(left_fit)
			print(right_fit)
			plt.imshow(out_img)
			plt.plot(left_fitx, ploty, color='yellow')
			plt.plot(right_fitx, ploty, color='yellow')
			plt.xlim(0, 1280)
			plt.ylim(720, 0)
			plt.show()


		left_y_eval = np.max(lefty)
		right_y_eval = np.max(righty)

		ym_per_pix = 30/720 # meters per pixel in y dimension
		xm_per_pix = 3.7/700 # meters per pixel in x dimension

		# Fit new polynomials to x,y in world space
		left_fit_cr = np.polyfit(lefty*ym_per_pix, leftx*xm_per_pix, 2)
		right_fit_cr = np.polyfit(righty*ym_per_pix, rightx*xm_per_pix, 2)
		# Calculate the new radii of curvature
		left_curverad = ((1 + (2*left_fit_cr[0]*left_y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
		right_curverad = ((1 + (2*right_fit_cr[0]*right_y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])
		# Now our radius of curvature is in meters
		print(left_curverad, 'm', right_curverad, 'm')
		self.curvature_radius = (left_curverad + right_curverad) / 2.0

		# Create an image to draw the lines on
		warp_zero = np.zeros_like(binary_warped).astype(np.uint8)
		color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

		# Recast the x and y points into usable format for cv2.fillPoly()
		pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
		pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
		pts = np.hstack((pts_left, pts_right))

		# Draw the lane onto the warped blank image
		cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))

		return self.curvature_radius, 0.3, color_warp