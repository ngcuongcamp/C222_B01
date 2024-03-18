import pytesseract
import cv2
import numpy as np
import pytesseract
import pyscreeze
from utilities import cmd_printer
from skimage.metrics import structural_similarity as ssim
import pyautogui
import time


def capture_screen(position):
    # position = (
    #     position.left,
    #     position.top,
    #     (position.right - position.left),
    #     (position.bottom - position.top),
    # )
    """TODO
    Su dung de hinh anh man hinh theo toa do (left, top, right, bottom)
    @position: toa do (L,T,R,B) *type: `Array`
    @return: hinh anh *type `numpy array`
    """
    position = (
        position[0],
        position[1],
        (position[2] - position[0]),
        (position[3] - position[1]),
    )
    try:
        screenshot = pyscreeze.screenshot(region=position)
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        return screenshot

    except Exception as E:
        print(E)


#


def compare_image_ssim(img1, img2):
    try:
        similarity_index, _ = ssim(
            img1,
            img2,
            full=True,
        )
        percent_matching = round(float(similarity_index), 3)
        print("percent matching: ", percent_matching)

        # if percent matching smaller than 1.0 -> two images deference true
        # equal 1.0 -> same -> return false
        # if percent_matching < 1.0:
        if percent_matching < 0.98:
            return False
        elif percent_matching >= 0.98:
            return True
        else:
            print("Throw error when compare two images")

    except Exception as E:
        print(E)


def lookup_screenshot(self, template):
    """TODO
    Su dung de tim kiem  `template` xuat hien tren man hinh chinh
    @template : *`type: numpy array`
    @return : *`type: boolean`
    """
    try:
        position = pyscreeze.locateOnScreen(
            image=template,
            # region=None,
            # L229, T44, R826, B493
            # region=(229, 44, 826, 493),
            # region=(
            #     self.MES_AREA_SNAPSHOT_POSITION[0],
            #     self.MES_AREA_SNAPSHOT_POSITION[1],
            #     self.MES_AREA_SNAPSHOT_POSITION[2],
            #     self.MES_AREA_SNAPSHOT_POSITION[3],
            # ),
            region=(
                self.MES_SN_INPUT_POSITION[0] - 25,
                self.MES_SN_INPUT_POSITION[1] - 25,
                self.MES_SN_INPUT_POSITION[2] + 25,
                self.MES_SN_INPUT_POSITION[3] + 25,
            ),
            grayscale=True,
            confidence=self.MES_COMPARE_CONFIDENCE,
            minSearchTime=0,
        )
        if position:
            print(position)
            return True
    except Exception as E:
        print(E)
        return False


def convert_image_to_string(image):
    pytesseract.pytesseract.tesseract_cmd = r"./libs/Tesseract-OCR/tesseract.exe"
    # config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ</"
    # config = r"--oem 3 --psm 6 outputbase digits tessedit_char_whitelist=0123456789"
    # config = r"--oem 3 --psm 6"
    # config = (
    #     "--psm 10 --oem 3 -c outputbase digits tessedit_char_whitelist=0123456789</"
    # )
    config = "--oem 3 --psm 6 -c outputbase digits tessedit_char_whitelist=0123456789</"
    try:
        # str_label = pytesseract.image_to_string(screenshot, config=config)
        # txt_result = str_label.strip().split(" ")[-1]
        # return txt_result
        str_label = pytesseract.image_to_string(image, config=config)
        cmd_printer("SUCCESS", str_label)
        return str_label
    except Exception as E:
        print("Error while convert image to string", E)


def capture_by_position(position):
    """
    TODO: `@position` parameter is an array like [LEFT, TOP, RIGHT, BOTTOM]
    @return an gray image <np.array> type
    """
    position = (
        position[0],
        position[1],
        (position[2] - position[0]),
        (position[3] - position[1]),
    )
    try:
        screenshot = pyscreeze.screenshot(region=position)
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        return screenshot

    except Exception as E:
        print("Error while capture screen", E)
