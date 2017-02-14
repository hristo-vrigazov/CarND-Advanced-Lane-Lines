##Writeup Template
###You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

Quick commands:
---
To run unit tests:
```
green -r
```
To get test code coverage in html format:
```
coverage html 
```

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[test-distorted]: ./camera_cal/calibration1.jpg "Distorted test"
[test-undistorted]: ./output_images/test_undist.jpg "Undistorted test"
[distorted]: ./test_images/test1.jpg "Distorted"
[undistorted]: ./output_images/undistorted_example.jpg "Undistorted"
[example_test_image]: ./test_images/test5.jpg "Example test image"
[binarized]: ./output_images/binarized.jpg "Binary Example"
[perspective_transformed]: ./output_images/perspective_transform.jpg "Perspective transformed"
[binary_warped]: ./output_images/binary_warped.jpg "Binary warped"
[binary_fitted]: ./output_images/binary_fitted.jpg "Binary fitted"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points
###Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
###Writeup / README

####1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!
###Camera Calibration

####1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the `calibrate_camera.py` file, in the `CalibratedCamera` class.
This class is an abstraction of a calibrated camera, and in this contructor, it sets mtx and dist 
fields either by reading them from pickle, or by using chessboard images. mtx and dist are then used 
in the `CalibratedCamera#undistort` method.

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I then use this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 


Distorted                      |  Undistorted
:----------------------------:|:------------------------------:
![alt text][test-distorted]| ![alt text][test-undistorted]

###Pipeline (single images)

####1. Provide an example of a distortion-corrected image.
In the `calibrate_camera.py` file, in the `CalibratedCamera` class, the undistort method
uses the mtx and dst fields, which were initialized in the constuctor. See the example output:

Distorted                      |  Undistorted
:----------------------------:|:------------------------------:
![alt text][distorted]| ![alt text][undistorted]

####2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I experimented with different ways to binarize the image (see the file `binarize_image.py`). I converted the image to HLS color space, and then used a thresholding, and combined that with normal grayscale thresholding.
I also experimented with different adaptive thresholding, like Gaussian for example, but they did not seem
to produce reliable results.

Test image                      |  Binarized
:----------------------------:|:------------------------------:
![alt text][example_test_image]| ![alt text][binarized]


####3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The class `PerspectiveTransformer`, located in the file `transform_perspective.py`, is responsible for 
the perspective transform. To construc an instance of this object, we must pass in the source and destination
points. Then the matrices for transorm and inverse transform are computed and they are later used in
the `transform` and `inverse_transform` methods. The actual source and destination points are supplied
using the `get_src_dst` function in the `src_dst_supplier.py` file and they are as following:

```
src = np.float32(
    [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
    [((img_size[0] / 6) - 10), img_size[1]],
    [(img_size[0] * 5 / 6) + 60, img_size[1]],
    [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
dst = np.float32(
    [[(img_size[0] / 4), 0],
    [(img_size[0] / 4), img_size[1]],
    [(img_size[0] * 3 / 4), img_size[1]],
    [(img_size[0] * 3 / 4), 0]])

```
This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 585, 460      | 320, 0        | 
| 203, 720      | 320, 720      |
| 1127, 720     | 960, 720      |
| 695, 460      | 960, 0        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

Test image                      |  Transformed image
:----------------------------:|:------------------------------:
![alt text][example_test_image]| ![alt text][perspective_transformed]

####4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

The code for fitting the polynomial is located in the `curvature_finder.py` file.

Binary warped                      |   Polynomial fitted
:----------------------------:|:------------------------------:
![alt text][binary_warped]| ![alt text][binary_fitted]

####5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines # through # in my code in `my_other_file.py`

####6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

###Pipeline (video)

####1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

###Discussion

####1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  

