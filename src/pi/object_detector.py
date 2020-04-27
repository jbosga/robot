import json
import numpy as np
import tensorflow as tf
import cv2 as cv
import os
from pathlib import Path

class ObjectDetector(object):

    def __init__(self, labels_path='data/80_coco_labels.json', model_path='models/ssd_mobilenet_v1_coco_2017_11_17/frozen_inference_graph.pb', conf_thresh=0.3):
        labels_path = Path.cwd() / Path(labels_path)
        
        with labels_path.open() as f:
            self.labels = json.load(f)
        # Read the graph.
        with tf.compat.v1.gfile.FastGFile(model_path, 'rb') as f:
            self.graph_def = tf.compat.v1.GraphDef()
            self.graph_def.ParseFromString(f.read())

        self.session = tf.compat.v1.Session()

        self.session.graph.as_default()
        tf.import_graph_def(self.graph_def, name='')

        self.conf_thresh = conf_thresh

    def detect(self, img):
            rows = img.shape[0]
            cols = img.shape[1]
            inp = cv.resize(img, (300, 300))
            inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

            # Run the model
            out = self.session.run([self.session.graph.get_tensor_by_name('num_detections:0'),
                            self.session.graph.get_tensor_by_name('detection_scores:0'),
                            self.session.graph.get_tensor_by_name('detection_boxes:0'),
                            self.session.graph.get_tensor_by_name('detection_classes:0')],
                        feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

            # Visualize detected bounding boxes.
            num_detections = int(out[0][0])
            
            detections = []
            for i in range(num_detections):
                classId = int(out[3][0][i])
                label = self.labels[str(classId)]
                score = float(out[1][0][i])
                bbox = [float(v) for v in out[2][0][i]]
                if score > self.conf_thresh:
                    detection = dict()
                    detection["label"] = label
                    detection["score"] = score
                    detection["x"] = bbox[1] * cols
                    detection["y"] = bbox[0] * rows
                    detection["right"] = bbox[3] * cols
                    detection["bottom"] = bbox[2] * rows
                    detections.append(detection)
            return detections