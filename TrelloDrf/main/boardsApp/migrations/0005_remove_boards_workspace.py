# Generated by Django 4.1 on 2022-08-19 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boardsApp', '0004_alter_boards_background_alter_boards_column_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boards',
            name='workspace',
        ),
    ]
