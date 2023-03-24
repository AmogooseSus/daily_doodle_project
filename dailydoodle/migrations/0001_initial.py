# Generated by Django 2.2.28 on 2023-03-23 22:06

import dailydoodle.models
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
            name='Drawing',
            fields=[
                ('drawing', models.ImageField(upload_to='submissions')),
                ('drawing_id', models.CharField(max_length=61, primary_key=True, serialize=False, unique=True)),
                ('total_upvotes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(max_length=30, unique=True)),
                ('prompt_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, upload_to=dailydoodle.models.rename_path)),
                ('upvotes_recieved', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drawing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dailydoodle.Drawing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='drawing',
            name='prompt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dailydoodle.Prompt'),
        ),
        migrations.AddField(
            model_name='drawing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('comment', models.CharField(max_length=200)),
                ('drawing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dailydoodle.Drawing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
