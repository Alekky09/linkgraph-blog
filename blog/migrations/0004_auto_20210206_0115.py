# Generated by Django 3.1.6 on 2021-02-06 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210206_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
