from os import listdir
from os.path import isfile, join
import time  # 프로그램 실행 시간 측정
import utils.constants as util
import hmm as hmm
import data_processing.train_data as pc
import extract_result.get_result as gr
import winsound as sd
import json
import os


def beefsound():
    fr = 2000
    du = 1000
    sd.Beep(fr, du)


def all_execute_for_series():
    states = ('intro', 'none')


    dir_list = [util.DATASETFOLDER + "/" + f for f in listdir(util.DATASETFOLDER)]

    for vid_name in dir_list:
        print(vid_name)
        files = [str(vid_name) + '/' + f for f in listdir(vid_name) if isfile(join(vid_name, f))]

        index = 0
        files_len = len(files)
        while index < files_len:
            path, ext = os.path.splitext(files[index])

            if ext == '.json':
                del files[index]
                files_len = files_len - 1
                continue
            index = index + 1

        start = time.time()
        observation = []

        hash_list = []

        temp_observation = []

        pc.combine_observation(files, temp_observation)
        pc.observation_processing(observation, temp_observation)

        len_of_train = int((0.7) * len(files))
        len_of_test = len(files) - len_of_train

        end = time.time() - start

        labels = []

        with open(f"{vid_name}/intro_info.json", "r") as st_json:
            st_python = json.load(st_json)

        pc.create_label_list(len_of_train, labels, st_python)

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
            print(gr.get_intro_interval(example(test)))

        print("time: ", end)

        execute_result = {
            "series": vid_name,
            "probability": {
                "start": start_p,
                "transition": transition_p,
                "emission": emission_p
            },
            "running_time": end
        }

        with open(f"{vid_name}execute_result.json", "w") as json_file:
            json.dump(execute_result, json_file, indent=4)




def one_series_execute(dir_name):
    states = ('intro', 'none')

    start = time.time()

    files = [str(dir_name) + '/' + f for f in listdir(dir_name) if isfile(join(dir_name, f))]

    index = 0
    files_len = len(files)
    while index < files_len:
        path, ext = os.path.splitext(files[index])

        if ext == '.json':
            del files[index]
            files_len = files_len - 1
            continue
        index = index + 1


    observation = []

    temp_observation = []

    pc.combine_observation(files, temp_observation)
    pc.observation_processing(observation, temp_observation)

    len_of_train = int((0.7) * len(files))
    len_of_test = len(files) - len_of_train

    end_time = time.time() - start

    labels = []

    beefsound()

    with open(f"{dir_name}/intro_info.json", "r") as st_json:
        st_python = json.load(st_json)

    pc.create_label_list(len_of_train, labels, st_python)

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

    predict_result = {}
    for test in testX:
        idx += 1
        print(str(idx) + '화')
        print(example(test))
        print(gr.get_intro_interval(example(test)))
        predict_result[f'{idx}'] = gr.get_intro_interval(example(test))


    print("time: ", end_time)

    execute_result = {
        "series": dir_name,
        "probability": {
            "start": start_p,
            "transition": transition_p,
            "emission": emission_p
        },
        "running_time": end_time
    }

    execute_result['predict_result'] = predict_result

    with open(f"{dir_name}/execute_result.json", "w") as json_file:
        json.dump(execute_result, json_file, indent=4)


all_execute_for_series()