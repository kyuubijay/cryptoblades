import cv2, pyautogui, time
import numpy as np

time.sleep(2)
filename = "img/src.jpg"
im = pyautogui.screenshot()

im2 = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)
cv2.imwrite(filename, im2)