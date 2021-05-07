import numpy as np
import cv2
# 영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
# 영상이 있는 경로

im_list = []

vidcap = cv2.VideoCapture('F:/dataset/나쁜 녀석들/나쁜 녀석들.E11.720p.H264.AAC-BCB.mkv')

count = 0

vidcap.set(cv2.CAP_PROP_POS_MSEC, (0.4)*1000)
sec = 0
while(vidcap.isOpened()):

    ret, image = vidcap.read() # 이미지 사이즈 960x540으로 변경
    image = cv2.resize(image, (128, 128)) # 30프레임당 하나씩 이미지 추출
    im_list.append(image)
    count = count + 1
    sec = sec + 0.4
    sec = round(sec, 2)
    if sec >= 44:
        break

c = 1
img = cv2.imread('static/img/img.jpg', cv2.IMREAD_COLOR)
img = cv2.resize(img, (128, 128))
im_list_list = []
temp = []
print(len(im_list))
for a in im_list:
    temp.append(a)
    if c % 20 == 0:
        addc = cv2.hconcat(temp)
        im_list_list.append(addc)
        temp = []
    elif c == len(im_list) and c % 20 != 0:
        for i in range(20 - (c % 20)):
            temp.append(img)
        print(len(temp))
        addc = cv2.hconcat(temp)
        im_list_list.append(addc)


    c = c + 1

num = 0

addv = cv2.vconcat(im_list_list)

cv2.imwrite('static/img/ddgg.jpg', addv)

result = 0
cc = 0
# for b in im_list_list:
#
#     addc = cv2.hconcat(b)
#     cv2.imwrite(f'addc {cc}.jpg', addc)
#     cc = cc + 1
# for b in im_list_list:
#     addv = cv2.hconcat(b)

vidcap.release()

