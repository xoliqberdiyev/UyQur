from django.db import transaction

from rest_framework import serializers

from core.apps.finance.models import Expence


class ExpenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expence
        fields = [
            'cash_transaction', 'payment_type', 'project_folder', 'project', 'expence_type',
            'counterparty', 'price', 'exchange_rate', 'currency', 'date', 'comment', 'audit', 'file'
        ]
    
    def create(self, validated_data):
        with transaction.atomic():
            expence = Expence.objects.create(
                cash_transaction=validated_data.get('cash_transaction'),
                payment_type=validated_data.get('payment_type'),
                project_folder=validated_data.get('project_folder'),
                project=validated_data.get('project'),
                expence_type=validated_data.get('expence_type'),
                counterparty=validated_data.get('counterparty'),
                price=validated_data.get('price') * validated_data.get('exchange_rate') if validated_data.get('exchange_rate') else validated_data.get('price'),
                exchange_rate=validated_data.get('exchange_rate'),
                currency=validated_data.get('currency'),
                date=validated_data.get('date'),
                comment=validated_data.get('comment'),
                audit=validated_data.get('audit'),
                file=validated_data.get('file'),
            )
            cash_transaction = expence.cash_transaction
            payment_type = expence.payment_type
        
            if validated_data.get('currency') == 'uzs':
                cash_transaction.expence_balance_uzs += expence.price
                cash_transaction.total_balance_uzs = cash_transaction.income_balance_uzs - cash_transaction.expence_balance_uzs
                if payment_type.total_uzs > expence.price:
                    payment_type.total_uzs -= expence.price
            
                if expence.counterparty:
                    if expence.counterparty.kredit_uzs != 0:
                        expence.counterparty.kredit_uzs -= expence.price 
                        expence.counterparty.total_kredit -= expence.price

                        expence.counterparty.debit_uzs += expence.counterparty.kredit_uzs - expence.price
                        expence.counterparty.total_debit += expence.price
                    else:
                        expence.counterparty.debit_uzs += expence.price
                        expence.counterparty.total_debit += expence.price
            
            elif validated_data.get('currency') == 'usd':
                cash_transaction.expence_balance_usd += expence.price
                cash_transaction.total_balance_usd = cash_transaction.income_balance_usd - cash_transaction.expence_balance_usd
                if payment_type.total_usd > expence.price:
                    payment_type.total_usd -= expence.price
            
                if expence.counterparty:
                    if expence.counterparty.kredit_usd != 0:
                        expence.counterparty.kredit_usd -= validated_data.get('price')
                        expence.counterparty.total_kredit -= expence.price

                        expence.counterparty.debit_usd += expence.counterparty.kredit_usd - validated_data.get('price')
                        expence.counterparty.total_debit += expence.price
                    else:
                        expence.counterparty.debit_usd += validated_data.get('price')
                        expence.counterparty.total_debit += expence.price
            
            cash_transaction.save()
            payment_type.save()
            expence.counterparty.save()
            return expence
        
    
class ExpenceListSerializer(serializers.ModelSerializer):
    cash_transaction = serializers.SerializerMethodField(method_name='get_cash_transaction')
    payment_type = serializers.SerializerMethodField(method_name='get_payment_type')
    project_folder = serializers.SerializerMethodField(method_name='get_project_folder')
    project = serializers.SerializerMethodField(method_name='get_project')
    counterparty = serializers.SerializerMethodField(method_name='get_counterparty')
    expence_type = serializers.SerializerMethodField(method_name='get_expence_type')

    class Meta:
        model = Expence
        fields = [
            'id', 'cash_transaction', 'payment_type', 'project_folder', 'project', 'expence_type',
            'counterparty', 'price', 'exchange_rate', 'currency', 'date', 'comment', 'audit', 'file'
        ]
    
    def get_cash_transaction(self, obj):
        return {
            'id': obj.cash_transaction.id,
            'name': obj.cash_transaction.name
        }
    
    def get_payment_type(self, obj):
        return {
            'id': obj.payment_type.id,
            'name': obj.payment_type.name
        }
    
    def get_project_folder(self, obj):
        return {
            'id': obj.project_folder.id,
            'name': obj.project_folder.name
        }
    
    def get_project(self, obj):
        return {
            'id': obj.project.id,
            'name': obj.project.name
        } if obj.project else None
    
    def get_counterparty(self, obj):
        return {
            'id': obj.counterparty.id,
            'name': obj.counterparty.name
        } if obj.counterparty else None
    
    def get_expence_type(self, obj):
        return {
            'id': obj.expence_type.id,
            'name': obj.expence_type.name
        } if obj.expence_type else None
