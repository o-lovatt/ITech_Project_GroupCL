from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_default_users(apps, schema_editor):
    Role = apps.get_model("accounts", "Role")
    User = apps.get_model("accounts", "User")

    admin_role, _ = Role.objects.get_or_create(role_name="Admin")
    guest_role, _ = Role.objects.get_or_create(role_name="Guest")

    admin_user, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@gmail.com",
            "password": make_password("admin123"),
            "role": admin_role,
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        },
    )

    if not created:
        admin_user.email = "admin@gmail.com"
        admin_user.password = make_password("admin123")
        admin_user.role = admin_role
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()

    guest_user, created = User.objects.get_or_create(
        username="guest",
        defaults={
            "email": "guest@gmail.com",
            "password": make_password("guest123"),
            "role": guest_role,
            "is_staff": False,
            "is_superuser": False,
            "is_active": True,
        },
    )

    if not created:
        guest_user.email = "guest@gmail.com"
        guest_user.password = make_password("guest123")
        guest_user.role = guest_role
        guest_user.is_staff = False
        guest_user.is_superuser = False
        guest_user.is_active = True
        guest_user.save()


def remove_default_users(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(username__in=["admin", "guest"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_auto_20260317_2153"),
    ]

    operations = [
        migrations.RunPython(seed_default_users, remove_default_users),
    ]
