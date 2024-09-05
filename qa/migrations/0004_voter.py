# Generated by Django 5.1 on 2024-09-05 07:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0003_alter_question_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted', models.IntegerField(choices=[(0, 'NO'), (-1, 'DOWN'), (1, 'UP')], default=0)),
                ('CustomText', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voters', to='qa.customtext')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voters', to='qa.question')),
                ('voter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='voter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
