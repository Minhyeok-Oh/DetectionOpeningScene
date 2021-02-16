import cv2
import imagehash
from PIL import Image
from os import listdir
from os.path import isfile, join
import numpy as np

DATASETFOLDER = "C:/dataset"
VIDEO_TIME = 20
FRAMERATE = 0.5
FRAME_NUMBER = VIDEO_TIME / FRAMERATE

def hash_compare(hashes_A, hashes_B):
    result = []

    for hash_A in hashes_A:
        for hash_B in hashes_B:
            diff = hash_A["hash"] - hash_B["hash"]
            if diff < 5:
                result.append({"count": hash_A["count"], "sec": hash_A["sec"]})
                break
    return result

def get_hash(vidcap, sec, count, video_filename, hashes):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
    hasFrames, image = vidcap.read()

    if hasFrames:
        image = cv2.resize(image, (256, 256))
        hash_img = imagehash.average_hash(Image.fromarray(image))
        hashes.append({"hash": hash_img, "count": count, "sec": sec})
    return hasFrames



def video_to_hashes(video_filename, hashes):

    vidcap = cv2.VideoCapture(video_filename)
    sec = 0
    frameRate = 0.5 #//it will capture image in each 0.5 second
    count = 1
    success = get_hash(vidcap, sec, count, video_filename, hashes)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        if sec >= VIDEO_TIME:
            break
        success = get_hash(vidcap, sec, count, video_filename, hashes)
    vidcap.release()


hashes_A = []
hashes_B = []


states = ('intro', 'none')
observations = ('(0,0)', '(0,0)', '(1,0)', '(1,1)', '(1,0)', '(0,0)', '(0,0)', '(1,0)', '(1,1)', '(1,1)')
start_probability = {'intro': 0.43, 'none': 0.57}
transition_probability = {
    'intro': {'intro': 0.63, 'none': 0.37},
    'none': {'intro': 0.44, 'none': 0.56}
}

emission_probability = {
    'intro': {'(0,0)': 0.28, '(1,0)': 0.32, '(1,1)': 0.4},
    'none': {'(0,0)': 0.43, '(1,0)': 0.24, '(1,1)': 0.23}
}
#
# Helps visualize the steps of Viterbi.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)


def viterbi(obs, states, start_p, trans_p, emit_p):
    global t
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        print(y)
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
        print(V)
        print(path)

    # alternative Python 2.7+ initialization syntax
    # V = [{y:(start_p[y] * emit_p[y][obs[0]]) for y in states}]
    # path = {y:[y] for y in states}

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max((V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)

            V[t][y] = prob
            # print("gggg", path[state] + [y])
            # print("eeee", path[state], [y])
            newpath[y] = path[state] + [y]
            print("d", newpath)
        # Don't need to remember the old paths
        path = newpath

    print_dptable(V)

    (prob, state) = max((V[t][y], y) for y in states)
    return (prob, path[state])


def example():
    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)

# print(example())
#
# print(hashes_A, hashes_B)
def linearSearch(list, key):
    for i in range(len(list)):
        if key == list[i]['count']:
            return 1
    return -1



files = [str(DATASETFOLDER) + '/' + f for f in listdir(DATASETFOLDER) if isfile(join(DATASETFOLDER, f))]

observation = []

hash_list = []

temp_observation = []

for i in range(5):
    hash_A = []
    video_to_hashes(files[i], hash_A)
    hashlist = []

    zero_one_list = []

    for j in range(5):
        if i == j:
            continue
        hash_B = []
        video_to_hashes(files[j], hash_B)
        result = hash_compare(hash_A, hash_B)
        hashlist.append(result)

    for k in range(1, int(FRAME_NUMBER)):
        count = 0
        for m in range(4):
            if linearSearch(hashlist[m], k) == 1:
                count += 1

        if count >= 3:
            zero_one_list.append(1)
        else:
            zero_one_list.append(0)

    temp_observation.append(zero_one_list)

observation = []
for obs in temp_observation:
    c = 0
    observation_one_video = []
    for i in range(len(obs)):
        intro_and_none = False
        if ((i+1) % 4) == 0 or i == len(obs):
            if obs[i] == 1:
                c += 1
            if c >= 3:
                observation_one_video.append(1)
            else:
                observation_one_video.append(0)
            c = 0
        else:
            if obs[i] == 1:
                c += 1
    observation.append(observation_one_video)

print(observation)

def create_intro_list(start_time, end_time):
    result = []

    start = start_time / FRAMERATE
    end = end_time / FRAMERATE
    for i in range(int(480/0.5)):
        if i >= start and i <= end:
            result.append('intro')
        else:
            result.append('none')

    return result

print(create_intro_list(240,360))