from django.db import transaction

from rest_framework import serializers

from core.apps.finance.models import Income


class IncomeListSerializer(serializers.ModelSerializer):
    cash_transaction = serializers.SerializerMethodField(method_name='get_cash_transaction')
    payment_type = serializers.SerializerMethodField(method_name='get_payment_type')
    project_folder = serializers.SerializerMethodField(method_name='get_project_folder')
    project = serializers.SerializerMethodField(method_name='get_project')
    counterparty = serializers.SerializerMethodField(method_name='get_counterparty')
    type_income = serializers.SerializerMethodField(method_name='get_type_income')
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = Income
        fields = [
            'id', 'cash_transaction', 'payment_type', 'project_folder', 'project',
            'counterparty', 'type_income', 'currency', 'price', 'exchange_rate', 'date',
            'comment', 'file', 'audit', 'user'
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
        } if obj.project_folder else None
    
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
    
    def get_type_income(self, obj):
        return {
            'id': obj.type_income.id,
            'name': obj.type_income.name
        } if obj.type_income else None

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
        } if obj.user else None


class IncomeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            'cash_transaction', 'payment_type', 'project_folder', 'project',
            'counterparty', 'type_income', 'currency', 'price', 'exchange_rate', 'date',
            'comment', 'file', 'audit'
        ]

    def create(self, validated_data):
        with transaction.atomic():
            income = Income.objects.create(
                user=self.context.get('user'),
                cash_transaction=validated_data['cash_transaction'],
                payment_type=validated_data['payment_type'],
                project_folder=validated_data.get('project_folder'),
                project=validated_data.get('project'),
                counterparty=validated_data.get('counterparty'),
                type_income=validated_data.get('type_income'),
                currency=validated_data.get('currency'),
                price=validated_data.get('price') * validated_data.get('exchange_rate') if validated_data.get('exchange_rate') else validated_data.get('price'),
                exchange_rate=validated_data.get('exchange_rate'),
                date=validated_data.get('date'),
                comment=validated_data.get('comment'),
                file=validated_data.get('file'),
                audit=validated_data.get('audit')
            )
            cash_transaction = income.cash_transaction
            payment_type = income.payment_type

            if validated_data.get('currency') == 'uzs':
                cash_transaction.income_balance_uzs += income.price
                cash_transaction.total_balance_uzs = cash_transaction.income_balance_uzs - cash_transaction.expence_balance_uzs
                payment_type.total_uzs += income.price
            
                if income.counterparty:
                    if income.counterparty.debit_uzs != 0:
                        income.counterparty.debit_uzs -= income.price 
                        income.counterparty.total_debit -= income.price

                        income.counterparty.kredit_uzs += income.counterparty.debit_uzs - income.price
                        income.counterparty.total_kredit += income.price
                    else:
                        income.counterparty.kredit_uzs += income.price
                        income.counterparty.total_kredit += income.price
                    income.counterparty.save()

            elif validated_data.get('currency') == 'usd':
                cash_transaction.income_balance_usd += income.price
                cash_transaction.total_balance_usd = cash_transaction.income_balance_usd - cash_transaction.expence_balance_usd
                payment_type.total_usd += income.price
                if income.counterparty:
                    if income.counterparty.debit_usd != 0:
                        income.counterparty.debit_usd -= validated_data.get('price')
                        income.counterparty.total_debit -= income.price

                        income.counterparty.kredit_usd += income.counterparty.debit_usd - validated_data.get('price')
                        income.counterparty.total_kredit += income.price
                    else:
                        income.counterparty.kredit_usd += validated_data.get('price')
                        income.counterparty.total_kredit += income.price
                    income.counterparty.save()

            cash_transaction.save()
            payment_type.save()
            return income