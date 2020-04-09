import numpy as np
import tensorflow as tf
import cv2 as cv
import os
import json

# Text printing settings
font = cv.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2


with open('data/80_coco_labels.json', 'r') as f:
    labels = json.load(f)

# Read the graph.
with tf.compat.v1.gfile.FastGFile('models/ssd_mobilenet_v1_coco_2017_11_17/frozen_inference_graph.pb', 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())


cap = cv.VideoCapture(0)

with tf.compat.v1.Session() as sess:
    # Restore session
    sess.graph.as_default()
    tf.import_graph_def(graph_def, name='')

    while(True):

        # Read and preprocess an image.
        ret, img = cap.read()
        rows = img.shape[0]
        cols = img.shape[1]
        inp = cv.resize(img, (300, 300))
        inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

        # Run the model
        out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                        sess.graph.get_tensor_by_name('detection_scores:0'),
                        sess.graph.get_tensor_by_name('detection_boxes:0'),
                        sess.graph.get_tensor_by_name('detection_classes:0')],
                    feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

        # Visualize detected bounding boxes.
        num_detections = int(out[0][0])
        for i in range(num_detections):
            classId = int(out[3][0][i])
            label = labels[str(classId)]
            score = float(out[1][0][i])
            bbox = [float(v) for v in out[2][0][i]]
            if score > 0.3:
                x = bbox[1] * cols
                y = bbox[0] * rows
                right = bbox[3] * cols
                bottom = bbox[2] * rows
                bottomLeftCornerOfText = (int(x), int(y-3))
                cv.putText(img, label,
                            bottomLeftCornerOfText,
                            cv.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (125, 255, 51),
                            2)
                cv.rectangle(img, (int(x), int(y)), (int(right),
                                                    int(bottom)), (125, 255, 51), thickness=2)

        cv.imshow('TensorFlow MobileNet-SSD', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
cv.waitKey()
