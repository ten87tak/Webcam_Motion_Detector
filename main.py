import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread


video = cv2.VideoCapture(0)
time.sleep(1)

frame_1 = None
status_list = []
count = 1


def clean_folder():
    print("The clean_folder function started.")
    # Get a list that contains all the file names stored in the images folder:
    images = glob.glob("images/*.png")
    # Remove all the images inside the images folder:
    for image in images:
        os.remove(image)
    print("The clean_folder function ended.")


while True:
    status = 0
    check, frame = video.read()

    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(grayscale, (21, 21), 0)

    if frame_1 is None:
        frame_1 = gaussian

    delta_frame = cv2.absdiff(frame_1, gaussian)

    threshold = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dilate_frame = cv2.dilate(threshold, None, iterations=2)
    cv2.imshow("my_video", dilate_frame)

    outlines, check = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

    for outline in outlines:
        if cv2.contourArea(outline) < 5000:
            continue

        x, y, w, h = cv2.boundingRect(outline)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            # 'glob' returns a list of file names
            images_list = glob.glob("images/*.png")
            index = int(len(images_list) / 2)
            image_to_be_sent = images_list[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        threading_email = Thread(target=send_email, args=(image_to_be_sent, ))
        threading_email.daemon = True
        threading_cleaning = Thread(target=clean_folder)
        threading_cleaning.daemon = True

        threading_email.start()

    print(status_list)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

threading_cleaning.start()

video.release()


