# Generated by Django 3.1.14 on 2023-02-10 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0014_auto_20230209_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonelementtype',
            name='img',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='element_icons',
                verbose_name='Иконка стихии'
            ),
        ),
    ]
