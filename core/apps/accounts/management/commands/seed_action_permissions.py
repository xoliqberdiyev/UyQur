from django.core.management.base import BaseCommand

from core.apps.accounts.models.permission import PermissionToAction


class Command(BaseCommand):
    help = "Creates intial permission entries"

    def handle(self, *args, **options):
        permissions = [
            {'code': 'create_order', 'name': "Buyurtma berish"},
            {'code': 'delete_order', 'name': "Buyurtmani o'chirish"},
            {'code': 'update_order', 'name': "Buyurtmani tahrirlash"},
            {'code': 'create_offer', 'name': "Taklif berish"},
            {'code': 'offer_history', 'name': "Takliflar tarixi"},
            {'code': 'history_offer', 'name': "Takliflar tarixi"},
            {'code': 'update_offer', 'name': "Takliflarni tahrirlash"},
            {'code': 'delete_offer', 'name': "Takliflarni o'chirish"},
            {'code': 'create_party', 'name': "Partiya qo'shish"},
            {'code': 'update_party', 'name': "Partiyalarni tahrirlash"},
            {'code': 'delete_party', 'name': "Partiyalarni o'chirish"},
            {'code': 'create_counterparty', 'name': "Kontragent qo'shish"},
            {'code': 'delete_counterparty', 'name': "Kontragentlarni o'chirish"},
            {'code': 'update_counterparty', 'name': "Kontragentlarni tahrirlash"},
            {'code': 'archive_counterparty', 'name': "Kontragentlarni arxivlash"},
            {'code': 'create_counterparty_folder', 'name': "Kontragent papkalar qo'shish"},
            {'code': 'delete_counterparty_folder', 'name': "Kontragent papkalarni o'chirish"},
            {'code': 'update_counterparty_folder', 'name': "Kontragent papkalarni tahrirlash"},
            {'code': 'update_counterparty_folder', 'name': "Kontragent papkalarni tahrirlash"},
            {'code': 'create_warehouse', 'name': "Omborxona qo'shish"},
            {'code': 'update_warehouse', 'name': "Omborxonalarni tahrirlash"},
            {'code': 'delete_warehouse', 'name': "Omborxonalarni o'chirish"},
            {'code': 'create_stock_movemend', 'name': "O'tkazma qilish"},
            {'code': 'update_stock_movemend', 'name': "O'tkazmalarni tahrishlash"},
            {'code': 'delete_stock_movemend', 'name': "O'tkazmalarni o'chirish"},
            {'code': 'create_invalid_product', 'name': "Yaroqsizga chiqarish"},
            {'code': 'update_invalid_product', 'name': "Yaroqsizlarni tahrirlash"},
            {'code': 'cancel_invalid_product', 'name': "Yaroqsizlarni qaytarish"},
            {'code': 'create_project_folder', 'name': "Loyiha papkasini qo'shish"},
            {'code': 'update_project_folder', 'name': "Loyiha papkasini tahrirlash"},
            {'code': 'delete_project_folder', 'name': "Loyiha papkasini o'chirish"},
            {'code': 'create_project', 'name': "Loyiha qo'shish"},
            {'code': 'update_project', 'name': "Loyihani tahrirlash"},
            {'code': 'delete_project', 'name': "Loyihani o'chirish"},
            {'code': 'transfer_project', 'name': "Loyihani ko'chirish"},
            {'code': "create_income", 'name': "Kirim qo'shish"},
            {'code': "delete_income", 'name': "Kirimlarni o'chirish"},
            {'code': "update_income", 'name': "Kirimlarni tahrirlash"},
            {'code': "create_expence", 'name': "Chiqim qo'shish"},
            {'code': "delete_expence", 'name': "Chiqimlarni o'chirish"},
            {'code': "update_expence", 'name': "Chiqimlarni tahrirlash"},
            {'code': 'create_income_contract', 'name': "Kirim shartnoma qo'shish"},
            {'code': 'delete_income_contract', 'name': "Kirim shartnomalarni o'chirish"},
            {'code': 'update_income_contract', 'name': "Kirim shartnomalarni tahrirlash"},
            {'code': 'create_expence_contract', 'name': "Chiqim shartnoma qo'shish"},
            {'code': 'delete_expence_contract', 'name': "Chiqim shartnomalarni o'chirish"},
            {'code': 'update_expence_contract', 'name': "Chiqim shartnomalarni tahrirlash"},
            {'code': 'create_cash_transaction', 'name': "Kassa qo'shish"},
            {'code': 'update_cash_transaction', 'name': "Kassalarni tahrirlash"},
            {'code': 'delete_cash_transaction', 'name': "Kassalarni o'chirish"},
            {'code': 'create_cash_transaction_folder', 'name': "Kassa papka qo'shish"},
            {'code': 'update_cash_transaction', 'name': "Kassa papkalarni tahrirlash"},
            {'code': 'delete_cash_transaction', 'name': "Kassalarni papkalarni o'chirish"},
            {'code': 'create_payment_type', 'name': "To'lov turi qo'shish"},
            {'code': 'delete_payment_type', 'name': "To'lov turi o'chirish"},
            {'code': 'update_payment_type', 'name': "To'lov turi tahrirlash"},
            {'code': 'create_income_type', 'name': "Daromad turi qo'shish"},
            {'code': 'update_income_type', 'name': "Daromad turini tahrirlash"},
            {'code': 'delete_income_type', 'name': "Daromad turini o'chirish"},
            {'code': 'create_expence_type', 'name': "Xarajat turi qo'shish"},
            {'code': 'update_expence_type', 'name': "Xarajat turini tahrirlash"},
            {'code': 'delete_expence_type', 'name': "Xarajat turini o'chirish"},
        ]

        for perm in permissions:
            obj, created = PermissionToAction.objects.get_or_create(
                code=perm['code'], name=perm['name']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {perm['code']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {perm['code']}"))