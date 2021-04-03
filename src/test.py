from os import listdir
from os.path import isfile, join



DATASETFOLDER = "F:/고스트 헌트"

files = ["F:/고스트 헌트/" + f for f in listdir(DATASETFOLDER) if isfile(join(DATASETFOLDER, f))]


