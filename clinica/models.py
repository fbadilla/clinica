from django.db import models
from django.contrib.auth.models import User

# Create your models here.

especialidad=[('Cardiologia','Cardiologia'),
('Dermatologia','Dermatologia'),
('Medicina Urgencias','Medicina Urgencias'),
('Alergia/Immunologia','Alergia/Immunologia'),
('Anestesiologia','Anestesiologia'),
('Oncologia','Oncologia')
]
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    foto_perfil= models.ImageField(upload_to='foto_perfil/DoctorProfilePic/',null=True,blank=True)
    direccion = models.CharField(max_length=40)
    telefono = models.CharField(max_length=20,null=True)
    especialidad= models.CharField(max_length=50,choices=especialidad,default='Cardiologia')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.especialidad)



class Paciente(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    foto_perfil= models.ImageField(upload_to='foto_perfil/PatientProfilePic/',null=True,blank=True)
    direccion = models.CharField(max_length=40)
    telefono = models.CharField(max_length=20,null=False)
    sintomas = models.CharField(max_length=100,null=False)
    doctorAsignadoId = models.PositiveIntegerField(null=True)
    fechaAdmision=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_nombre(self):
        return self.user.nombre+" "+self.user.apellido
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.nombre+" ("+self.sintomas+")"


class Agenda(models.Model):
    pacienteId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    nombrePaciente=models.CharField(max_length=40,null=True)
    nombreDoctor=models.CharField(max_length=40,null=True)
    fechaAgenda=models.DateField(auto_now=True)
    descripcion=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class DetallesAltaPaciente(models.Model):
    pacienteId=models.PositiveIntegerField(null=True)
    nombrePaciente=models.ForeignKey(Agenda, null=True,blank=True,on_delete=models.CASCADE)
    nombreDoctorAsignado=models.CharField(max_length=40)
    direccion = models.CharField(max_length=40)
    telefono = models.CharField(max_length=20,null=True)
    sintomas = models.CharField(max_length=100,null=True)

    fechaAdmision=models.ForeignKey(Paciente, null=True,blank=True,on_delete=models.CASCADE)
    fechaAlta=models.DateField(null=False)
    diaTranscurrido=models.PositiveIntegerField(null=False)

    cargoHabitacion=models.PositiveIntegerField(null=False)
    costoMedicina=models.PositiveIntegerField(null=False)
    tarifaDoctor=models.PositiveIntegerField(null=False)
    otrosCargos=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)