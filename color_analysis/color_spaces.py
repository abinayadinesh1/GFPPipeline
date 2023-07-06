import argparse
import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, default="color_analysis/random.png",
	help="path to input image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
cv2.imshow("RGB", image) #RGB is our 'window' - what does that mean? also where is our window getting displayed? can look further into imshow
print(image.shape) # (3024, 4032, 3). 3 channels presumably RGB? actually its BGR because thats the way opencv loads it in
print("------")
# print(len(cv2.split(image)[0])) #length of this tuple is three. length of first element is 3024. perfect, so we've split into B, G, R. 

for (name, chan) in zip(("B", "G", "R"), cv2.split(image)):
	cv2.imshow(name, chan)