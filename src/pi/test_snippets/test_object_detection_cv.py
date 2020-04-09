## DOESN'T WORK YET

import cv2 as cv


from cv2.dnn import  DetectionModel

net = cv.dnn.DetectionModel('models/ssd_mobilenet_v3_large_coco/frozen_inference_graph.pb', 'models/ssd_mobilenet_v3_large_coco/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

frame = cv.imread('data/example.jpg')

classes, confidences, boxes = net.detect(frame, confThreshold=0.5)

for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
    print(classId, confidence)
    cv.rectangle(frame, box, color=(0, 255, 0))

cv.imshow('out', frame)
cv.waitKey()


while(True):
# Capture frame-by-frame
    ret, frame = cap.read()
    rows = frame.shape[0]
    cols = frame.shape[1]
    cvNet.setInput(cv.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False))
    cvOut = cvNet.forward()

    for detection in cvOut[0,0,:,:]:
        score = float(detection[2])
        if score > 0.3:
            left = detection[3] * cols
            top = detection[4] * rows
            right = detection[5] * cols
            bottom = detection[6] * rows
            cv.rectangle(frame, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)

    cv.imshow('img', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()