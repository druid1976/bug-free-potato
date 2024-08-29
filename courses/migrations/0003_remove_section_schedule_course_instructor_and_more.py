# Generated by Django 5.1 on 2024-08-29 09:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_remove_course_section_section_course'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='schedule',
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_instructor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='section',
            name='day',
            field=models.IntegerField(choices=[(1, 'MONDAY'), (2, 'TUESDAY'), (3, 'WEDNESDAY'), (4, 'THURSDAY'), (5, 'FRIDAY')], default=0),
        ),
        migrations.AddField(
            model_name='section',
            name='ending_hour',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='starting_hour',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='courses.course'),
        ),
        migrations.CreateModel(
            name='AcademicDream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(blank=True, null=True)),
                ('courses', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_in_course', to='courses.course')),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='academic_dream', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
