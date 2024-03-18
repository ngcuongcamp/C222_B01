from libs.libs import (
    Desktop,
    pywinauto,
    Application,
    pyautogui,
    keyboard,
)
from utilities import logger, cmd_printer
from UI_handler import set_error_mes_state


def get_name_mes_app(self):
    try:
        top_windows = Desktop(backend=self.MES_BACKEND).windows()
        is_found = False
        for w in top_windows:
            if (
                "login:" in w.window_text().lower()
                and "ver:" in w.window_text().lower()
            ):
                self.MES_APP_NAME = w.window_text()
                is_found = True
                break

        # if is_found == True:
        #     export = pywinauto.findwindows.find_windows(best_match=self.MES_APP_NAME)
        #     if export:
        #         app = Application(backend=self.MES_BACKEND).connect(handle=export[0])
        #         dialog = app.window(title=self.MES_APP_NAME)
        #         txtSN_element = dialog.child_window(auto_id=self.MES_SN_INPUT_ID)
        #         self.MES_SN_INPUT_POSITION = txtSN_element.rectangle()
        #         print("Position of txtSN: ", self.MES_SN_INPUT_POSITION)

        if is_found == False:
            set_error_mes_state(self)
            self.is_processing = True
            print("Can't connect with MES APP")
            logger.error("Can't connect with MES APP")
    except Exception as E:
        # print(E)
        set_error_mes_state(self)


def send_data_to_mes(self, data: str):
    cmd_printer("INFO", "Start send")
    x = 1024 / 2
    y = 768 / 2
    pyautogui.moveTo(x, y)
    pyautogui.typewrite(data)
    pyautogui.moveTo(x, y)
    keyboard.press_and_release("enter")
    cmd_printer("INFO", "End send")
