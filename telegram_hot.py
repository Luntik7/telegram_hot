from telegram import TelegramApp
import time
from img_detection import *
from devtools import *
from pywinauto.keyboard import send_keys


class TelegramAppHOT(TelegramApp):
    def __init__(self, exe_path):
        super().__init__(exe_path)
        self.hot_window = None
        self.devtools = None


    def launch_hot(self, link, timeout=30):
        self.hot_window = self.launch_app(
            'templates\\hot\\launch.png',
            'templates\\hot\\allow_msg.png',
            'templates\\hot\\OK.png',
            link,
            "Hot",
        )
    

    def change_referal(self, count):
        with open('tmp.txt', 'r', encoding='utf-8') as fileobj:
            ref_list = fileobj.readlines()
        new_ref = ref_list[count].strip()

        click_on_img(self.hot_window, 'templates\\hot\\hot_settings.png', 0.5, 5, 0.9)
        click_on_img(self.hot_window, 'templates\\hot\\recover_inviter.png', 0.5, 5, 0.9)
        click_on_img(self.hot_window, 'templates\\hot\\inviter_address.png', 0.5, 5, 0.9)
        self.enter_new_text(new_ref)
        logger.info(f"Recovered referal - {new_ref}")
        time.sleep(1)
        if not click_on_img(self.hot_window, 'templates\\hot\\change_inviter.png', 0.5, 10, 0.9):
            raise Exception('Referal not changed')


    def open_hot_dev_tools(self, wait=30):
        self.devtools = self.open_dev_tools(self.hot_window, 'templates\\hot\\main_page_arrow.png', "Hot")
        

    def collect_data(self):
        data = self.devtools.prepare_and_get_tgWebAppData()
        print(data)
