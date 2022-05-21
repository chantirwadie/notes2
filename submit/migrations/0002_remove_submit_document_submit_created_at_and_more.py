# Generated by Django 4.0.2 on 2022-05-04 20:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submit',
            name='document',
        ),
        migrations.AddField(
            model_name='submit',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submit',
            name='documentSubmit',
            field=models.FileField(null=True, upload_to='documentsSubmit/'),
        ),
        migrations.AddField(
            model_name='submit',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
