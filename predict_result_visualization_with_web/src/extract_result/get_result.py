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


def result_to_json():
    i = 0