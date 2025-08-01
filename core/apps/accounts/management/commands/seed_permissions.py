from django.core.management.base import BaseCommand

from core.apps.accounts.models.permission import Permission


class Command(BaseCommand):
    help = "Creates intial permission entries"

    def handle(self, *args, **options):
        permissions = [
            {"code": "can_see_product_wherehouse", "name": "permission for see wherehouse list"},
            {
                "code": "can_add_product_wherehouse",
                "name": "permission for add product in wherehouse"
            }
        ]

        for perm in permissions:
            obj, created = Permission.objects.get_or_create(
                code=perm['code'], name=perm['name']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {perm['code']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {perm['code']}"))
                