# Generated by Django 4.1 on 2022-10-15 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='birthDate',
            new_name='birth_date',
        ),
        migrations.RenameField(
            model_name='artist',
            old_name='createdDate',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='artist',
            old_name='deathDate',
            new_name='death_date',
        ),
        migrations.RenameField(
            model_name='artist',
            old_name='lastModified',
            new_name='modified_date',
        ),
        migrations.RenameField(
            model_name='artist',
            old_name='sortTitle',
            new_name='sort_title',
        ),
    ]
