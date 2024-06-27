# import tensorflow as tf
# import tensorflow_hub as hub

# def load_models():
#     detector_EfficientNetV2 = hub.load("https://tfhub.dev/tensorflow/efficientdet/d2/1")
#     detector_CenternetHourglass104_512x512 = hub.load("https://tfhub.dev/tensorflow/centernet/hourglass_512x512/1")

#     return detector_EfficientNetV2, detector_CenternetHourglass104_512x512

# def load_label_map():
#     label_map_url = "https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt"
#     label_map_path = tf.keras.utils.get_file("coco_classes.txt", label_map_url)

#     return label_map_path