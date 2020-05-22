from rest_framework import serializers
from .models import *


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    # name = serializers.CharField(max_length=100, allow_blank=False, required=True)
    # password = serializers.CharField(max_length=100, allow_blank=False, required=True)
    # balance = serializers.IntegerField(default=0)

    account_detail = serializers.HyperlinkedIdentityField(view_name='account-detail')
    # def create(self, validated_data):
    #     return Account.objects.create(**validated_data)

    class Meta:
        model = Account
        fields = [
            'id',
            'created_at',
            'name',
            'account_detail',
            'balance',
            'password'
        ]


class TransactionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='transaction-detail')

    class Meta:
        model = Transaction
        exclude = []


class AccountRegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True
    )

    password = serializers.CharField(
        required=True,
        label='Password',
        style={'input_type': 'password'}
    )

    # password_2 = serializers.CharField(
    #     required=True,
    #     label='Confirm Password',
    #     style={'input_type': 'password'}
    # )

    class Meta:
        model = Account
        fields = ['name', 'password']

    def validate_name(self, value):
        if Account.objects.filter(name=value).exists():
            raise serializers.ValidationError('name exists')
        return value

    def validate_password(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('too short, at least 3')
        return value

    # def validate_password_2(self, value):
    #     data = self.get_initial()
    #     password = data.get('password')
    #     if password!= value:
    #         raise serializers.ValidationError('password not match')
    #     return value

    def create(self, validated_data):
        return validated_data


class AccountLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = Account
        fields = ['id','name', 'password']

    def validate(self, attrs):
        name = attrs.get('name', None)
        password = attrs.get('password', None)

        if not name or not password:
            raise serializers.ValidationError('no name or password')

        account = Account.objects.filter(name=name,password=password)

        if account:
            return attrs
        else:
            raise serializers.ValidationError('wrong name or password')


class AccountProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={
            'input_type': 'password'
        }
    )

    class Meta:
        model = Account
        fields = ['id', 'name', 'password', 'balance']


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    # product_detail = serializers.HyperlinkedIdentityField(view_name='product-detail')

    class Meta:
        model = Product
        exclude = ['creator']
        # fields = ['id', 'created_at', 'name', 'price', 'volume', 'creator', 'product_detail']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        exclude = []


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = []
