# Generated by Django 3.2.7 on 2021-09-27 22:48

from django.db import migrations, models
import django.db.models.deletion
import helpers.filesystem
import imagekit.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('banner_image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=helpers.filesystem.RandomFileName('offers/'), verbose_name='Imagen principal')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('discount_percent', models.FloatField(blank=True, default=0, null=True, verbose_name='Porcentaje de descuento')),
                ('discounted_price', models.FloatField(blank=True, default=0, null=True, verbose_name='Precio con descuento')),
                ('active', models.BooleanField(default=True, verbose_name='Activa')),
                ('begin_date', models.DateField(blank=True, null=True, verbose_name='Fecha de inicio')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Fecha de fin')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='currency.entity')),
            ],
            options={
                'verbose_name': 'Oferta',
                'verbose_name_plural': 'Ofertas',
                'ordering': ['-published_date'],
            },
        ),
    ]
