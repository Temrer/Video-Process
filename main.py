import cv2
import os



def main():
    input_folder = r"J:\Petru\Projects\Results\Vid1\Split"
    output_folder = r"J:\Petru\Projects\Results\Vid1\Processed"

    os.chdir(input_folder)
    output_folders = -1
    for folder in os.listdir(input_folder):
        current_folder = os.path.join(input_folder, folder)
        os.chdir(current_folder)
        output_folders += 1
        split_images_left = []
        split_images_right = []
        for filename in os.listdir(current_folder):
            file = cv2.imread(filename)

            width = int(file.shape[1])
            height = int(file.shape[0])
            halved_width = width//2

            sub_image1 = file[0:height, 0:halved_width]
            sub_image2 = file[0:height, halved_width+1:width]

            split_images_left.append(sub_image1)
            split_images_right.append(sub_image2)


        output_subfolder = os.path.join(output_folder, "folder"+str(output_folders))
        os.mkdir(output_subfolder)
        os.chdir(output_subfolder)
        last_index = 0
        for index, image in enumerate(split_images_left):
            cv2.imwrite("img"+str(index)+".jpg", image)
            last_index = index

        for index, image in enumerate(split_images_right):
            cv2.imwrite("img"+str(last_index + index)+".jpg", image)
    print("done")


if __name__ == "__main__":
    main()