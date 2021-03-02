import cv2
import imagehash
from PIL import Image
from os import listdir
from os.path import isfile, join

DATASETFOLDER = "C:/dataset/원피스"
VIDEO_TIME = 480
FRAMERATE = 0.5
FRAME_NUMBER = VIDEO_TIME / FRAMERATE
SCENE = 3

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
    frameRate = FRAMERATE #//it will capture image in each 0.5 second
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

states = ('intro', 'none')
#
# Helps visualize the steps of Viterbi.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    # print(s)


def viterbi(obs, states, start_p, trans_p, emit_p):
    global t
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        # print(y)
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
        # print(V)
        # print(path)

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
            # print("d", newpath)
        # Don't need to remember the old paths
        path = newpath

    print_dptable(V)

    (prob, state) = max((V[t][y], y) for y in states)
    return (prob, path[state])


def linearSearch(list, key):
    for i in range(len(list)):
        if key == list[i]['count']:
            return 1
    return -1

files = [str(DATASETFOLDER) + '/' + f for f in listdir(DATASETFOLDER) if isfile(join(DATASETFOLDER, f))]

observation = []

hash_list = []

temp_observation = []

len_of_train = int((0.7) * len(files))
len_of_test = len(files) - len_of_train

for i in range(len(files)):
    hash_A = []
    video_to_hashes(files[i], hash_A)
    hashlist = []

    zero_one_list = []

    for j in range(5):
        index = i + j
        if(index >= len(files) - 1):
            index = i - j

        if i == j:
            continue
        hash_B = []
        video_to_hashes(files[index], hash_B)
        result = hash_compare(hash_A, hash_B)
        hashlist.append(result)

    for k in range(1, int(FRAME_NUMBER) + 1) :
        count = 0
        for m in range(4):
            if linearSearch(hashlist[m], k) == 1:
                count += 1

        if count >= 3:
            zero_one_list.append('1')
        else:
            zero_one_list.append('0')

    temp_observation.append(zero_one_list)

def group_compare_to_get_hash(filename):
    hash_AA = []
    video_to_hashes(filename, hash_AA)
    temp_hashlist = []

    temp_zero_one_list = []

    for j in range(4):
        hash_BB = []
        video_to_hashes(files[j], hash_BB)
        temp_result = hash_compare(hash_AA, hash_BB)
        temp_hashlist.append(temp_result)

    for k in range(1, int(FRAME_NUMBER)):
        temp_count = 0
        for m in range(4):
            if linearSearch(temp_hashlist[m], k) == 1:
                temp_count += 1

        if temp_count >= 3:
            temp_zero_one_list.append('1')
        else:
            temp_zero_one_list.append('0')
    return temp_zero_one_list

observation = []

for obs in temp_observation:
    c = 0
    observation_one_video = []
    for i in range(len(obs)):
        intro_and_none = False
        if ((i+1) % (SCENE / FRAMERATE)) == 0:
            if obs[i] == '1':
                c += 1
            if c >= 5:
                observation_one_video.append('1')
            else:
                observation_one_video.append('0')
            c = 0
        else:
            if obs[i] == '1':
                c += 1
    observation.append(observation_one_video)

print(observation)

def create_intro_list(start_time, end_time):
    result = []

    start = start_time / SCENE
    end = end_time / SCENE
    for i in range(int(VIDEO_TIME/SCENE)):
        if start <= i <= end:
            result.append('intro')
        else:
            result.append('none')

    return result

labels = []

for i in range(len_of_train):
    start = int(input('%d 화 인트로 Start : ' % (i+1)))
    end = int(input('%d 화 인트로 End : ' % (i+1)))
    labeled = create_intro_list(start, end)
    labels.append(labeled)

print(labels)

trainX, trainY = observation[:len_of_train], labels[:len_of_train]
testX, testY = observation[-len_of_test:], labels[-len_of_test:]

def get_emission_probability_list(obs, label):
    intro_all_case = 0
    none_all_case = 0

    intro_one_emission_number = 0
    none_one_emission_number = 0

    for i in range(len(obs)):
        for j in range(len(obs[i])):
            if label[i][j] == 'intro':
                intro_all_case += 1
                if obs[i][j] == '1':
                    intro_one_emission_number += 1
            else:
                none_all_case += 1
                if obs[i][j] == '1':
                    none_one_emission_number += 1

    none_all_case = (len(obs) * len(obs[0])) - intro_all_case

    intro_one_emission_prob = intro_one_emission_number / intro_all_case
    none_one_emission_prob = none_one_emission_number / none_all_case

    emission_prob = {
        'intro': {'0': 1 - intro_one_emission_prob, '1': intro_one_emission_prob},
        'none': {'0': 1 - none_one_emission_prob, '1': none_one_emission_prob}
    }

    return emission_prob

def get_transition_probability_list(obs, label):
    intro_all_case = 0

    intro_intro_transition_number = 0
    none_none_transition_number = 0

    for i in range(len(obs)):
        for j in range(len(obs[i])):
            if j+1 < len(obs[i]):
                if label[i][j] == 'intro':
                    intro_all_case += 1
                    if label[i][j+1] == 'intro':
                        intro_intro_transition_number += 1
                if label[i][j] == 'none':
                    if label[i][j+1] == 'none':
                        none_none_transition_number += 1

    none_all_case = (len(obs) * len(obs[0])) - intro_all_case

    intro_intro_transition_prob = intro_intro_transition_number / intro_all_case
    none_none_transition_prob = none_none_transition_number / none_all_case

    transition_prob = {
        'intro': {'intro': intro_intro_transition_prob, 'none': 1 - intro_intro_transition_prob},
        'none': {'intro': 1 - none_none_transition_prob, 'none': none_none_transition_prob}
    }

    return transition_prob

def get_start_probability_list(obs, label):
    all_case = len(obs)

    intro_start_number = 0

    for i in range(len(obs)):
        if label[i][0] == 'intro':
            intro_start_number += 1

    intro_start_prob = intro_start_number / all_case
    none_start_prob = 1 - intro_start_prob

    start_prob = {'intro': intro_start_prob, 'none': none_start_prob}

    return start_prob

start_p = get_start_probability_list(trainX, trainY)
transition_p = get_transition_probability_list(trainX, trainY)
emission_p = get_emission_probability_list(trainX, trainY)

def example(observation):
    return viterbi(observation,
                   states,
                   start_p,
                   transition_p,
                   emission_p)

for test in testX:
    print(example(test))

print("train: ", trainX, trainY, "test: ", testX, testY)