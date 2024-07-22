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


    def launch_hot(self, link, sleep_before_launch=3, tries_count=30):
        time.sleep(2)
        old_windows = list(self.app.windows())

        for i in range(tries_count):
            self.write_to_saved_messages(link)
            time.sleep(sleep_before_launch)
            if click_on_img(self.main_window, 'templates\\hot\\launch.png', 0.5, 2, 0.9):
                break

        for i in range(tries_count):
            if get_img_coords(self.main_window, 'templates\\hot\\allow_msg.png', 0.5, 10, 0.9):
                click_on_img(self.main_window, 'templates\\hot\\OK.png', 0.5, 5, 0.9)

            new_windows = list(self.app.windows())
            if len(new_windows) > len(old_windows):
                unique_windows = [w for w in new_windows if w not in old_windows]
                self.hot_window = unique_windows[0]
                if self.hot_window:
                    logger.info('HOT window successfully launched!')
                    return True
            time.sleep(1)

        raise Exception('HOT window do not launched.')
    

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


    def open_dev_tools(self, wait):
        if self.hot_window is None:
            print('No HOT window!')
            return 0

        click_on_img(self.hot_window, 'templates\\hot\\main_page_arrow.png', 0.5, 5, 0.9)
        time.sleep(0.5)
        send_keys("{F12}")
        time.sleep(1)

        self.devtools = DevTools()
        

    def collect_data(self):
        data = self.devtools.prepare_and_get_tgWebAppData()
        print(data)
