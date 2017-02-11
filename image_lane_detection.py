from calibrate_camera import CalibratedCamera
from image_binarizer import ImageBinarizer
from transform_perspective import PerspectiveTransformer
from src_dst_supplier import get_src_dst

class ImageLaneDetector:

	def __init__(self, img_size):
		self.camera = CalibratedCamera()
		self.binarizer = ImageBinarizer()
		src, dst = get_src_dst(img_size)
		self.warper = PerspectiveTransformer(src, dst)



