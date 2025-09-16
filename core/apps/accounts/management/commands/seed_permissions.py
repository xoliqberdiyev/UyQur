from django.core.management.base import BaseCommand

from core.apps.accounts.models.permission import Permission


class Command(BaseCommand):
    help = "Creates intial permission entries"

    def handle(self, *args, **options):
        permissions = [
            {'code': 'supply', 'name': "Ta'minot"},
            {'code': 'counterparty', 'name': "Kontragent"},
            {'code': 'warehouse', 'name': "Omborxona"},
            {'code': 'project', 'name': "Loyiha"},
            {'code': 'cash_transaction', 'name': "Kassa"},
            {'code': 'directory', 'name': "Katalog"},
            {'code': 'finance', 'name': "Moliya"},
            {'code': 'archive', 'name': "Arxiv"},
        ]

        for perm in permissions:
            obj, created = Permission.objects.get_or_create(
                code=perm['code'], name=perm['name']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {perm['code']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {perm['code']}"))