import tensorflow_hub as hub
import tensorflow as tens
import cv2 as cv
import pandas as pd
import numpy as np

detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/lite3x/detection/1")

labels = pd.read_csv('C:\\Users\\ahayd\Desktop\\My GitHub\\opencv\\detections\\labels.csv', sep=';', index_col='ID')
labels = labels['OBJECT (2017 REL.)']

vid = cv.VideoCapture(0)

while True:
    
    ret, frame = vid.read()
    frame = cv.flip(frame, 1)
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    rgb_tensor = tens.convert_to_tensor(rgb, dtype=tens.uint8)
    rgb_tensor = tens.expand_dims(rgb_tensor, 0)


    boxes, scores, classes, num_det = detector(rgb_tensor)
    p_label = classes.numpy().astype('int')[0]
    
    p_label = [labels[i] for i in p_label]
    p_box = boxes.numpy()[0].astype('int')
    p_score = scores.numpy()[0]

    for score, (miny, minx, maxy, maxx), label in zip(p_score, p_box, p_label):
        if score < 0.5:
            continue

        score_text = f'%{100 * round(score,0)}'
        frame = cv.rectangle(frame, (minx, miny), (maxx, maxy), (0,0,255), 2)
        font = cv.FONT_HERSHEY_COMPLEX
        cv.putText(frame, f'{label}', (minx, miny-10), font, 1.1, (0,255,0), 2)
        cv.putText(frame, f'{score_text}', (minx, miny-30), font, 1, (0,255,0), 2)

    cv.imshow('detection', frame)

    key = cv.waitKey(2)
    if key == ord('q'):
        break

vid.release()
cv.destroyAllWindows()
