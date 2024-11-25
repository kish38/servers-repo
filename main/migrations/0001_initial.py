# Generated by Django 5.0.6 on 2024-11-25 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hardware_name', models.CharField(max_length=255)),
                ('cpu_model', models.CharField(max_length=255)),
                ('memory', models.CharField(max_length=255)),
                ('storage', models.CharField(max_length=255)),
                ('network_info', models.CharField(max_length=255)),
                ('firmware_version', models.CharField(max_length=255)),
                ('power_cooling', models.CharField(max_length=255)),
                ('cpu_utilisation', models.CharField(max_length=255)),
                ('load_average', models.CharField(max_length=255)),
                ('os_version', models.CharField(max_length=255)),
                ('hypervisor_details', models.CharField(max_length=255)),
                ('ip_address', models.CharField(max_length=255)),
                ('mac_address', models.CharField(max_length=255)),
                ('routing_tables', models.CharField(max_length=255)),
                ('dns_dhp', models.CharField(max_length=255)),
                ('switch_info', models.CharField(max_length=255)),
                ('idrac_ip', models.CharField(max_length=255)),
                ('pxe_address', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ServerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('servers', models.IntegerField(default=0)),
                ('vms', models.IntegerField(default=0)),
            ],
        ),
    ]
