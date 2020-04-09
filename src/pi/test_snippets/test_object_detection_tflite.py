## DOESN'T WORK YET

import tflite_runtime.interpreter as tflite
import tensorflow as tf
import numpy as np


import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Load TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path="models/ssd_mobilenet_v3_coco/detect_coco.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # # Our operations on the frame come here
    # Transform frame to the right input format
    input_data = np.moveaxis(cv2.dnn.blobFromImage(frame, size=(320, 320), swapRB=True).astype(dtype='uint8'), 1, -1)

    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Obtain results 
    interpreter.invoke()
    boxes = interpreter.get_tensor(output_details[0]['index'])
    scores = interpreter.get_tensor(output_details[1]['index'])
    scores1 = interpreter.get_tensor(output_details[2]['index'])
    scores2 = interpreter.get_tensor(output_details[3]['index'])
    # Overlay the classes and bounding boxes on the original frame
    for box in boxes:
        # Probably need to de-quantize or whatever
        # Also rescale to original shape
        # Also need to figure out how those 2034 boxes relate to the original image
        x1, x2, y1, y2 = box[1], box[3], box[2], box[0]
        cv2.rectangle(frame ,(x1,y1),(x2,y2),(0,255,0),2)
        # cv2.putText(im,'Moth Detected',(x+w+10,y+h),0,0.3,(0,255,0))


    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()