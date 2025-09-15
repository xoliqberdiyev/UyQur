from django.db import transaction

from rest_framework import serializers

from core.apps.finance.models import ExpenceContract


class ExpenceContractSerializer(serializers.ModelSerializer):
    project_folder = serializers.SerializerMethodField(method_name='get_project_folder')
    project = serializers.SerializerMethodField(method_name='get_project')
    expence_type = serializers.SerializerMethodField(method_name='get_expence_type')
    counterparty = serializers.SerializerMethodField(method_name='get_counterparty')
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = ExpenceContract
        fields = [
            'id', 'project_folder', 'project', 'expence_type', 'counterparty', 'price', 
            'currency', 'date', 'comment', 'user'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name
        } if obj.user else None

    def get_counterparty(self, obj):
        return {
            'id': obj.counterparty.id,
            'name': obj.counterparty.name,
        } if obj.counterparty else None
    
    def get_expence_type(self, obj):
        return {
            'id': obj.expence_type.id,
            'name': obj.expence_type.name
        } if obj.expence_type else None
    
    def get_project(self, obj):
        return {
            'id': obj.project.id,
            'name': obj.project.name
        } if obj.project else None

    def get_project_folder(self, obj):
        return {
            'id': obj.project_folder.id,
            'name': obj.project_folder.name
        } if obj.project_folder else None


    def create(self, validated_data):
        with transaction.atomic():
            expence_contract = ExpenceContract.objects.create(
                project_folder=validated_data.get('project_folder'),
                project=validated_data.get('project'),
                expence_type=validated_data.get('expence_type'),
                counterparty=validated_data.get('counterparty'),
                price=validated_data.get('price'),
                currency=validated_data.get('currency'),
                date=validated_data.get('date'),
                comment=validated_data.get('comment'),
                user=self.context.get('user'),
            )
            return expence_contract

