# Generated by Django 3.0.2 on 2020-01-08 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Project Name', max_length=50)),
                ('pub_date', models.DateField(verbose_name='Date the book was published.')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Task title', max_length=100)),
                ('description', models.TextField(help_text='Task description')),
                ('time_estimate', models.IntegerField(help_text='Time in hours required to complete the task.')),
                ('completed', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectm.Project')),
            ],
        ),
    ]
