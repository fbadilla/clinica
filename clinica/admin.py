from django.contrib import admin
from django.db import models
from .models import Doctor,Paciente,Agenda,DetallesAltaPaciente

# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PacienteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Paciente, PacienteAdmin)

class AgendaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Agenda, AgendaAdmin)

class DetallesAltaPacienteAdmin(admin.ModelAdmin):
    pass
admin.site.register(DetallesAltaPaciente, DetallesAltaPacienteAdmin)
