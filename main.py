import time
from telegram import TelegramApp
from telegram_hot import TelegramAppHOT
from loguru import logger
import random


TRIES_COUNT = 3
CHECK_WEBVIEW_INSPECTIOIN = False
counter = 0


def main_hot(path, ref_link):
    global counter
    if TelegramAppHOT.is_proxifier_running():
        TelegramAppHOT.stop_telegram_processes()
        telegram_app = TelegramAppHOT(path)
        if CHECK_WEBVIEW_INSPECTIOIN:
            telegram_app.turn_on_webview_inspecting()
        telegram_app.launch_hot(ref_link)
        telegram_app.change_referal(counter)
        time.sleep(5)
        
        time.sleep(0.3)
        telegram_app.quit_telegram()
        time.sleep(1)


def main():
    global counter
    # logger.add("file.log", level="DEBUG")
    
    with open('all_refs.txt', 'r', encoding='utf-8') as fileobj:
        ref_links = fileobj.readlines()

    with open('all_pathes.txt', 'r', encoding='utf-8') as fileobj:
        pathes_list = fileobj.readlines()

    for path in pathes_list:
        for i in range(TRIES_COUNT):
            try:
                if path.find('all_telegrams') != -1:
                    short_path = path[path.index('all_telegrams')+13:].strip()
                else:
                    short_path = path[-40:]

                if TelegramApp.is_proxifier_running():
                    TelegramApp.stop_telegram_processes()
                    time.sleep(1)
                    logger.info(f"Start account ...{short_path}")

                    ref_link = random.choice(ref_links).strip()
                    if ref_link.find('?') != -1:
                        logger.info(f"Account referal: {ref_link[ref_link.index('?'):]}")
                    else:
                        logger.info(f"Account referal: {ref_link}")
                    
                    main_hot(path.strip(), ref_link)
                    counter += 1
                    break
                else:
                    logger.warning('Launch proxyfier firstly')
                    return 0
            except Exception as e:
                logger.error(f'Error: {str(e).strip()}')
                logger.warning(f"TRY {i+1}/{TRIES_COUNT}")
                if i+1 < TRIES_COUNT:
                    continue
                else:
                    with open('bad_accounts.txt', 'a', encoding='utf-8') as fileobj:
                        fileobj.write(path + '\n')
                        counter += 1
            finally:
                logger.info(f"Finish account ...{short_path}\n")
    input()


if __name__ == '__main__':
    main()