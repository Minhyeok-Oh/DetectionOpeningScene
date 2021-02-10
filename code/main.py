import cv2
import imagehash
from PIL import Image

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
    frameRate = 0.3 #//it will capture image in each 0.5 second
    count = 1
    success = get_hash(vidcap, sec, count, video_filename, hashes)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        if sec >= 480:
            break
        success = get_hash(vidcap, sec, count, video_filename, hashes)
    vidcap.release()


hashes_A = []
hashes_B = []

video_to_hashes('C:/Users/alsgu/Downloads/편의점 샛별이.E01.200620.1080p.WEB-DL.x264.AAC-Deresisi.mp4', hashes_A)
video_to_hashes('C:/Users/alsgu/Downloads/편의점 샛별이.E02.200620.1080p.WEB-DL.x264.AAC-Deresisi.mp4', hashes_B)



states = ('intro', 'none')
observations = ('(0,0)', '(0,0)', '(1,0)', '(1,1)', '(1,0)', '(0,0)', '(0,0)', '(1,0)', '(1,1)', '(1,1)')
start_probability = {'intro': 0.43, 'none': 0.57}
transition_probability = {
    'intro': {'intro': 0.63, 'none': 0.37},
    'none': {'intro': 0.44, 'none': 0.56}
}

emission_probability = {
    'intro': {'(0,0)': 0.28, '(1,0)': 0.32, '(1,1)': 0.4},
    'none': {'(0,0)': 0.43, '(1,0)': 0.24, '(1,1)': 0.23}
}
#
# Helps visualize the steps of Viterbi.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)


def viterbi(obs, states, start_p, trans_p, emit_p):
    global t
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        print(y)
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
        print(V)
        print(path)

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
            print("d", newpath)
        # Don't need to remember the old paths
        path = newpath

    print_dptable(V)

    (prob, state) = max((V[t][y], y) for y in states)
    return (prob, path[state])


def example():
    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)


print(example())

print(hashes_A, hashes_B)

result = []

for hash_A in hashes_A:
    for hash_B in hashes_B:
        diff = hash_A["hash"] - hash_B["hash"]
        if diff < 5:
            result.append({"count": hash_A["count"], "sec": hash_A["sec"]})
            break
print(result)