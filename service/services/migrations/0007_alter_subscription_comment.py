# Generated by Django 3.2.16 on 2024-10-08 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_subscription_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='comment',
            field=models.CharField(db_index=True, default='', max_length=50),
        ),
    ]
