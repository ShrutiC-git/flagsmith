# Generated by Django 2.2.17 on 2021-04-01 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("features", "0029_auto_20210223_2106"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feature",
            name="initial_value",
            field=models.CharField(default=None, max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name="featurestatevalue",
            name="string_value",
            field=models.CharField(blank=True, max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name="historicalfeature",
            name="initial_value",
            field=models.CharField(default=None, max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name="historicalfeaturestatevalue",
            name="string_value",
            field=models.CharField(blank=True, max_length=20000, null=True),
        ),
    ]
