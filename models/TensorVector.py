from tensorflow import io, image, newaxis, float32
from numpy import squeeze
import tensorflow_hub as hub

#modelo de RN convolucional mobilenet 
embed = hub.KerasLayer("https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4")

class TensorVector(object):
  def __init__(self, FileName=None):
    self.FileName = FileName
  def process(self):
        img = image.convert_image_dtype(image.resize_with_pad(io.decode_jpeg(io.read_file(self.FileName), channels=3), 224, 224), float32)[newaxis, ...]
        return list(squeeze(embed(img)))