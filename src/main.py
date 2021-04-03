from os import listdir
from os.path import isfile, join
import time # 프로그램 실행 시간 측정
import utils.constants as util
import hmm as hmm
import data_processing.train_data as pc
import extract_result.get_result as gr
import winsound as sd

def beefsound():
    fr = 2000
    du = 1000
    sd.Beep(fr, du)

states = ('intro', 'none')


start = time.time()

files = [str(util.DATASETFOLDER) + '/' + f for f in listdir(util.DATASETFOLDER) if isfile(join(util.DATASETFOLDER, f))]

observation = []

hash_list = []

temp_observation = []

pc.combine_observation(files, temp_observation)
pc.observation_processing(observation, temp_observation)


len_of_train = int((0.7) * len(files))
len_of_test = len(files) - len_of_train



end = time.time() - start

labels = []

beefsound()

pc.create_label_list(len_of_train, labels)


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

print("train: ", trainX, "test: ", testX)

print("time: ", end)