from django import forms
from django.contrib.auth.models import User
from . import models



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['direccion','telefono','especialidad','status','foto_perfil']



#for teacher related form
class PacienteUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PacienteForm(forms.ModelForm):
#este es el campo adicional para vincular al paciente y su médico asignado
#esto mostrará el menú desplegable __str__ method doctor model se muestra en html, así que anúlelo
#to_field_name esto obtendrá el valor correspondiente user_id presente en el modelo Doctor y lo devolverá
    doctorAsignadoId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Nombre y Especialidad", to_field_name="user_id")
    class Meta:
        model=models.Paciente
        fields=['direccion','telefono','status','sintomas','foto_perfil']



class AgendaForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Nombre Doctor y Especialidad", to_field_name="user_id")
    pacienteId=forms.ModelChoiceField(queryset=models.Paciente.objects.all().filter(status=True),empty_label="Nombre Paciente y Especialidad", to_field_name="user_id")
    class Meta:
        model=models.Agenda
        fields=['descripcion','status']


class PacienteAgendaForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Nombre Doctor y Especialidad", to_field_name="user_id")
    class Meta:
        model=models.Agenda
        fields=['descripcion','status']


#for contact us page
class ContactanosForm(forms.Form):
    Nombre = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Mensaje = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))