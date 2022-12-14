# Generated by Django 4.1.1 on 2022-09-11 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0002_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('email', models.EmailField(max_length=254)),
                ('otp', models.IntegerField(primary_key=True, serialize=False)),
                ('expiry', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.JSONField()),
            ],
        ),
    ]
