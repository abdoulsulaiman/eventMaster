# Generated by Django 4.2.6 on 2024-03-29 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_event_will_be_there_alter_event_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]