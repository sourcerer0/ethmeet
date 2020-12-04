import sys
from time import sleep
from clockwork import Clockwork
from selenium import webdriver
from datetime import timedelta

def assert_meeting_code(meeting_code, min_len, max_len):
    try: meeting_code + "STRING_TEST"
    except TypeError:
        print("Meeting code must be string!")
        sys.exit(0)

    code_len = len(meeting_code)
    if code_len != max_len and code_len != min_len:
        print("Meeting code not accepted! Please check again")
        sys.exit(0)
    elif (code_len == max_len and meeting_code[3] == "-" and meeting_code[8] == "-") or code_len == min_len:
        for crc in meeting_code:
            try:
                int(crc)
                print("Numbers are not accepted!")
                sys.exit(0)
            except ValueError: continue
        return "https://meet.google.com/%s" % meeting_code

class AttendClass(Clockwork):
    def __init__(self, code, **kwargs):
        super().__init__(**kwargs)
        self.MEET_URL = assert_meeting_code(code, 10, 12)
        self.driver = webdriver.Chrome()

    def run(self):
        print(__name__, "started!")
        print("Process scheduled to", self.__target.format_datetime(), "\n")
        while True:
            print(self.get_time().format_datetime(), end="\r")
            if self.__time_now == self.__target or self.__time_now > self.__target:
                print("Time reached\nStarting process...")
                try:
                    self.execute()
                except:
                    print("ERROR TRYING TO GET URL")
                    sys.exit(0)
                finally:
                    self.shutdownConnection()
            sleep(1)

    def execute(self, **kwargs):
        self.driver.get(self.MEET_URL)
        return

    def shutdownConnection(self, **kwargs):
        self._Clockwork__target = self.get_time() + timedelta(hours=10, minutes=30)
        while True:
            if self.get_time() == self._Clockwork__target:
                self.driver.close()
                break
            sleep(1)
        return
