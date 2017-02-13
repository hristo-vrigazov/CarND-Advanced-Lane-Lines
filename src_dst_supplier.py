import numpy as np

def get_src_dst(img_size=(1280, 720)):
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

	return src, dst