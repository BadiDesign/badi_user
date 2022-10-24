from os import getenv

import requests

SMS_SEND_URL = getenv('SMS__IP_PANEL_URL')
ORIGINATOR = getenv('SMS__IP_PANEL_ORGINATOR')
SMS_ENABLE = getenv('SMS__ENABLE')
SMS__IPPANEL_F_NUM_VERIFY_CODE = getenv('SMS__IPPANEL_F_NUM_VERIFY_CODE')
SMS__IPPANEL_P_ID_VERIFY_CODE = getenv('SMS__IPPANEL_P_ID_VERIFY_CODE')


class IpPanelSms:

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def send_forgot_link(self, pattern_code, values):
        print(f'Send Sms {str(values)}')
        if not SMS_ENABLE:
            return
        for i in range(10):
            try:
                requests.post(
                    SMS_SEND_URL,
                    json={
                        "originator": ORIGINATOR,
                        "recipient": self.phone_number,
                        "pattern_code": pattern_code,
                        "values": values
                    }, headers={
                        "Content-Type": "application/json",
                        "Authorization": ORIGINATOR
                    })
                return True
            except Exception as e:
                print(e)
        return False

    def send_verify_code(self, text):
        print(f'Send code {str(text)}')
        if not SMS_ENABLE:
            return
        for i in range(10):
            try:

                x = requests.get(
                    SMS_SEND_URL,
                    params={
                        "apikey": ORIGINATOR,
                        "fnum": SMS__IPPANEL_F_NUM_VERIFY_CODE,
                        "tnum": self.phone_number,
                        "pid": SMS__IPPANEL_P_ID_VERIFY_CODE,
                        "p1": "v-code",
                        "v1": text
                    }, headers={
                        "Content-Type": "application/json",
                    })
                print(x)
                return True
            except Exception as e:
                print(e)
        return False
