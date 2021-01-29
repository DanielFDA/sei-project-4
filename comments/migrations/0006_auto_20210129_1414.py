# Generated by Django 3.1.5 on 2021-01-29 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group_members', '0002_auto_20210129_0826'),
        ('comments', '0005_auto_20210129_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_comments', to='group_members.groupmember'),
        ),
    ]
