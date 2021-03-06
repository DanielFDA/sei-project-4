# Generated by Django 3.1.5 on 2021-02-03 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
        ('group_members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmember',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='projects.project'),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='group', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='groupmember',
            unique_together={('user', 'project')},
        ),
    ]
