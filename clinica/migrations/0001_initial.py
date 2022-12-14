# Generated by Django 4.1.3 on 2022-11-22 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pacienteId', models.PositiveIntegerField(null=True)),
                ('doctorId', models.PositiveIntegerField(null=True)),
                ('nombrePaciente', models.CharField(max_length=40, null=True)),
                ('nombreDoctor', models.CharField(max_length=40, null=True)),
                ('fechaAgenda', models.DateField(auto_now=True)),
                ('descripcion', models.TextField(max_length=500)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DetallesAltaPaciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pacienteId', models.PositiveIntegerField(null=True)),
                ('nombrePaciente', models.CharField(max_length=40)),
                ('nombreDoctorAsignado', models.CharField(max_length=40)),
                ('direccion', models.CharField(max_length=40)),
                ('telefono', models.CharField(max_length=20, null=True)),
                ('sintomas', models.CharField(max_length=100, null=True)),
                ('fechaAdmision', models.DateField()),
                ('fechaAlta', models.DateField()),
                ('diaTranscurrido', models.PositiveIntegerField()),
                ('cargoHabitacion', models.PositiveIntegerField()),
                ('costoMedicina', models.PositiveIntegerField()),
                ('tarifaDoctor', models.PositiveIntegerField()),
                ('otrosCargos', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='foto_perfil/PatientProfilePic/')),
                ('direccion', models.CharField(max_length=40)),
                ('telefono', models.CharField(max_length=20)),
                ('sintomas', models.CharField(max_length=100)),
                ('doctorAsignadoId', models.PositiveIntegerField(null=True)),
                ('fechaAdmision', models.DateField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='foto_perfil/DoctorProfilePic/')),
                ('direccion', models.CharField(max_length=40)),
                ('telefono', models.CharField(max_length=20, null=True)),
                ('especialidad', models.CharField(choices=[('Cardiologia', 'Cardiologia'), ('Dermatologia', 'Dermatologia'), ('Medicina Urgencias', 'Medicina Urgencias'), ('Alergia/Immunologia', 'Alergia/Immunologia'), ('Anestesiologia', 'Anestesiologia'), ('Oncologia', 'Oncologia')], default='Cardiologia', max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
