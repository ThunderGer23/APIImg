from tensorflow import io, image, newaxis, float32
from base64 import b64encode, b64decode
from io import BytesIO
from numpy import sum, array
from math import sqrt
from PIL import Image
from models.TensorVector import TensorVector
from threading import current_thread

def convertBase64(FileName):
    with open(FileName, "rb") as f:
        data = f.read()
    return array(Image.open(BytesIO(b64decode(b64encode(data).decode("UTF-8")))))

def cosineSim(a1,a2):
    sum, suma1, sumb1 = [0, 0, 0]
    tup = list(zip(a1,a2))
    for i,j in tup:
        suma1 += i**2
        sumb1 += j**2
        sum += i*j
    return (sum / ((sqrt(suma1))*(sqrt(sumb1))))

def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

def average(x):
    return(float(sum(x)) / len(x)) if(len(x) > 0) else None

def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod, xdiff2, ydiff2 = [0, 0 , 0]
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff **2
        ydiff2 += ydiff **2
    return float(diffprod / sqrt(xdiff2 * ydiff2))

def Interprete(img1_tit, img2_tit):
  helper = TensorVector(img1_tit)
  vec = helper.process()
  helper_2 = TensorVector(img2_tit)
  vec2 = helper_2.process()
  value = (jaccard_similarity(vec, vec2) + cosineSim(vec, vec2) + pearson_def(vec, vec2)) / 3
  current_thread().similarity = True if (value >= 0.5) else False
  current_thread().percent = value
  current_thread().images = [img1_tit, img2_tit]
  return