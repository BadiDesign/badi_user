from os import getenv

import requests
import json

SMS_PANNEL_TYPE = getenv('SMS_PANNEL_TYPE', 'ippanel')

ORIGINATOR = getenv('SMS__IP_PANEL_ORGINATOR')
SMS_ENABLE = getenv('SMS__ENABLE')
SMS__IPPANEL_P_ID_VERIFY_CODE = getenv('SMS__IPPANEL_P_ID_VERIFY_CODE')
SMS__IPPANEL_PATTERN_CODE_FORGOT_LINK = getenv('SMS__IPPANEL_PATTERN_CODE_FORGOT_LINK')
SMS__IPPANEL_PARAM_NAME = getenv('SMS__IPPANEL_PARAM_NAME', "v-code")
SMS__IPPANEL_FORGOT_LINK_V1 = getenv('SMS__IPPANEL_FORGOT_LINK_V1', "token")
SMS__IPPANEL_FORGOT_LINK_V2 = getenv('SMS__IPPANEL_FORGOT_LINK_V2', "hash")
SMS__IPPANEL_SENDER = getenv('SMS__IPPANEL_SENDER', "3000505")
SMS__IPPANEL_SEND_URL = getenv('SMS__IPPANEL_SEND_URL', "http://api2.ippanel.com/api/v1/sms/pattern/normal/send")
SMS__IPPANEL_SEND_URL_FORGOT = getenv('SMS__IPPANEL_SEND_URL_FORGOT', SMS__IPPANEL_SEND_URL)


class IpPanelSms:

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def send_forgot_link(self, token_id_hash, hash_code):
        print(f'Send send_forgot_link', token_id_hash, hash_code)
        if not SMS_ENABLE:
            print('SMS DISABLED')
            return
        for i in range(10):
            try:
                url = SMS__IPPANEL_SEND_URL_FORGOT
                payload = json.dumps({
                    "code": SMS__IPPANEL_PATTERN_CODE_FORGOT_LINK,
                    "recipient": self.phone_number,
                    "sender": SMS__IPPANEL_SENDER,
                    "variable": {
                        SMS__IPPANEL_FORGOT_LINK_V1: str(token_id_hash),
                        SMS__IPPANEL_FORGOT_LINK_V2: str(hash_code),
                    }
                })
                headers = {
                    'apikey': ORIGINATOR,
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print("Response:", response)
                return True
            except Exception as e:
                print(e)
        return False

    def send_verify_code(self, text):
        print(f'Send code {str(text)}')
        if not SMS_ENABLE:
            print('SMS DISABLED')
            return
        for i in range(10):
            try:
                url = SMS__IPPANEL_SEND_URL
                payload = json.dumps({
                    "code": SMS__IPPANEL_P_ID_VERIFY_CODE,
                    "recipient": self.phone_number,
                    "sender": SMS__IPPANEL_SENDER,
                    "variable": {
                        SMS__IPPANEL_PARAM_NAME: text,
                    }
                })
                headers = {
                    'apikey': ORIGINATOR,
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print("Response:", response)
                return True
            except Exception as e:
                print(e)
        return False

    def send_custom(self, params):
        print(f'Send send_custom', params)
        if not SMS_ENABLE:
            print('SMS DISABLED')
            return
        for i in range(10):
            try:
                url = SMS__IPPANEL_SEND_URL
                payload = {
                    "recipient": self.phone_number,
                    "sender": SMS__IPPANEL_SENDER,
                }
                payload.update(params)
                payload = json.dumps(payload)
                headers = {
                    'apikey': ORIGINATOR,
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print("Response:", response)
                return True
            except Exception as e:
                print(e)
        return False


SMS__PANNEL = getenv('SMS__PANNEL')
SMS__TOKEN = getenv('SMS__TOKEN')
SMS__FORGET_TEMPLATE_ID = getenv('SMS__FORGET_TEMPLATE_ID', 'forget')
SMS__VERIFY_TEMPLATE_ID = getenv('SMS__VERIFY_TEMPLATE', 'entry')
SMS__FORGET_CODE_TEMPLATE_ID = getenv('SMS__FORGET_CODE_TEMPLATE_ID', 'forgetcode')


class KavenegarSms:

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def send_forgot_link(self, token_id_hash, hash_code):
        print(f'Send send_forgot_link', token_id_hash, hash_code)
        if not SMS_ENABLE:
            print('SMS DISABLED')
            return
        for i in range(10):
            try:
                result = requests.get(
                    SMS__PANNEL.format(key=SMS__TOKEN),
                    params={
                        "type": 'sms',
                        "template": SMS__FORGET_TEMPLATE_ID,
                        "receptor": self.phone_number,
                        "token": token_id_hash,
                        "token2": hash_code,
                    }, headers={
                        "Content-Type": "application/json",
                    }
                )
                return True
            except Exception as e:
                print(e)
        return False

    def send_verify_code(self, text):
        print(f'Send code {str(text)}')
        if not SMS_ENABLE:
            print('SMS DISABLED')
            return
        for i in range(10):
            try:
                response = requests.get(
                    SMS__PANNEL.format(key=SMS__TOKEN),
                    params={
                        "type": 'sms',
                        "template": SMS__VERIFY_TEMPLATE_ID,
                        "receptor": self.phone_number,
                        "token": text,
                    }, headers={
                        "Content-Type": "application/json",
                    }
                )
                print(response, response.ok)
                if response.ok:
                    return True
            except Exception as e:
                print(e)
        return False

    def send_forgot_code(self, text):
        print(f'Send Forgot code {str(text)}')
        if not SMS_ENABLE:
            print('SMS DISABLED')
            return
        for i in range(10):
            try:
                response = requests.get(
                    SMS__PANNEL.format(key=SMS__TOKEN),
                    params={
                        "type": 'sms',
                        "template": SMS__FORGET_CODE_TEMPLATE_ID,
                        "receptor": self.phone_number,
                        "token": text,
                    }, headers={
                        "Content-Type": "application/json",
                    }
                )
                print(response, response.ok)
                if response.ok:
                    return True
            except Exception as e:
                print(e)
        return False

    def send_custom(self, params):
        print(f'Send send_custom', params)
        if not SMS_ENABLE:
            print('SMS DISABLED')
            return
        for i in range(10):
            try:
                default_params = {
                    "type": 'sms',
                    "template": SMS__FORGET_CODE_TEMPLATE_ID,
                    "receptor": self.phone_number,
                }
                default_params.update(params)
                result = requests.get(
                    SMS__PANNEL.format(key=SMS__TOKEN),
                    params=default_params, headers={
                        "Content-Type": "application/json",
                    })
                return True
            except Exception as e:
                print(e)
        return False


print('SMS_PANNEL_TYPE got:', SMS_PANNEL_TYPE)
if SMS_PANNEL_TYPE == 'kavenegar':
    SmsManager = KavenegarSms
else:
    SmsManager = IpPanelSms
