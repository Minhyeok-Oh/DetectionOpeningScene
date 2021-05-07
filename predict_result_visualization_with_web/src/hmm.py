

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