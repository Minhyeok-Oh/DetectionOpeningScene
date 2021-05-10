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

    total_time = 0
    dir_list = [util.DATASETFOLDER + "/" + f for f in listdir(util.DATASETFOLDER)]

    indexe = 0
    files_lens = len(dir_list)
    while indexe < files_lens:
        path, ext = os.path.splitext(dir_list[indexe])

        if ext == '.json':
            del dir_list[indexe]
            files_lens = files_lens - 1
            continue
        indexe = indexe + 1

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

        predict_result = {}
        for test in testX:
            idx += 1
            print(str(idx) + '화')
            print(example(test))
            print(gr.get_intro_interval(example(test)))
            predict_result[f'{idx}'] = gr.get_intro_interval(example(test))

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
        total_time = total_time + end
        execute_result['predict_result'] = predict_result

        with open(f"{vid_name}/execute_result.json", "w") as json_file:
            json.dump(execute_result, json_file, indent=4, ensure_ascii=False)
        co = 0
        for file_name in files:
            name = os.path.basename(file_name)
            name_without_etc = os.path.splitext(name)[0]
            observation_info = {}
            observation_info['observation'] = observation[co]
            with open(f"{vid_name}/{name_without_etc}.json", "w") as json_file:
                json.dump(observation_info, json_file, indent=4, ensure_ascii=False)
            co = co + 1

    print(f'총 소요시간 : {total_time}')


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
        json.dump(execute_result, json_file, indent=4, ensure_ascii=False)


all_execute_for_series()