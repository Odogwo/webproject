# Generated by Django 3.2.6 on 2021-08-09 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='affiliate_url',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_description',
            field=models.TextField(default='No Description'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]