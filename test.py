import requests
import os
import re
import time
from requests.exceptions import RequestException
from datetime import datetime

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""  __  __                          
 |  \/  |___ ______ __ _ __ _ ___ 
 | |\/| / -_|_-<_-</ _` / _` / -_)
 |_|  |_\___/__/__/\__,_\__, \___|
                        |___/
""")

class Main:
    def __init__(self) -> None:
        pass

    def inputs(self):
        try:
            banner()
            with open("cookies.txt", 'r') as cookies_file:
                self.your_cookies = cookies_file.read().splitlines()
                if len(self.your_cookies) == 0:
                    print("[Error] the cookies file that you entered is empty")
                    exit()
            self.send_from_multiple_accounts = len(self.your_cookies) > 1
            with open("conversation_id.txt", 'r') as conversation_id_file:
                message_ids = int(conversation_id_file.read().strip())
            with open("timer.txt", 'r') as timer_file:
                delay = int(timer_file.read().strip())
            print(" ")
            while True:
                try:
                    with open("message.txt", 'r') as message_file:
                        message = message_file.read().strip()
                        for cookies in self.your_cookies:
                            time.sleep(delay)
                            self.send_message(cookies, message_ids, message, delay)
                except RequestException as e:
                    print(f"[Error] {str(e).lower()}")
                    continue
                except Exception as e:
                    print(f"[Error] {str(e).lower()}")
                    continue
                except KeyboardInterrupt:
                    break
        except Exception as e:
            print(f"[Error] {str(e).lower()}")
            exit()

    def send_message(self, cookies, message_ids, teks, delay):
        with requests.Session() as r:
            r.headers.update({
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-fetch-site': 'none',
                'accept-language': 'id,en;q=0.9',
                'Host': 'mbasic.facebook.com',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-encoding': 'gzip, deflate',
                'sec-fetch-mode': 'navigate',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'connection': 'keep-alive',
            })

            response = r.get('https://mbasic.facebook.com/messages/t/{}/'.format(message_ids), cookies={
                "cookie": cookies
            })

            self.next_action = re.search('method="post" action="(.*?)"', response.text).group(1).replace('amp;', '')
            self.fb_dtsg = re.search('name="fb_dtsg" value="(.*?)"', response.text).group(1)
            self.jazoest = re.search('name="jazoest" value="(\d+)"', response.text).group(1)
            self.tids = re.search('name="tids" value="(.*?)"', response.text).group(1)
            self.csid = re.search('name="csid" value="(.*?)"', response.text).group(1)

            data = {
                'fb_dtsg': self.fb_dtsg,
                'tids': self.tids,
                'jazoest': self.jazoest,
                'csid': self.csid,
                'body': teks,
                'wwwupp': 'C3',
                'cver': 'legacy',
                'send': 'Kirim',
            }
            r.headers.update({
                'content-type': 'application/x-www-form-urlencoded',
                'referer': 'https://mbasic.facebook.com/messages/t/{}/'.format(message_ids),
                'origin': 'https://mbasic.facebook.com',
            })
            response2 = r.post('https://mbasic.facebook.com{}'.format(self.next_action), data=data, cookies={
                "cookie": cookies
            })

            if 'send_success' in str(response2.url) and response2.status_code == 200:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"""Status : Your Message Sent Successfully by Error Rulex 3:) 🤖
Time   : {current_time}
Teks   : {teks}
""")
            else:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"""Status : Failed <3 :(
Time   : {current_time}
Teks   : {teks}
""")

Main().inputs()
