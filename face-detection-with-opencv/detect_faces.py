import numpy as np
import argparse
import cv2


# Construct the argument parse and parse the arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to image file")
ap.add_argument("-p", "--prototxt", required= True, help ="path to the Caffee deploy prototxt file")
ap.add_argument("-m", "--model", required = True, help="path to the Caffee pretrained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help = "minimum confidence")
args = vars(ap.parse_args())

# Load our serialized model from the disk
print("[INFO] Loading model...")
net = cv2.dnn.readNetFromCaffe(args['prototxt'], args['model'])

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
image = cv2.imread(args['image'])
(h,w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300,300)), 1.0, (300,300), (104.0, 177.0, 123.0))

# Pass the blob through the network and obtain the detections and predictions

print("[INFO] Computing object detections")
net.setInput(blob)
detections = net.forward()

#loop over the detections

for i in range(0, detections.shape[2]):
    # extract the confidence for each of the predictions
    confidence = detections[0, 0, i, 2]

    # filter out the detections by ensuring the  confidence is above threshold
    if confidence > args['confidence']:
        # compute the (x,y)-coordinate of the bounding box for the object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # draw the bounding box of the face along with the associated probability
        text = "{:.2f}%".format(confidence * 100)
        y = startY -10 if startY-10 >10 else startY + 10
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

# Show the output image

cv2.imshow("Detector Output: ", image)
cv2.waitKey(0)

        