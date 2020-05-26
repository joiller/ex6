from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .models import *
from django.shortcuts import redirect


class MyMiddleware(MiddlewareMixin):

    # def __init__(self, get_response):
    #     self.get_response = get_response
    #     print('init')

    def get_account(self, request):
        if 'acc' in request.COOKIES:
            account = Account.objects.filter(name=request.COOKIES['acc'])
            if account:
                return account[0]
            else:
                if request.path not in ['', 'login/', 'register/']:
                    return redirect('login/')
            return None

    def process_request(self, request):

        if request.path not in ['/', '/login/']:
            if self.get_account(request):
                request.account = self.get_account(request)
            else:
                return redirect('/login/')

