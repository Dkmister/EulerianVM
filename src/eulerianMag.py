#from eularian_magnification.base import eulerian_magnification, show_frequencies
from Transformacoes import uint8_2_float
import os
import cv2
import numpy
print("imports ok")

def uint8_to_float(img):
    result = numpy.ndarray(shape=img.shape, dtype='float')
    result[:] = img * (1. / 255)
    return result

def get_capture_dimensions(capture):
    """Get the dimensions of a capture"""
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height
	
def _load_video(video_filename):
    """Load a video into a numpy array"""
    print("Loading " + video_filename)
    if not os.path.isfile(video_filename):
        raise Exception("File Not Found: %s" % video_filename)
    # noinspection PyArgumentList
    capture = cv2.VideoCapture(video_filename)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width, height = get_capture_dimensions(capture)
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    x = 0
    vid_frames = numpy.zeros((frame_count, height, width, 3), dtype='uint8')
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        vid_frames[x] = frame
        x += 1
    capture.release()

    return vid_frames, fps

def load_video_float(video_filename):
    vid_data, fps = _load_video(video_filename)
    return uint8_2_float(vid_data), fps
	
def play_video(video_filename):
    orig_vid, fps = load_video_float(video_filename)
    play_vid_data(orig_vid)

def play_vid_data(frames):
    play_pyramid([frames])
	
def play_pyramid(pyramid):
	i = 0
	while True:
		try:
			for level, vid in enumerate(pyramid):
				cv2.imshow('Level %i' % level, vid[i])
			i += 1
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		except IndexError:
			break
#show_frequencies('face.mp4')
#eulerian_magnification('face.mp4', image_processing='gaussian', pyramid_levels=6, freq_min=50.0 / 60.0, freq_max=1.0, amplification=50)
#play_pyramid(pyramid)
video, fps = _load_video('face.mp4')
play_vid_data(video)

print("fim \n fps:" + str(fps))