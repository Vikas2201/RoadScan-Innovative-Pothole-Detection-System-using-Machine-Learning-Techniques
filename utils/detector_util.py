import numpy as np
import tensorflow as tf
import cv2
from utils import label_map_util
import constants
import warnings
warnings.filterwarnings("ignore")

detection_graph = tf.Graph()
BASE_DIR = constants.BASEDIR
TRAINED_MODEL_DIR = '/frozen_graphs'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = BASE_DIR + TRAINED_MODEL_DIR + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = BASE_DIR + TRAINED_MODEL_DIR + '/pothole_labelmap.pbtxt'
NUM_CLASSES = 1

# load label map using utils provided by tensorflow object detection api
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

a = b = 0

# Load a frozen infrerence graph into memory
def load_inference_graph():
    # load frozen tensorflow model into memory
    print("> ====== Loading frozen graph into memory")
    detection_graph1 = tf.Graph()
    with detection_graph1.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.compat.v1.Session(graph=detection_graph1)
    print(">  ====== Inference graph loaded.")
    return detection_graph1, sess

def draw_box_on_image(num_potholes_detect, score_thresh, scores, boxes, classes, im_width, im_height, image_np, lat,lon):
    latitude = lat
    longitude = lon
    focalLength = 875
    avg_width = 4.0

    # To more easily differentiate distances and detected bboxes
    global a
    pothole_cnt = 0
    color = None
    color0 = (255, 0, 0)
    for i in range(num_potholes_detect):
        if (scores[i] > score_thresh):
            if classes[i] == 1:
                id = 'pothole'
            if i == 0:
                color = color0
            else:
                color = color0
            (left, right, top, bottom) = (boxes[i][1] * im_width, boxes[i][3] * im_width,boxes[i][0] * im_height, boxes[i][2] * im_height)
            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))
            dist = distance_to_camera(avg_width, focalLength, int(right - left))
            if dist:
                pass
            cv2.rectangle(image_np, p1, p2, color, 5, 1)
            pothole_cnt = pothole_cnt + 1
            print(pothole_cnt)

            color_geo = (0, 0, 255)
            cv2.putText(image_np, 'Latitude  :' + str(latitude), (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_geo, 2)
            cv2.putText(image_np, 'Longitude : ' + str(longitude), (10, 136), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_geo,2)
            cv2.putText(image_np, 'confidence: ' + str("{0:.2f}".format(scores[i])),
                        (int(left), int(top) - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if pothole_cnt == 0:
            a = 0
        else:
            a = pothole_cnt
    print('inside draw box method')
    return a

# Show fps value on image.
def draw_text_on_image_cnt(fps, image_np):
    cv2.putText(image_np, fps, (20, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (77, 255, 9), 2)

# compute and return the distance from the hand to the camera using triangle similarity
def distance_to_camera(knownWidth, focalLength, pixelWidth):
    return (knownWidth * focalLength) / pixelWidth

# Actual detection .. generate scores and bounding boxes given an image
def detect_objects(image_np, detection_graph, sess):

    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    image_np_expanded = np.expand_dims(image_np, axis=0)

    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores,detection_classes, num_detections],feed_dict={image_tensor: image_np_expanded})
    print("inside object detect method")
    return np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes)
