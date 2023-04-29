import os
import mediapipe as mp
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import re

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def clamp(min, max, num):
    if num < min:
        return min
    if num > max:
        return max
    return num


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


TargetFolder = r"""J:\Petru\Projects\Results\Vid3"""
SourceFolder = os.path.join(TargetFolder, "Body")

images = sorted_alphanumeric(os.listdir(SourceFolder))

os.chdir(TargetFolder)
if not os.path.exists(os.path.join(TargetFolder, "Hands")):
    os.mkdir("Hands")
os.chdir(os.path.join(TargetFolder, "Hands"))
if not os.path.exists(os.path.join(TargetFolder, "Hands\\LeftHand")):
    os.mkdir("LeftHand")
if not os.path.exists(os.path.join(TargetFolder, "Hands\\RightHand")):
    os.mkdir("RightHand")

RATIO_THRESHOLD = 0.6

index = 0
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    for image_name in images:
        index += 1
        image = cv2.imread(os.path.join(SourceFolder, image_name))
        width = image.shape[1]
        height = image.shape[0]

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        # mp_drawing.draw_landmarks(
        #     image,
        #     results.pose_landmarks,
        #     mp_pose.POSE_CONNECTIONS,
        #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Flip the image horizontally for a selfie-view display.
        if results is not None:
            if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST] and \
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX]:
                left_hand_index_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x * width)
                left_hand_index_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y * height)
                left_hand_index_z = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].z * width)

                left_hand_wrist_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * width)
                left_hand_wrist_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * height)
                left_hand_wrist_z = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].z * width)

                left_hand_dist = int(math.sqrt((left_hand_wrist_x - left_hand_index_x) ** 2 +
                                               (left_hand_wrist_y - left_hand_index_y) ** 2 +
                                               (left_hand_wrist_z - left_hand_index_z) ** 2))

                high_border = clamp(0, height, left_hand_index_y - left_hand_dist)
                low_border = clamp(0, height, left_hand_index_y + left_hand_dist)
                left_border = clamp(0, width, left_hand_index_x - left_hand_dist)
                right_border = clamp(0, width, left_hand_index_x + left_hand_dist)
                left_hand_roi = image[high_border:low_border, left_border:right_border]
                if not (left_hand_roi.shape[0] == 0 or left_hand_roi.shape[1] == 0) and \
                        abs(left_hand_roi.shape[0] / left_hand_roi.shape[1]) > RATIO_THRESHOLD:

                    os.chdir(os.path.join(TargetFolder, "Hands\\LeftHand"))
                    try:
                        res_roi = cv2.resize(left_hand_roi, (100, 100))
                    except cv2.error as e:
                        print(left_hand_roi.shape)
                        print(high_border, low_border, left_border, right_border)
                        print(left_hand_index_x, left_hand_index_y, "  ", left_hand_dist)
                        raise e
                    cv2.imwrite(image_name, res_roi)

            if results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX] and \
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]:
                right_hand_index_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x * width)
                right_hand_index_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y * height)
                right_hand_index_z = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].z * width)

                right_hand_wrist_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * width)
                right_hand_wrist_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * height)
                right_hand_wrist_z = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].z * width)

                right_hand_dist = int(math.sqrt((right_hand_wrist_x - right_hand_index_x) ** 2 +
                                                (right_hand_wrist_y - right_hand_index_y) ** 2 +
                                                (right_hand_wrist_z - right_hand_index_z) ** 2))

                high_border = clamp(0, height, right_hand_index_y - right_hand_dist)
                low_border = clamp(0, height, right_hand_index_y + right_hand_dist)
                left_border = clamp(0, width, right_hand_index_x - right_hand_dist)
                right_border = clamp(0, width, right_hand_index_x + right_hand_dist)
                right_hand_roi = image[high_border:low_border, left_border:right_border]

                if not (right_hand_roi.shape[0] == 0 or right_hand_roi.shape[1] == 0) and \
                        abs(right_hand_roi.shape[0] / right_hand_roi.shape[1]) > RATIO_THRESHOLD:

                    os.chdir(os.path.join(TargetFolder, "Hands\\RightHand"))
                    try:
                        res_roi = cv2.resize(right_hand_roi, (100, 100))
                    except cv2.error as e:
                        print(right_hand_roi.shape)
                        print(high_border, low_border, left_border, right_border)
                        print(right_hand_index_x, right_hand_index_y, "  ", right_hand_dist)
                        raise e
                    cv2.imwrite(image_name, res_roi)

        if index % 100 == 0:
            print(image_name)
