# Generated by Django 2.2.4 on 2022-06-26 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0003_auto_20220626_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
