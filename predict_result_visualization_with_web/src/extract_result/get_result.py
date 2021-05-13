from os import listdir
from os.path import isfile,join
import urllib
import cv2
import os
import constants as util
import json

def get_intro_interval(viterbi_result):
    intro_list = []
    count = 0
    start = 0
    end = 0
    consecutive = 0

    for state in viterbi_result[1]:

        if count + 1 < len(viterbi_result[1]):

            if state == 'intro':
                if (viterbi_result[1][count + 1] == 'intro') & (consecutive == 0):
                    start = count
                    consecutive = 1
                elif (viterbi_result[1][count + 1] == 'none') & (consecutive == 1):
                    end = count + 1
                    consecutive = 0
                    intro_list.append(str(start*2) + '-' + str(end*2))
        count = count + 1
    return intro_list


def extract_frame_sequence_of_intro(file_name, start, end):
    im_list = []

    vidcap = cv2.VideoCapture(file_name)

    count = 0
    sec = 0

    while vidcap.isOpened():
        if sec >= start:
            vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
            ret, image = vidcap.read()
            image = cv2.resize(image, (128, 128))
            im_list.append(image)
            count = count + 1
        sec = sec + 0.4
        sec = round(sec, 2)
        if sec >= end:
            break

    c = 1
    img = cv2.imread('C:/Users/alsgu/PycharmProjects/DetectionOpeningScene1/predict_result_visualization_with_web/static/img/white_img.jpg', cv2.IMREAD_COLOR)
    img = cv2.resize(img, (128, 128))
    im_list_list = []
    temp = []
    for a in im_list:
        temp.append(a)
        if c % 20 == 0:
            addc = cv2.hconcat(temp)
            im_list_list.append(addc)
            temp = []
        elif c == len(im_list) and c % 20 != 0:
            for i in range(20 - (c % 20)):
                temp.append(img)

            addc = cv2.hconcat(temp)
            im_list_list.append(addc)

        c = c + 1

    addv = cv2.vconcat(im_list_list)
    name = os.path.basename(file_name)
    real_name = os.path.splitext(name)[0]
    quote_real_name = urllib.parse.quote(real_name)
    path = f'C:/Users/alsgu/PycharmProjects/DetectionOpeningScene1/predict_result_visualization_with_web/static/img/{quote_real_name}.jpg'

    extension = os.path.splitext(path)[1]

    result, encoded_img = cv2.imencode(extension, addv)
    if result:
        with open(path, mode='w+b') as f:
            encoded_img.tofile(f)

    vidcap.release()


def extract_probability_json():
    result = {}
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

    count = 0

    total_start_intro_prob = 0
    total_start_none_prob = 0

    total_transition_intro_to_intro = 0
    total_transition_intro_to_none = 0
    total_transition_none_to_intro = 0
    total_transition_none_to_none = 0

    total_emission_intro_zero = 0
    total_emission_intro_one = 0
    total_emission_none_zero = 0
    total_emission_none_one = 0

    TheNumberOfVOD = 0

    total_intro_interval = 0
    for json_file_name in dir_list:
        count += 1
        with open(f'{json_file_name}/execute_result.json', "r") as json_file:
            st_python = json.load(json_file)
        with open(f'{json_file_name}/intro_info.json', "r") as json_f:
            s_python = json.load(json_f)

        for info in s_python:
            TheNumberOfVOD += 1
            total_intro_interval += s_python[info]['end'] - s_python[info]['start']


        total_start_intro_prob += st_python['probability']['start']['intro']
        total_start_none_prob += st_python['probability']['start']['none']

        total_transition_intro_to_intro += st_python['probability']['transition']['intro']['intro']
        total_transition_intro_to_none += st_python['probability']['transition']['intro']['none']
        total_transition_none_to_intro += st_python['probability']['transition']['none']['intro']
        total_transition_none_to_none += st_python['probability']['transition']['none']['none']

        total_emission_intro_zero += st_python['probability']['emission']['intro']['0']
        total_emission_intro_one += st_python['probability']['emission']['intro']['1']
        total_emission_none_zero += st_python['probability']['emission']['none']['0']
        total_emission_none_one += st_python['probability']['emission']['none']['1']

    average_intro_interval = total_intro_interval / TheNumberOfVOD
    print(average_intro_interval)
    start_prob = {'intro': total_start_intro_prob/count, 'none': 1 - total_start_intro_prob/count}
    transition_prob = {
        'intro': {'intro': total_transition_intro_to_intro/count , 'none': 1 - total_transition_intro_to_intro/count},
        'none': {'intro': total_transition_none_to_intro/count, 'none': 1 - total_transition_none_to_intro/count}
    }
    emission_prob = {
        'intro': {'0': total_emission_intro_zero/count, '1': 1 - total_emission_intro_zero/count},
        'none': {'0': total_emission_none_zero/count , '1': 1 - total_emission_none_zero/count}
    }
    integrated_result = {
        "the_number_of_series": count,
        "probability": {
            "start": start_prob,
            "transition": transition_prob,
            "emission": emission_prob
        },
        "average_intro_interval": average_intro_interval
    }
    with open(f"{util.DATASETFOLDER}/integrated_model.json", "w") as json_file:
        json.dump(integrated_result, json_file, indent=4, ensure_ascii=False)
