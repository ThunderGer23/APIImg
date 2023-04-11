from tensorflow import io, image, newaxis, float32
from io import BytesIO
from base64 import b64encode, b64decode
from numpy import sum, array, squeeze
import tensorflow_hub as hub
from math import sqrt
from PIL import Image

#modelo de RN convolucional mobilenet 
embed = hub.KerasLayer("https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4")

#funcion para el preprocesamiento de la imagen
class TensorVector(object):
  def __init__(self, FileName=None):
    self.FileName = FileName
  def process(self):
        img = image.convert_image_dtype(image.resize_with_pad(io.decode_jpeg(io.read_file(self.FileName), channels=3), 224, 224), float32)[newaxis, ...]
        return list(squeeze(embed(img)))


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

# #accediendo a las imagenes
# drive.mount('/content/drive')
# os.chdir('/content/drive/MyDrive/APA_entrenamientos/img_tesis')

img1_tit = 'VSCodeAPIImg.png'
img2_tit = 'VSCodeAPIPara.png'

def Interprete(img1_tit, img2_tit):
  helper = TensorVector(img1_tit)
  vec = helper.process()
  helper_2 = TensorVector(img2_tit)
  vec2 = helper_2.process()
  similarity = (jaccard_similarity(vec, vec2) + cosineSim(vec, vec2) + pearson_def(vec, vec2)) / 3
  return True if (similarity >= 0.5) else False

print(Interprete(img1_tit,img2_tit))