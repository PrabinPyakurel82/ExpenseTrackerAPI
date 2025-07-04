from django.contrib.auth.models import User

from rest_framework import serializers

from .models import ExpenseIncome


class UserSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','password','email','first_name','last_name']


    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            email = validated_data.get('email',''),
            first_name = validated_data.get('first_name',''),
            last_name = validated_data.get("last_name",'')

            )
        return user


class ExpenseIncomeListSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseIncome
        fields = [
            'id', 'title', 'amount', 'transaction_type',
            'total', 'created_at'
        ]

    def get_total(self, obj):
        return obj.total_amount
    

class ExpenseIncomeDetailSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseIncome
        fields = [
            'id', 'title', 'description', 'amount', 'transaction_type',
            'tax', 'tax_type', 'total', 'created_at', 'updated_at'
        ]

    def get_total(self, obj):
        return obj.total_amount
