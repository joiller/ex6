from django.shortcuts import render
from rest_framework import viewsets, permissions, views, generics, status
from rest_framework.response import Response
from .serializers import *
import json
from django.db import transaction
from jwt import JWT

# Create your views here.


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class AccountRegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Account.objects.all()
    serializer_class = AccountRegisterSerializer


class AccountLoginView(generics.ListCreateAPIView):
    print('login')
    queryset = Account.objects.all()
    serializer_class = AccountLoginSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(request.data)
            account = Account.objects.filter(request.data)
            if account:
                account = JWT.encode(account, key='jhl')
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('account', account)
                return res
            return Response('No this account', status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountProfileView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountProfileSerializer
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()  # 通过look up field 得到一个account instance
        item = self.get_serializer(instance)   # 把account instance 变成serializer
        serializer = self.serializer_class(request.account)  # 把request.account 变成serializer
        res = item.data
        if serializer.data==res:
            return Response(res,status=status.HTTP_200_OK)
        else:
            # 不可以看密码
            del res['password']
            return Response(res, status=status.HTTP_200_OK)


"""""""""交易"""""""""


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PurchaseView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def post(self, request, *args, **kwargs):
        product = request.data['product']
        product = Product.objects.filter(id=product)
        if product:
            product=product[0]
        else:
            return Response('Product Not Exist')

        print(product.volume, request.data['volume'])
        if product.volume>=int(request.data['volume']):

            amount = int(request.data['volume']) * product.price
            if amount> request.account.balance:
                return Response('Money not Enough')

            with transaction.atomic():

                product.volume -= int(request.data['volume'])
                product.save()

                request.account.balance -= amount
                request.account.save()

                purchase = Purchase.objects.create(
                    account=request.account,
                    product=product,
                    amount=amount,
                    volume=request.data['volume']
                )

                print(self.get_serializer(purchase))

                return Response(self.get_serializer(purchase).data, status=status.HTTP_200_OK)

        else:
            return Response('Product Out')


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # lookup_field = 'id'

    # def create(self, request, *args, **kwargs):
    #     return

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(account=request.account)
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def retrieve(self, request, *args, **kwargs):
    #     return Response(self.get_serializer())

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 0 :
            return Response('Cannot be refunded!')
        account = instance.account
        if type(instance) == Charge:
            account.balance += instance.amount
            # account.save()

            serializer2 = AccountSerializer(account)
            self.perform_update(serializer2)

            instance.status = 1
            serializer = self.get_serializer(instance)
            self.perform_update(serializer)
            return Response([serializer2.data, serializer.data], status=status.HTTP_200_OK)

        elif type(instance) == Purchase:
            product = instance.product
            product.volume += instance.volume
            product.save()
            account.balance += instance.amount
            # account.save()

            serializer2 = AccountSerializer(account)
            self.perform_update(serializer2)

            instance.status = 1
            serializer = self.get_serializer(instance)
            self.perform_update(serializer)
            return Response([serializer2.data,serializer.data], status=status.HTTP_200_OK)

        elif type(instance) == Extraction:
            pass

