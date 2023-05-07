import matplotlib
import matplotlib.pyplot as plt
import cv2
import os
import re
from os.path import join
from time import sleep
from threading import Thread, Event
from global_hotkeys import *
import keyboard
import ctypes


PATH_TO_MOVES = r"""J:\Petru\Projects\Results\Vid4\Hands\Movement"""
START_INDEX = 470
KEYFRAME_TIME = 0.3
change_event = Event()
not_running_event = Event()
plot_photos = Event()

current_index = START_INDEX
main_loop = True



class Exit(Exception):
    pass


class Next(Exception):
    pass


class Previous(Exception):
    pass


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


class VideoPlayer:
    def __init__(self):
        self.__WorkingThread = None # Thread(name="VideoThread")
        not_running_event.set()
        self.__continue_cond = True

    def __play_vid(self, current_index):
        not_running_event.clear()
        current_path = join(PATH_TO_MOVES, "move" + str(current_index))
        os.chdir(current_path)
        self.__continue_cond = True

        while self.__continue_cond:
            for image in sorted_alphanumeric(os.listdir(current_path)):
                frame = cv2.imread(join(current_path, image))
                cv2.imshow("video", frame)
                cv2.setWindowProperty("video", cv2.WND_PROP_TOPMOST, 1)
                k = cv2.waitKey(5)

                sleep(KEYFRAME_TIME)

                if change_event.is_set():
                    cv2.destroyAllWindows()
                    not_running_event.set()
                    self.__continue_cond = False
                    break

    def change_index(self, new_index):
        self.__WorkingThread = Thread(target=self.__play_vid, args=(new_index,), name="VideoThread")
        self.__WorkingThread.start()

    def stop(self):
        self.__continue_cond = False

v_player = VideoPlayer()


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def r_(ret):
    return ret


def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)


def play_video(local_current_index):
    current_path = join(PATH_TO_MOVES, "move"+str(local_current_index))
    os.chdir(current_path)

    while True:
        for image in sorted_alphanumeric(os.listdir(current_path)):
            frame = cv2.imread(join(current_path, image))
            cv2.imshow("video", frame)
            cv2.setWindowProperty("video", cv2.WND_PROP_TOPMOST, 1)
            k = cv2.waitKey(5)
            # if k == 100:  # D KeyHelp.py
            #     raise Next
            #
            # elif k == 27:
            #     raise Exit
            #
            # elif k == 97:
            #     raise Previous
            if keyboard.is_pressed('f9'):
                raise Next
            elif keyboard.is_pressed('esc'):
                raise Exit
            elif keyboard.is_pressed('f3'):
                raise Previous
            sleep(KEYFRAME_TIME)


def pyplot(current_index):
    current_path = join(PATH_TO_MOVES, "move" + str(current_index))
    os.chdir(current_path)
    fig = plt.figure(figsize=(10, 2))
    fig.canvas.manager.set_window_title("move"+str(current_index))
    images = sorted_alphanumeric(os.listdir(current_path))

    img1 = cv2.cvtColor(cv2.imread(join(current_path, images[0])), cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(cv2.imread(join(current_path, images[1])), cv2.COLOR_BGR2RGB)
    img3 = cv2.cvtColor(cv2.imread(join(current_path, images[2])), cv2.COLOR_BGR2RGB)
    img4 = cv2.cvtColor(cv2.imread(join(current_path, images[3])), cv2.COLOR_BGR2RGB)
    img5 = cv2.cvtColor(cv2.imread(join(current_path, images[4])), cv2.COLOR_BGR2RGB)

    fig.add_subplot(1, 5, 1)
    plt.imshow(img1)
    plt.axis("off")
    plt.title(images[0])

    fig.add_subplot(1, 5, 2)
    plt.imshow(img2)
    plt.axis("off")
    plt.title(images[1])

    fig.add_subplot(1, 5, 3)
    plt.imshow(img3)
    plt.axis("off")
    plt.title(images[2])

    fig.add_subplot(1, 5, 4)
    plt.imshow(img4)
    plt.axis("off")
    plt.title(images[3])

    fig.add_subplot(1, 5, 5)
    plt.imshow(img5)
    plt.axis("off")
    plt.title(images[4])

    plt.show(block=False)
    move_figure(fig, 0, 0)
    plt.pause(0.02)


def show_imgs(current_index):
    change_event.set()
    not_running_event.wait()
    change_event.clear()
    plot_photos.set()

    v_player.change_index(current_index)


def nextf():
    global current_index
    current_index += 1
    if os.listdir(join(PATH_TO_MOVES, "move" + str(current_index))):
        show_imgs(current_index)
    else:
        Mbox('Warning', 'A folder without content has been skipped\n( move'+str(current_index)+" )", 0)
        nextf()

def prevf():
    global current_index
    current_index -= 1
    if os.listdir(join(PATH_TO_MOVES, "move" + str(current_index))):
        show_imgs(current_index)
    else:
        Mbox('Warning', 'A folder without content has been skipped\n( move' + str(current_index) + " )", 0)
        prevf()

def Exitf():
    global main_loop
    main_loop = False
    v_player.stop()
    stop_checking_hotkeys()
    plot_photos.set()



bindings = [
    [["f3"], None, prevf],
    [["f9"], None, nextf],
    [["escape"], None, Exitf]
]
register_hotkeys(bindings)



def main():
    continue_condition = True
    previous_input = None
    # while True:
    #     keyboard.unhook_all()
    start_checking_hotkeys()
    plot_photos.clear()

    while True:
        plot_photos.wait()
        if not main_loop:
            break
        plot_photos.clear()
        plt.close('all')
        pyplot(current_index)


    # while continue_condition:
    #     if os.listdir(join(PATH_TO_MOVES, "move" + str(current_index))):
    #         pyplot(current_index)
    #         try:
    #             play_video(current_index)
    #         except Exit:
    #             continue_condition = False
    #         except Next:
    #             cv2.destroyAllWindows()
    #             plt.close('all')
    #             current_index += 1
    #             previous_input = Next
    #         except Previous:
    #             cv2.destroyAllWindows()
    #             plt.close('all')
    #             current_index -= 1
    #             previous_input = Previous
    #     elif previous_input == Previous:
    #         current_index -= 1
    #     else:
    #         current_index += 1



print('start')
print("please press f3 or f9")
main()
print('exit')
