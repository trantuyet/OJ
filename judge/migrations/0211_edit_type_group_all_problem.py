# Generated by Django 3.2.19 on 2025-02-13 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0210_clarify_rate_all_desc'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='problem',
            options={'permissions': (('see_private_problem', 'See hidden problems'), ('edit_own_problem', 'Edit own problems'), ('create_organization_problem', 'Create organization problem'), ('edit_all_problem', 'Edit all problems'), ('edit_public_problem', 'Edit all public problems'), ('suggest_new_problem', 'Suggest new problem'), ('problem_full_markup', 'Edit problems with full markup'), ('clone_problem', 'Clone problem'), ('upload_file_statement', 'Upload file-type statement'), ('change_public_visibility', 'Change is_public field'), ('change_manually_managed', 'Change is_manually_managed field'), ('see_organization_problem', 'See organization-private problems'), ('import_polygon_package', 'Import Codeforces Polygon package'), ('edit_type_group_all_problem', 'Edit type and group for all problems')), 'verbose_name': 'problem', 'verbose_name_plural': 'problems'},
        ),
    ]
