# Generated by Django 5.0.6 on 2024-05-31 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("queue_app", "0003_queueentry_desk"),
    ]

    operations = [
        migrations.AddField(
            model_name="queueentry",
            name="served",
            field=models.BooleanField(default=False),
        ),
    ]
