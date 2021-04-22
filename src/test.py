from os import listdir
import glob, os
from os.path import isfile, join
import winsound as sd
import json


len = 4
folder = "F:/"

data = {
    "start": 43.2,
    "transition": 53.1,
    "emission": 23.4
}
intro = {}

# print(intro)
for i in range(10):
    start = int(input(f'{i+1}화 start: '))
    end = int(input(f'{i+1}화 end: '))
    intro[i+1] = {}
    intro[i + 1]["start"] = start
    intro[i + 1]["end"] = end
# print(intro)
with open(f"{folder}intro_info.json", "w") as json_file:
    json.dump(intro, json_file)

with open(f"{folder}intro_info.json", "r") as st_json:
    st_python = json.load(st_json)

python = {"k": 1, "m":3}

st_python["predict_result"] = python

print(st_python)




