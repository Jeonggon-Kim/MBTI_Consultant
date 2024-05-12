# Generated by Django 5.0.4 on 2024-05-09 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mbtichat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='text',
            new_name='prompt',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='label',
        ),
        migrations.AddField(
            model_name='chat',
            name='response',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]