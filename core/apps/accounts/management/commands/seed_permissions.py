from django.core.management.base import BaseCommand

from core.apps.accounts.models.permission import Permission


class Command(BaseCommand):
    help = "Creates intial permission entries"

    def handle(self, *args, **options):
        permissions = [
            {"code": "project", "name": "project all access"},
            {
                "code": "project_folder",
                "name": "project folder all access"
            },
            {'code': 'delete_user', "name": 'can delete user permissions'},
            {'code': 'user', 'name': 'all user access'},
            {'code': 'settings', 'name': 'all settings access'},
            {'code': 'product_folder', 'name': 'all access to product folder'},
            {'code': 'product', 'name': 'all access to product'},
            {'code': 'order', 'name': 'all access to orders'},
            {'code': 'offer', 'name': 'all access to offers'},
            {'code': 'party', 'name': 'all access to partyies'},
            {'code': '', 'name': 'kataloglar'},
            {'code': '', 'name': 'kassa'},
            {'code': '', 'name': 'moliya'},
            {'code': '', 'name': 'arxiv'},
        ]

        for perm in permissions:
            obj, created = Permission.objects.get_or_create(
                code=perm['code'], name=perm['name']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {perm['code']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {perm['code']}"))
                