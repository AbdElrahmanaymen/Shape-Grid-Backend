# Generated by Django 4.2.9 on 2024-01-09 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_rename_user_shapegallery"),
    ]

    operations = [
        migrations.RenameModel(old_name="ShapeGallery", new_name="Shape",),
    ]