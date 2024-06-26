# Generated by Django 4.2.6 on 2024-01-26 16:06

from django.db import migrations, models
import django.db.models.deletion
import event.models.event
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('deleted_status', models.BooleanField(default=False)),
                ('doneAt', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now_add=True)),
                ('done_by', models.CharField(editable=False, max_length=255)),
                ('last_updated_by', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'activity',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('deleted_status', models.BooleanField(default=False)),
                ('doneAt', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now_add=True)),
                ('done_by', models.CharField(editable=False, max_length=255)),
                ('last_updated_by', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=100)),
                ('soldTickets', models.IntegerField(default=0)),
                ('isPayableEvent', models.BooleanField(default=False)),
                ('landingImage', models.ImageField(default=None, null=True, upload_to=event.models.event.wrapper)),
                ('homeImage', models.ImageField(default=None, null=True, upload_to=event.models.event.wrapper)),
                ('address', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'event',
            },
        ),
        migrations.CreateModel(
            name='EventTicketCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('deleted_status', models.BooleanField(default=False)),
                ('doneAt', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now_add=True)),
                ('done_by', models.CharField(editable=False, max_length=255)),
                ('last_updated_by', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=100)),
                ('Quantity', models.IntegerField(default=0)),
                ('Price', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
            ],
            options={
                'db_table': 'event_ticket_category',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('deleted_status', models.BooleanField(default=False)),
                ('doneAt', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now_add=True)),
                ('done_by', models.CharField(editable=False, max_length=255)),
                ('last_updated_by', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'package',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('deleted_status', models.BooleanField(default=False)),
                ('doneAt', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now_add=True)),
                ('done_by', models.CharField(editable=False, max_length=255)),
                ('last_updated_by', models.CharField(max_length=255)),
                ('tickNumber', models.CharField(max_length=100)),
                ('paymentStatus', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], max_length=200)),
                ('used', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.client')),
                ('eventTicketCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.eventticketcategory')),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='PackageActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('deleted_status', models.BooleanField(default=False)),
                ('doneAt', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now_add=True)),
                ('done_by', models.CharField(editable=False, max_length=255)),
                ('last_updated_by', models.CharField(max_length=255)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.activity')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.package')),
            ],
            options={
                'db_table': 'package_activity',
            },
        ),
    ]
