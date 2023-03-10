# Generated by Django 3.2.14 on 2022-11-14 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bobina_consumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumo_bobina', models.CharField(max_length=30)),
                ('tecnico', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Bobina_hisotiral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seriado_bobina', models.CharField(max_length=30)),
                ('tecnico', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tecnico', models.CharField(max_length=30)),
                ('equipo', models.CharField(max_length=30)),
                ('mac', models.CharField(max_length=30, unique=True)),
                ('vt', models.CharField(max_length=30)),
                ('cliente', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=60)),
                ('nombre_equipo', models.CharField(max_length=60)),
                ('seriado', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='EquiposRetirados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.CharField(max_length=30)),
                ('tecnico', models.CharField(max_length=120)),
                ('equipo_instalado', models.CharField(max_length=120)),
                ('mac_instalado', models.CharField(max_length=50)),
                ('equipo_desinstalado', models.CharField(max_length=120)),
                ('mac_desinstalado', models.CharField(max_length=50)),
                ('numero_vt', models.CharField(max_length=50)),
                ('numero_cliente', models.CharField(max_length=50)),
                ('nombre_cliente', models.CharField(max_length=120)),
                ('dni_cliente', models.CharField(max_length=50)),
                ('direccion_cliente', models.CharField(max_length=120)),
                ('localidad_cliente', models.CharField(max_length=50)),
                ('partido_cliente', models.CharField(max_length=50)),
                ('telefono_cliente', models.CharField(max_length=50)),
                ('region_cliente', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('metros', models.IntegerField(blank=True, unique=True)),
            ],
        ),
    ]
