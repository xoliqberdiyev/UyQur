from django.core.management.base import BaseCommand

from core.apps.accounts.models.permission import PermissionToTab


class Command(BaseCommand):
    help = "Creates intial tab permission entries"

    def handle(self, *args, **options):
        permissions = [
            {'code': 'order', 'name': "Buyurtmalar"},
            {'code': 'offer', 'name': "Takliflar"},
            {'code': 'party', 'name': "Partiyalar"},
            {'code': 'warehouse', 'name': "Omborxona"},
            {'code': 'transfer', 'name': "O'tkazmalar"},
            {'code': 'invalid', 'name': "Yaroqsiz"},
            {'code': 'income', 'name': "Kirim"},
            {'code': 'expence', 'name': "Chiqim"},
            {'code': 'income_contract', 'name': 'Kirim shartnoma'},
            {'code': 'expence_contract', 'name': 'Chiqim shartnoma'},
        ]

        for perm in permissions:
            obj, created = PermissionToTab.objects.get_or_create(
                code=perm['code'], name=perm['name']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {perm['code']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {perm['code']}"))