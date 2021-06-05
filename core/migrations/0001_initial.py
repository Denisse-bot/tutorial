# Generated by Django 2.2 on 2021-06-05 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Nombre de usuario')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, unique=True, verbose_name='Correo Electronico')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido')),
                ('rut', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Rut')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha Nacimiento')),
                ('direccion', models.CharField(blank=True, max_length=50, null=True, verbose_name='Dirección')),
                ('nro_direccion', models.IntegerField(blank=True, null=True, verbose_name='Nro Direccion')),
                ('comuna', models.IntegerField(blank=True, choices=[(1, 'Providencia'), (2, 'San Bernardo'), (3, 'La Serena'), (4, 'Temuco')], default=1, null=True)),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateField(auto_now=True, verbose_name='Fecha de creación')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.IntegerField(choices=[(1, 'Disponible'), (2, 'En atención'), (3, 'En mantención'), (4, 'No disponible, deshabilitada')], default=None)),
                ('especialidad', models.IntegerField(choices=[(1, 'Fonoaudiologia'), (2, 'Kinesiologia'), (3, 'General')], default=None)),
            ],
            options={
                'verbose_name': 'Box',
                'verbose_name_plural': 'Boxes',
                'ordering': ['estado'],
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('especialidad', models.IntegerField(choices=[(1, 'Kinesiología'), (2, 'Fonoaudiología'), (3, 'General')], default=3)),
                ('dia_reservado', models.DateTimeField()),
                ('sucursal', models.IntegerField(blank=True, choices=[(1, 'Providencia'), (2, 'San Bernardo'), (3, 'La Serena'), (4, 'Temuco')], default=1, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'ordering': ['sucursal'],
            },
        ),
        migrations.CreateModel(
            name='Atencion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_especialista', models.CharField(max_length=20)),
                ('apellido_especialista', models.CharField(max_length=20)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Box')),
                ('reserva', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Reserva')),
            ],
            options={
                'verbose_name': 'Atencion',
                'verbose_name_plural': 'Atenciones',
                'ordering': ['reserva_id'],
            },
        ),
    ]
