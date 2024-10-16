# Generated by Django 5.1 on 2024-09-03 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_academicdream_section_alter_academicdream_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicdream',
            name='grade',
            field=models.IntegerField(blank=True, default=-1),
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(max_length=200)),
                ('required_credits', models.IntegerField()),
                ('courses', models.ManyToManyField(related_name='curricula', to='courses.course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curricula', to='courses.semester')),
            ],
        ),
        migrations.AddField(
            model_name='academicdream',
            name='curriculum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curry_academic_dream', to='courses.curriculum'),
        ),
    ]
