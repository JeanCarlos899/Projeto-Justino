# Generated by Django 4.1.3 on 2023-03-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elaboradorapp', '0007_alter_question_enunciado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='enunciado',
            field=models.TextField(max_length=5000, verbose_name='enunciado'),
        ),
    ]