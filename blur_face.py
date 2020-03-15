from imutils import paths
import argparse
import cv2
import os
import sys
from shutil import move
from os import path
from pathlib import Path, PureWindowsPath


ap = argparse.ArgumentParser()
ap.add_argument("-t", "--threshold", type=float, default=40.0,
                help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

target_dir = os.getcwd()
target_dir = os.path.join(target_dir, 'data_src')
target_dir = os.path.join(target_dir, 'aligned')

#Setup the output directory for matching faces
blur_path = os.path.join(target_dir, 'blur')
not_blur_path = os.path.join(target_dir, 'not_blur')
no_face_path = os.path.join(target_dir, 'no_face')

#Make sure the path exists and if not, create it.
if not path.isdir(blur_path):
    try:
        os.mkdir(blur_path)
    except OSError:
        print("Creation of the directory %s failed" % blur_path)
    else:
        print("Successfully created the directory %s " % blur_path)

if not path.isdir(not_blur_path):
    try:
        os.mkdir(not_blur_path)
    except OSError:
        print("Creation of the directory %s failed" % not_blur_path)
    else:
        print("Successfully created the directory %s " % not_blur_path)

if not path.isdir(no_face_path):
    try:
        os.mkdir(no_face_path)
    except OSError:
        print("Creation of the directory %s failed" % no_face_path)
    else:
        print("Successfully created the directory %s " % no_face_path)


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F)

def report_image(image, laplacian, faces, face_laplacians=None):
    text = "Not Blurry"
    if laplacian.var() < args["threshold"]:
        text = "Blurry"

    if len(faces):
        return text
    else:
        return "Blurry"

def face_recognition(gray):
    face_cascade = cv2.CascadeClassifier("blur_face/haarcascade_frontalface_default.xml")
    return face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))

def crop_faces(gray, faces):
    return [gray[y: y + h, x: x + w] for x,y,w,h in faces]

for image_path in os.listdir(target_dir):
    file_name = os.path.join(target_dir, image_path)
    if os.path.isfile(file_name):
        file_name = os.path.join(target_dir, image_path)

        image = cv2.imread(file_name)
        image = cv2.resize(image, dsize=(256, 256))

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_recognition(gray)

        face_laplacians = None
        if len(faces) == False:
            move(
                file_name, no_face_path)

        elif len(faces):
            face_images = crop_faces(gray, faces)

            face_laplacians = [variance_of_laplacian(face_image) for face_image in face_images]

            laplacian = variance_of_laplacian(gray)
            blur = report_image(image, laplacian, faces, face_laplacians)
            if blur == "Blurry":
                move(
                    file_name, blur_path)
            elif blur == "Not Blurry":
                move(
                    file_name, not_blur_path)
