from os import listdir
from os.path import isfile, join
import time # 프로그램 실행 시간 측정
import utils.constants as util
import hmm as hmm
from get_similarity import compare as compare , get_hashes as hash


states = ('intro', 'none')


def linearSearch(list, key):
    for i in range(len(list)):
        if key == list[i]['count']:
            return 1
    return -1

start = time.time()

files = [str(util.DATASETFOLDER) + '/' + f for f in listdir(util.DATASETFOLDER) if isfile(join(util.DATASETFOLDER, f))]

observation = []

hash_list = []

temp_observation = []

len_of_train = int((0.7) * len(files))
len_of_test = len(files) - len_of_train

for i in range(len(files)):
    hash_A = []
    hash.video_to_hashes(files[i], hash_A)
    hashlist = []

    zero_one_list = []

    for j in range(5):
        index = i + j
        if index >= len(files) - 1:
            index = i - j

        if i == j:
            continue
        hash_B = []
        hash.video_to_hashes(files[index], hash_B)
        result = compare.hash_compare(hash_A, hash_B)
        hashlist.append(result)

    for k in range(1, int(util.FRAME_NUMBER) + 1):
        count = 0
        for m in range(4):
            if linearSearch(hashlist[m], k) == 1:
                count += 1

        if count >= 2:
            zero_one_list.append('1')
        else:
            zero_one_list.append('0')

    temp_observation.append(zero_one_list)


observation = []

for obs in temp_observation:
    c = 0
    observation_one_video = []
    for i in range(len(obs)):
        intro_and_none = False
        if ((i+1) % (util.SCENE / util.FRAMERATE)) == 0:
            if obs[i] == '1':
                c += 1
            if c >= 7:
                observation_one_video.append('1')
            else:
                observation_one_video.append('0')
            c = 0
        else:
            if obs[i] == '1':
                c += 1
    observation.append(observation_one_video)


def create_intro_list(start_time, end_time):
    result = []

    start = start_time / util.SCENE
    end = end_time / util.SCENE
    for i in range(int(util.VIDEO_TIME/util.SCENE)):
        if start <= i <= end:
            result.append('intro')
        else:
            result.append('none')

    return result


end = time.time() - start

labels = []

for i in range(len_of_train):
    start = int(input('%d 화 인트로 Start : ' % (i+1)))
    end = int(input('%d 화 인트로 End : ' % (i+1)))
    labeled = create_intro_list(start, end)
    labels.append(labeled)


trainX, trainY = observation[:len_of_train], labels[:len_of_train]
testX, testY = observation[-len_of_test:], labels[-len_of_test:]

start_p = hmm.get_start_probability_list(trainX, trainY)
transition_p = hmm.get_transition_probability_list(trainX, trainY)
emission_p = hmm.get_emission_probability_list(trainX, trainY)


def example(observation):
    return hmm.viterbi(observation,
                   states,
                   start_p,
                   transition_p,
                   emission_p)

idx = len_of_train

for test in testX:
    idx += 1
    print(str(idx) + '화')
    print(example(test))



print("train: ", trainX, "test: ", testX)

print("time: ", end)