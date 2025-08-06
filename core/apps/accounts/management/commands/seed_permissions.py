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
        ]

        for perm in permissions:
            obj, created = Permission.objects.get_or_create(
                code=perm['code'], name=perm['name']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {perm['code']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {perm['code']}"))
                