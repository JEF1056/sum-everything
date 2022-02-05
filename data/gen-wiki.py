import sys
import numpy as np
import os
import gdown
import zipfile
from tqdm import tqdm
from src.helpers import clean

DATA_URL = "https://drive.google.com/uc?export=download&id=1BnPhEZISDwuWIEzLMQeud-HBA4BSUUor"
IN = "wikiHow"

if not os.path.exists("wikiHow.zip"):
    gdown.download(DATA_URL, "wikiHow.zip", quiet=False)
if not os.path.exists(IN):
    os.mkdir(IN)
    if zipfile.is_zipfile("wikiHow.zip"):
        fz = zipfile.ZipFile("wikiHow.zip", "r")
        for file in fz.namelist():
            fz.extract(file, ".")

title_file = open('wikiHow/titles.txt', mode="r", encoding="utf-8").read().split("\n")
path = "wikiHow/articles"
os.makedirs("../datasets/wiki", exist_ok=True)
train_data = open("../datasets/wiki/wikiHow.train", mode="w", encoding="utf-8")
val_data = open("../datasets/wiki/wikiHow.validation", mode="w", encoding="utf-8")
outputs = [train_data, val_data]
overall_count = [0, 0]
if len(sys.argv) == 1: np.random.seed(2022)
else: np.random.seed(int(sys.argv[1]))
error_count = 0

for title in tqdm(title_file):
    file_path = path + "/" + title + ".txt"
    try:
        f = open(file_path, mode='r', encoding="utf-8")
        cont = f.read().split("@article")
        cont_tgt, cont_src = cont[0], cont[1]
        cont_tgt = cont_tgt.replace("@summary", " ")

        category = np.random.choice(2, 1, p=[0.8, 0.2])[0]
        outputs[category].write(clean(cont_src) + "\t" + clean(cont_tgt) + "\n")
        overall_count[category] += 1

    except Exception as e:
        # print("open", file_path, "fail. ")
        error_count += 1
        # print(e)

print("overall_count: [train, val]=", overall_count)
print("file name encoding error: ", error_count)
train_data.close()
val_data.close()