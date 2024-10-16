# Generated by Django 5.1 on 2024-08-28 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_number', models.CharField(max_length=10)),
                ('schedule', models.CharField(max_length=100)),
                ('room_name', models.CharField(max_length=50)),
                ('building_name', models.CharField(choices=[('ENG', 'FACULTY OF ENGINEERING'), ('LAW', 'FACULTY OF LAW'), ('MED', 'FACULTY OF MEDICINE'), ('LANG', 'FACULTY OF LANGUAGE'), ('LIT', 'FACULTY OF LITERATURE'), ('SCI', 'FACULTY OF SCIENCE')], max_length=100)),
                ('floor_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('semester_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('course_description', models.TextField()),
                ('course_code', models.CharField(max_length=200)),
                ('max_credit_points', models.CharField(max_length=10)),
                ('is_it_offered', models.BooleanField(default=False)),
                ('language', models.CharField(default='ENG', max_length=10)),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='courses.section')),
                ('semester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses_for_semester', to='courses.semester')),
            ],
        ),
    ]
