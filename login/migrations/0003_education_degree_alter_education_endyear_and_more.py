# Generated by Django 4.1.7 on 2023-09-26 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_alter_project_projectimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='degree',
            field=models.CharField(default='no degree', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='education',
            name='endYear',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='startYear',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='projectimages',
            field=models.ManyToManyField(blank=True, to='login.projectimage'),
        ),
    ]
