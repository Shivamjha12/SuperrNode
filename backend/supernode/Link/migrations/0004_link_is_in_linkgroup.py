# Generated by Django 4.2 on 2024-04-20 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Link', '0003_link_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='is_in_linkGroup',
            field=models.BooleanField(default=False),
        ),
    ]
