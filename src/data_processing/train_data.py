import utils.constants as util
from get_similarity import compare as compare, get_hashes as hash



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


def create_label_list(num, labels):

    for i in range(num):
        start = input(f'{i+1} start : ')
        end = input(f'{i+1} end : ')
        labels.append(create_intro_list(start, end))


def linear_search(list, key):
    for i in range(len(list)):
        if key == list[i]['count']:
            return 1
    return -1


def observation_processing(observation, temp_observation):
    for obs in temp_observation:
        c = 0
        observation_one_video = []
        for i in range(len(obs)):
            intro_and_none = False
            if ((i + 1) % (util.SCENE / util.FRAMERATE)) == 0:
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


def combine_observation(files, temp_observation):
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
                if linear_search(hashlist[m], k) == 1:
                    count += 1

            if count >= 2:
                zero_one_list.append('1')
            else:
                zero_one_list.append('0')

        temp_observation.append(zero_one_list)
