from os import getenv

import requests

SMS_PANNEL_TYPE = getenv('SMS_PANNEL_TYPE', 'ippanel')

SMS_SEND_URL = getenv('SMS__IP_PANEL_URL')
SMS_POST_URL = getenv('SMS_POST_URL', 'http://ippanel.com/api/select')
ORIGINATOR = getenv('SMS__IP_PANEL_ORGINATOR')
SMS__USERNAME = getenv('SMS__USERNAME')
SMS__PASSWORD = getenv('SMS__PASSWORD')
SMS_ENABLE = getenv('SMS__ENABLE')
SMS__IPPANEL_F_NUM_VERIFY_CODE = getenv('SMS__IPPANEL_F_NUM_VERIFY_CODE')
SMS__IPPANEL_P_ID_VERIFY_CODE = getenv('SMS__IPPANEL_P_ID_VERIFY_CODE')
SMS__IPPANEL_P_ID_FORGOT_LINK = getenv('SMS__IPPANEL_P_ID_FORGOT_LINK')
SMS__IPPANEL_PATTERN_CODE_FORGOT_LINK = getenv('SMS__IPPANEL_PATTERN_CODE_FORGOT_LINK')
SMS__IPPANEL_PARAM_NAME = getenv('SMS__IPPANEL_PARAM_NAME', "v-code")
SMS__IPPANEL_FORGOT_LINK_V1 = getenv('SMS__IPPANEL_FORGOT_LINK_V1', "token")
SMS__IPPANEL_FORGOT_LINK_V2 = getenv('SMS__IPPANEL_FORGOT_LINK_V2', "hash")
SMS__IPPANEL_FROM_NUMBER_FORGOT_LINK = getenv('SMS__IPPANEL_FROM_NUMBER_FORGOT_LINK', SMS__IPPANEL_F_NUM_VERIFY_CODE)


class IpPanelSms:

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def send_forgot_link(self, token_id_hash, hash_code):
        print(f'Send send_forgot_link', token_id_hash, hash_code)
        if not SMS_ENABLE:
            return
        for i in range(10):
            try:
                result = requests.get(
                    SMS_SEND_URL,
                    params={
                        "apikey": ORIGINATOR,
                        "fnum": SMS__IPPANEL_F_NUM_VERIFY_CODE,
                        "tnum": self.phone_number,
                        "pid": SMS__IPPANEL_PATTERN_CODE_FORGOT_LINK,
                        "p1": SMS__IPPANEL_FORGOT_LINK_V1,
                        "v1": str(token_id_hash),
                        "p2": SMS__IPPANEL_FORGOT_LINK_V2,
                        "v2": str(hash_code),
                    }, headers={
                        "Content-Type": "application/json",
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
                        "p1": SMS__IPPANEL_PARAM_NAME,
                        "v1": text
                    }, headers={
                        "Content-Type": "application/json",
                    })
                print(x)
                return True
            except Exception as e:
                print(e)
        return False

    def send_custom(self, params):
        print(f'Send send_custom', params)
        if not SMS_ENABLE:
            return
        for i in range(10):
            try:
                default_params = {
                    "apikey": ORIGINATOR,
                    "fnum": SMS__IPPANEL_F_NUM_VERIFY_CODE,
                    "tnum": self.phone_number,
                }
                default_params.update(params)
                result = requests.get(
                    SMS_SEND_URL,
                    params=default_params, headers={
                        "Content-Type": "application/json",
                    })
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
            return
        for i in range(10):
            try:
                default_params = {
                    "apikey": ORIGINATOR,
                    "fnum": SMS__IPPANEL_F_NUM_VERIFY_CODE,
                    "tnum": self.phone_number,
                }
                default_params.update(params)
                result = requests.get(
                    SMS_SEND_URL,
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
