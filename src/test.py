from os import listdir
from os.path import isfile, join


#
# DATASETFOLDER = "F:/고스트 헌트"
#
# files = ["F:/고스트 헌트/" + f for f in listdir(DATASETFOLDER) if isfile(join(DATASETFOLDER, f))]
#

temp = (1.1745510915347549e-14, ['none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'intro', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none'])


def get_intro_interval(viterbi_result):
    intro_list = []
    count = 0
    start = 0
    end = 0
    consecutive = 0

    for viterbi_result in temp[1]:

        if count + 1 < len(temp[1]):

            if viterbi_result == 'intro':
                if (temp[1][count+1] == 'intro') & (consecutive == 0):
                    start = count
                    consecutive = 1
                elif (temp[1][count+1] == 'none') & (consecutive == 1):
                    end = count
                    consecutive = 0
                    intro_list.append(str(start*3) + '-' + str(end*3))
        count = count + 1
    return intro_list

