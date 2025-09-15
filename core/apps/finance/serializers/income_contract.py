from django.db import transaction

from rest_framework import serializers

from core.apps.finance.models import IncomeContract


class IncomeContractSerializer(serializers.ModelSerializer):
    project_folder = serializers.SerializerMethodField(method_name='get_project_folder')
    project = serializers.SerializerMethodField(method_name='get_project')
    income_type = serializers.SerializerMethodField(method_name='get_income_type')
    counterparty = serializers.SerializerMethodField(method_name='get_counterparty')
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = IncomeContract
        fields = [
            'id', 'project_folder', 'project', 'income_type', 'counterparty', 'price', 'currency',
            'date', 'comment' , 'user'
        ]
        extra_kwargs = {'id': {'read_only': True}}

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name, 
        } if obj.user else None
    
    def get_counterparty(self, obj):
        return {
            'id': obj.counterparty.id,
            'name': obj.counterparty.name,
        } if obj.counterparty else None

    def get_income_type(self, obj):
        return {
            'id': obj.income_type.id,
            'name': obj.income_type.name
        } if obj.income_type else None

    def get_project(self, obj):
        return {
            'id': obj.project.id,
            'name': obj.project.name,
        } if obj.project else None

    def get_project_folder(self, obj):
        return {
            'id': obj.project_folder.id,
            'name': obj.project_folder.name
        }



class IncomeContractCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeContract
        fields = [
            'id', 'project_folder', 'project', 'income_type', 'counterparty', 'price', 'currency',
            'date', 'comment' 
        ]
        extra_kwargs = {'id': {'read_only': True}}
    
    def create(self, validated_data):
        with transaction.atomic():
            income_contract = IncomeContract.objects.create(
                project_folder=validated_data.get('project_folder'),
                project=validated_data.get('project'),
                income_type=validated_data.get('income_type'),
                counterparty=validated_data.get('counterparty'),
                price=validated_data.get('price'),
                currency=validated_data.get('currency'),
                date=validated_data.get('date'),
                comment=validated_data.get('comment'),
                user=self.context.get('user'),
            )
            return income_contract
        
    
class IncomeContractCalculatePriceSerializer(serializers.Serializer):
    price = serializers.IntegerField()