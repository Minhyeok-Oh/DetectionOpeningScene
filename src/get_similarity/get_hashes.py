import cv2
import imagehash
from PIL import Image
import utils.constants as c

def get_hash(vidcap, sec, count, video_filename, hashes):
    vidcap.SET(cv2.CAP_PROP_POS_MSEC, sec*1000)
    hasFrames, image = vidcap.read()

    if hasFrames:
        image = cv2.resize(image, (256, 256))
        hash_img = imagehash.average_hash(Image.fromarray(image))
        hashes.append({"hash": hash_img, "count": count, "sec": sec})
    return hasFrames



def video_to_hashes(video_filename, hashes):

    vidcap = cv2.VideoCapture(video_filename)
    sec = 0
    frameRate = c.FRAMERATE #it will capture image in each 0.5 second
    count = 1
    success = get_hash(vidcap, sec, count, video_filename, hashes)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        if sec >= c.VIDEO_TIME:
            break
        success = get_hash(vidcap, sec, count, video_filename, hashes)
    vidcap.release()
