# Generated by Django 4.0.4 on 2023-03-13 23:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_name', models.CharField(max_length=40)),
                ('card_holder', models.CharField(max_length=60)),
                ('card_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1000000000000000), django.core.validators.MaxValueValidator(9999999999999999)])),
                ('bank_name', models.CharField(max_length=80)),
                ('valid_date', models.DateField()),
                ('color', models.CharField(choices=[('purple', 'purple'), ('blue', 'blue'), ('green', 'green'), ('orange', 'orange')], default='purple', max_length=6)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
