import cv2
import os
import numpy as np

curr_dir = r"""J:\Petru\Projects\Results\Vid2\Processed"""


def get_rid_of_watermark(sample_zone, watermark_zone):
    sample_zone_width = sample_zone.shape[1]
    sample_zone_height = sample_zone.shape[0]

    average_color = np.zeros(shape=(3,))
    for column in sample_zone:
        for pixel in column:
            for index, color_value in enumerate(pixel):
                average_color[index] = average_color[index] + color_value/255

    for index, color in enumerate(average_color):
        average_color[index] = average_color[index]/sample_zone_height/sample_zone_width * 255

    for column in watermark_zone:
        for index, pixel in enumerate(column):
            column[index] = average_color


for folder in os.listdir(curr_dir):
    os.chdir(os.path.join(curr_dir, folder))
    for image_name in os.listdir(os.path.join(curr_dir, folder)):
        image = cv2.imread(image_name)
        get_rid_of_watermark(image[0:50, 220:310], image[5:30, 220:310])
        cv2.imwrite(image_name, image)

    print('done'+folder)
