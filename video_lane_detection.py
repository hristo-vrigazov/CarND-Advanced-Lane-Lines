from moviepy.editor import VideoFileClip
from image_lane_detection import ImageLaneDetector

class VideoLaneDetector:
	def __init__(self):
		self.image_lane_detector = ImageLaneDetector()


	def generate_video_with_detected_lanes(self, input_file_name, output_file_name):
		input_clip = VideoFileClip(input_file_name)
		output_clip = input_clip.fl_image(self.image_lane_detector.detect_lanes)
		output_clip.write_videofile(output_file_name, audio=False)