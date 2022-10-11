import json
import requests
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from badi_utils.dynamic_api import CustomValidation
from badi_utils.responses import ResponseNotOk, ResponseOk
from django.conf import settings
from django.apps import apps as django_apps

BankTransaction = django_apps.get_model(getattr(settings, "BANK_TRANSACTION_MODEL"), require_ready=False)
Transaction = django_apps.get_model(getattr(settings, "TRANSACTION_MODEL"), require_ready=False)

ZP_CONFIG = getattr(settings, "ZP_CONFIG", {})

MERCHANT = ZP_CONFIG.get("MERCHANT")
ZP_API_REQUEST = ZP_CONFIG.get("MERCHANT", "https://api.zarinpal.com/pg/v4/payment/request.json")
ZP_API_VERIFY = ZP_CONFIG.get("MERCHANT", "https://api.zarinpal.com/pg/v4/payment/verify.json")
ZP_API_STARTPAY = ZP_CONFIG.get("MERCHANT", "https://www.zarinpal.com/pg/StartPay/{authority}")
CallbackURL = ZP_CONFIG.get("MERCHANT", '/dashboard/wallet/zp_verify')


class ZPBankAction:
    bankError = _("The operation encountered an error. Please try again."
                  " If the amount is deducted from your account, it will be returned to your account within 72 hours.")

    def send_request(self, request, amount, mobile='', email=''):
        description = ' شارژ حساب کاربری ' + request.user.get_full_name()
        baseUrl = request._request.META.get('HTTP_ORIGIN') if request._request.META.get(
            'HTTP_ORIGIN') else 'https://iscconferences.ir/'
        amount = int(amount) * 10
        if amount < 10000:
            raise CustomValidation('amount', 'حداقل مبلغ قابل شارژ 10,000 تومان می باشد')

        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "callback_url": baseUrl + CallbackURL,
            "description": description,
            "metadata": {"mobile": mobile, "email": email}
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json"}
        try:
            req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
                req_data), headers=req_header)
            req_json = req.json()
        except:
            raise CustomValidation('request_error', 'مشکلی پیش آمده است لطفا دوباره تلاش کنید.')
        if len(req_json['errors']) == 0:
            authority = req_json['data']['authority']
            trans = BankTransaction(
                authority=authority,
                description=description,
                is_verified=False,
                ref_id=None,
                user=request.user,
                amount=amount,
                data=str(req_json)
            )
            trans.save()
            return ResponseOk(data={
                'redirect': ZP_API_STARTPAY.format(authority=authority)
            })
        else:
            e_message = req_json['errors']['message']
            return ResponseNotOk(reason={
                'error': e_message})

    def verify(self, request):
        t_status = request.GET.get('Status')
        t_authority = request.GET.get('Authority')
        trans = BankTransaction.objects.filter(authority=t_authority).first()
        if not trans or t_authority:
            return ResponseNotOk(reason={
                'error': self.bankError})
        if t_status == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": trans.amount,
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    trans.is_verified = True
                    trans.ref_id = req.json()['data']['ref_id']
                    trans.save()
                    if not Transaction.objects.filter(bank_transaction=trans).first():
                        transAction = Transaction(
                            user=trans.user,
                            amount=trans.amount,
                            type='1',
                            subject='شارژ حساب کاربری',
                            bank_transaction=trans,
                        )
                        transAction.save()
                        trans.user.amount += trans.amount
                        trans.user.save()
                    return ResponseOk({
                        'ref_id': req.json()['data']['ref_id']
                    })
                elif t_status == 101:
                    trans.message = req.json()['data']['message']
                    trans.save()
                    return ResponseNotOk(reason={
                        'error': req.json()['errors']['message']})
                else:
                    return ResponseNotOk(reason={
                        'error': self.bankError})
            else:
                return ResponseNotOk(reason={
                    'error': req.json()['errors']['message']})
        else:
            return ResponseNotOk(reason={
                'error': 'تراکنش لغو شد'})

    def get_bank_response(self, request, t_status, t_authority):
        if not t_status or not t_authority:
            return render(request, 'transaction/transaction_result.html', {
                'state': False,
                'error': _("Invalid Data"),
            })
        trans = BankTransaction.objects.filter(authority=t_authority).first()
        if not trans:
            return render(request, 'transaction/transaction_result.html', {
                'state': False,
                'error': self.bankError})
        if t_status == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": trans.amount,
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    trans.is_verified = True
                    trans.ref_id = req.json()['data']['ref_id']
                    trans.save()
                    if not Transaction.objects.filter(bank_transaction=trans).first():
                        transAction = Transaction(
                            user=trans.user,
                            amount=trans.amount,
                            type='1',
                            subject=_("Charge"),
                            bank_transaction=trans,
                        )
                        transAction.save()
                        trans.user.amount += trans.amount
                        trans.card_hash = req.json()['data']['card_pan']
                        trans.ref_id = req.json()['data']['ref_id']
                        trans.user.save()
                        trans.save()
                    return render(request, 'transaction/transaction_result.html', {
                        'state': True,
                        'transaction': {
                            'card': trans.card_hash,
                            'ref_id': trans.ref_id,
                            'amount': trans.amount,
                            'user': trans.user.get_full_name(),
                        },
                    })
                elif t_status == 101:
                    trans.message = req.json()['data']['message']
                    trans.save()
                    return render(request, 'transaction/transaction_result.html', {
                        'state': False,
                        'error': req.json()['errors']['message']})
                else:
                    return render(request, 'transaction/transaction_result.html', {
                        'state': False,
                        'error': self.bankError})
            else:
                return render(request, 'transaction/transaction_result.html', {
                    'state': False,
                    'error': req.json()['errors']['message']})
        else:
            return render(request, 'transaction/transaction_result.html', {
                'state': False,
                'error': _("Transaction canceled")})
