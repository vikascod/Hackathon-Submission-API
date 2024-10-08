# Generated by Django 4.2.6 on 2024-09-08 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hackathon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('background_image', models.ImageField(upload_to='hackathon/backgrounds/')),
                ('hackathon_image', models.ImageField(upload_to='hackathon/images/')),
                ('submission_type', models.CharField(choices=[('image', 'Image'), ('file', 'File'), ('link', 'Link')], default='link', max_length=10)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('reward_prize', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Hackathon',
                'verbose_name_plural': 'Hackathons',
                'ordering': ['-start_datetime'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('submission_file', models.FileField(blank=True, null=True, upload_to='submissions/files/')),
                ('submission_image', models.ImageField(blank=True, null=True, upload_to='submissions/images/')),
                ('submission_link', models.URLField(blank=True, max_length=500, null=True)),
                ('submission_datetime', models.DateTimeField(auto_now_add=True)),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='submission.hackathon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Submission',
                'verbose_name_plural': 'Submissions',
                'ordering': ['-submission_datetime'],
            },
        ),
        migrations.CreateModel(
            name='HackathonParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='submission.hackathon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hackathon_participant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
