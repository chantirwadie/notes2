# Generated by Django 4.0.2 on 2022-05-05 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0003_remove_submit_documentsubmit'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='commentaire',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
