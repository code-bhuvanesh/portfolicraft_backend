# Generated by Django 4.1.7 on 2023-10-02 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_education_degree_alter_education_endyear_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='projectimages',
        ),
        migrations.AddField(
            model_name='project',
            name='projectimage',
            field=models.ImageField(blank=True, upload_to='projectimages'),
        ),
        migrations.DeleteModel(
            name='ProjectImage',
        ),
    ]