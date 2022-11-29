# Create your views here.
from django.shortcuts import render,redirect,reverse
from clinica import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings

# Create your views here.
def home_vista(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'clinica/index.html')


#for showing signup/login button for admin(by sumit)
def adminclick_vista(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'clinica/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def doctorclick_vista(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'clinica/doctorclick.html')


#for showing signup/login button for patient(by sumit)
def pacienteclick_vista(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'clinica/pacienteclick.html')




def admin_signup_vista(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'clinica/adminsignup.html',{'form':form})




def doctor_signup_vista(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'clinica/doctorsignup.html',context=mydict)


def paciente_signup_vista(request):
    userForm=forms.PacienteUserForm()
    pacienteForm=forms.PacienteForm()
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST)
        pacienteForm=forms.pacienteForm(request.POST,request.FILES)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            paciente=pacienteForm.save(commit=False)
            paciente.user=user
            paciente.doctorAsignadoId=request.POST.get('doctorAsignadoId')
            paciente=paciente.save()
            my_paciente_group = Group.objects.get_or_create(name='PACIENTE')
            my_paciente_group[0].user_set.add(user)
        return HttpResponseRedirect('pacientelogin')
    return render(request,'clinica/pacientesignup.html',context=mydict)






#-----------for checking user is doctor , patient or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_paciente(user):
    return user.groups.filter(name='PACIENTE').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_vista(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
        #return HttpResponse('afterlogin')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'clinica/doctor_aprobacion_espera.html')
    elif is_paciente(request.user):
        accountapproval=models.Paciente.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('paciente-dashboard')
        else:
            return render(request,'clinica/paciente_aprobacion_espera.html')








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_vista(request):
    #for both table in admin dashboard
    doctores=models.Doctor.objects.all().order_by('-id')
    pacientes=models.Paciente.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    pacientecount=models.Paciente.objects.all().filter(status=True).count()
    pendingpacientecount=models.Paciente.objects.all().filter(status=False).count()

    agendacount=models.Agenda.objects.all().filter(status=True).count()
    pendingagendacount=models.Agenda.objects.all().filter(status=False).count()
    mydict={
    'doctores':doctores,
    'pacientes':pacientes,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'pacientecount':pacientecount,
    'pendingpacientecount':pendingpacientecount,
    'agendacount':agendacount,
    'pendingagendacount':pendingagendacount,
    }
    return render(request,'clinica/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_vista(request):
    return render(request,'clinica/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_vista_doctor_vista(request):
    doctores=models.Doctor.objects.all().filter(status=True)
    return render(request,'clinica/admin_vista_doctor.html',{'doctores':doctores})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def eliminar_doctor_del_hospital_vista(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-vista-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def actualizar_doctor_vista(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-vista-doctor')
    return render(request,'clinica/admin_actualizar_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_agregar_doctor_vista(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-vista-doctor')
    return render(request,'clinica/admin_agregar_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_aprobar_doctor_vista(request):
    #those whose approval are needed
    doctores=models.Doctor.objects.all().filter(status=False)
    return render(request,'clinica/admin_aprobar_doctor.html',{'doctores':doctores})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def aprobar_doctor_vista(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-aprobar-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def rechazar_doctor_vista(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-aprobar-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_vista_doctor_especialidad_vista(request):
    doctores=models.Doctor.objects.all().filter(status=True)
    return render(request,'clinica/admin_vista_doctor_especialidad.html',{'doctores':doctores})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_paciente_vista(request):
    return render(request,'clinica/admin_paciente.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_vista_paciente_vista(request):
    pacientes=models.Paciente.objects.all().filter(status=True)
    return render(request,'clinica/admin_vista_paciente.html',{'pacientes':pacientes})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def eliminar_paciente_del_hospital_vista(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)
    user.delete()
    paciente.delete()
    return redirect('admin-vista-paciente')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def actualizar_paciente_vista(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)

    userForm=forms.PacienteUserForm(instance=user)
    pacienteForm=forms.PacienteForm(request.FILES,instance=paciente)
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST,instance=user)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES,instance=paciente)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            paciente=pacienteForm.save(commit=False)
            paciente.status=True
            paciente.doctorAsignadoId=request.POST.get('doctorAsignadoId')
            paciente.save()
            return redirect('admin-vista-paciente')
    return render(request,'clinica/admin_actualizar_paciente.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_agregar_paciente_vista(request):
    userForm=forms.PacienteUserForm()
    pacienteForm=forms.PacienteForm()
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            paciente=pacienteForm.save(commit=False)
            paciente.user=user
            paciente.status=True
            paciente.doctorAsignadoId=request.POST.get('doctorAsignadoId')
            paciente.save()

            my_paciente_group = Group.objects.get_or_create(name='PACIENTE')
            my_paciente_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-vista-paciente')
    return render(request,'clinica/admin_agregar_paciente.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_aprobar_paciente_vista(request):
    #those whose approval are needed
    pacientes=models.Paciente.objects.all().filter(status=False)
    return render(request,'clinica/admin_aprobar_paciente.html',{'pacientes':pacientes})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def aprobar_paciente_vista(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    paciente.status=True
    paciente.save()
    return redirect(reverse('admin-aprobar-paciente'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def rechazar_paciente_vista(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)
    user.delete()
    paciente.delete()
    return redirect('admin-aprobar-paciente')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_alta_paciente_vista(request):
    pacientes=models.Paciente.objects.all().filter(status=True)
    return render(request,'clinica/admin_alta_paciente.html',{'pacientes':pacientes})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def alta_paciente_vista(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    dias=(date.today()-paciente.fechaAdmision) #2 days, 0:00:00
    doctorAsignado=models.User.objects.all().filter(id=paciente.doctorAsignadoId)
    d=dias.dias # only how many day that is 2
    pacienteDict={
        'pacienteId':pk,
        'nombre':paciente.get_nombre,
        'telefono':paciente.telefono,
        'direccion':paciente.direccion,
        'sintomas':paciente.sintomas,
        'fechaAdmision':paciente.fechaAdmision,
        'todayDate':date.today(),
        'dia':d,
        'nombreDoctorAsignado':doctorAsignado[0].nombre,
    }
    if request.method == 'POST':
        tarifaDict ={
            'cargoHabitacion':int(request.POST['cargoHabitacion'])*int(d),
            'tarifaDoctor':request.POST['tarifaDoctor'],
            'costoMedicina' : request.POST['costoMedicina'],
            'otrosCargos' : request.POST['otrosCargos'],
            'total':(int(request.POST['cargoHabitacion'])*int(d))+int(request.POST['tarifaDoctor'])+int(request.POST['costoMedicina'])+int(request.POST['otrosCargos'])
        }
        pacienteDict.update(tarifaDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.DetallesAltaPacienteAdmin()
        pDD.pacienteId=pk
        pDD.nombrePaciente=paciente.get_nombre
        pDD.nombreDoctorAsignado=doctorAsignado[0].nombre
        pDD.direccion=paciente.direccion
        pDD.telefono=paciente.telefono
        pDD.sintomas=paciente.sintomas
        pDD.fechaAdmision=paciente.fechaAdmision
        pDD.fechaAlta=date.today()
        pDD.diaTranscurrido=int(d)
        pDD.costoMedicina=int(request.POST['costoMedicina'])
        pDD.cargoHabitacion=int(request.POST['cargoHabitacion'])*int(d)
        pDD.tarifaDoctor=int(request.POST['tarifaDoctor'])
        pDD.otrosCargos=int(request.POST['otrosCargos'])
        pDD.total=(int(request.POST['cargoHabitacion'])*int(d))+int(request.POST['tarifaDoctor'])+int(request.POST['costoMedicina'])+int(request.POST['otrosCargos'])
        pDD.save()
        return render(request,'clinica/paciente_factura_final.html',context=pacienteDict)
    return render(request,'clinica/paciente_generar_factura.html',context=pacienteDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    detallesAlta=models.DetallesAltaPacienteAdmin.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'nombrePaciente':detallesAlta[0].nombrePaciente,
        'nombreDoctorAsignado':detallesAlta[0].nombreDoctorAsignado,
        'direccion':detallesAlta[0].direccion,
        'telefono':detallesAlta[0].telefono,
        'sintomas':detallesAlta[0].sintomas,
        'fechaAdmision':detallesAlta[0].fechaAdmision,
        'fechaAlta':detallesAlta[0].fechaAlta,
        'diaTranscurrido':detallesAlta[0].diaTranscurrido,
        'costoMedicina':detallesAlta[0].costoMedicina,
        'cargoHabitacion':detallesAlta[0].cargoHabitacion,
        'tarifaDoctor':detallesAlta[0].tarifaDoctor,
        'otrosCargos':detallesAlta[0].otrosCargos,
        'total':detallesAlta[0].total,
    }
    return render_to_pdf('clinica/descargar_factura.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_agenda_vista(request):
    return render(request,'clinica/admin_agenda.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_vista_agenda_vista(request):
    agendas=models.Agenda.objects.all().filter(status=True)
    return render(request,'clinica/admin_vista_agenda.html',{'agendas':agendas})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_agregar_agenda_vista(request):
    agendaForm=forms.AgendaForm()
    mydict={'agendaForm':agendaForm,}
    if request.method=='POST':
        agendaForm=forms.AgendaForm(request.POST)
        if agendaForm.is_valid():
            agenda=agendaForm.save(commit=False)
            agenda.doctorId=request.POST.get('doctorId')
            agenda.pacienteId=request.POST.get('pacienteId')
            agenda.nombreDoctor=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            agenda.nombrePaciente=models.User.objects.get(id=request.POST.get('patientId')).first_name
            agenda.status=True
            agenda.save()
        return HttpResponseRedirect('admin-vista-agenda')
    return render(request,'clinica/admin_agregar_agenda.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_aprobar_agenda_vista(request):
    #those whose approval are needed
    agenda=models.Agenda.objects.all().filter(status=False)
    return render(request,'clinica/admin_aprobar_agenda.html',{'agendas':agenda})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def aprobar_agenda_vista(request,pk):
    agenda=models.Agenda.objects.get(id=pk)
    agenda.status=True
    agenda.save()
    return redirect(reverse('admin-aprobar-agenda'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def rechazar_agenda_vista(request,pk):
    agenda=models.Agenda.objects.get(id=pk)
    agenda.delete()
    return redirect('admin-aprobar-agenda')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_vista(request):
    #for three cards
    pacientecount=models.Paciente.objects.all().filter(status=True,doctorAsignadoId=request.user.id).count()
    agendacount=models.Agenda.objects.all().filter(status=True,doctorId=request.user.id).count()
    pacienteAlta=models.DetallesAltaPaciente.objects.all().distinct().filter(nombreDoctorAsignado=request.user.first_name).count()

    #for  table in doctor dashboard
    agendas=models.Agenda.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    pacienteid=[]
    for a in agendas:
        pacienteid.append(a.pacienteId)
    pacientes=models.Paciente.objects.all().filter(status=True,user_id__in=pacienteid).order_by('-id')
    agendas=zip(agendas,pacientes)
    mydict={
    'pacientecount':pacientecount,
    'agendacount':agendacount,
    'pacientealta':pacienteAlta,
    'agendas':agendas,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'clinica/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_paciente_vista(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'clinica/doctor_paciente.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_vista_paciente_vista(request):
    pacientes=models.Paciente.objects.all().filter(status=True,doctorAsignadoId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'clinica/doctor_vista_paciente.html',{'pacientes':pacientes,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_vista_alta_paciente_vista(request):
    altapacientes=models.DetallesAltaPaciente.objects.all().distinct().filter(nombreDoctorAsignado=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'clinica/doctor_vista_alta_paciente.html',{'altapacientes':altapacientes,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_agenda_vista(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'clinica/doctor_agenda.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_vista_agenda_vista(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    agendas=models.Agenda.objects.all().filter(status=True,doctorId=request.user.id)
    pacienteid=[]
    for a in agendas:
        pacienteid.append(a.pacienteId)
    pacientes=models.Paciente.objects.all().filter(status=True,user_id__in=pacienteid)
    agendas=zip(agendas,pacientes)
    return render(request,'clinica/doctor_vista_agenda.html',{'agendas':agendas,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_eliminar_agenda_vista(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    agendas=models.Agenda.objects.all().filter(status=True,doctorId=request.user.id)
    pacienteid=[]
    for a in agendas:
        pacienteid.append(a.pacienteId)
    pacientes=models.Paciente.objects.all().filter(status=True,user_id__in=pacienteid)
    agendas=zip(agendas,pacientes)
    return render(request,'clinica/doctor_eliminar_agenda.html',{'agendas':agendas,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def eliminar_agenda_vista(request,pk):
    agenda=models.Agenda.objects.get(id=pk)
    agenda.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    agendas=models.Agenda.objects.all().filter(status=True,doctorId=request.user.id)
    pacienteid=[]
    for a in agendas:
        pacienteid.append(a.pacienteId)
    pacientes=models.Paciente.objects.all().filter(status=True,user_id__in=pacienteid)
    agendas=zip(agendas,pacientes)
    return render(request,'clinica/doctor_eliminar_agenda.html',{'agendas':agendas,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_dashboard_vista(request):
    paciente=models.Paciente.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=paciente.doctorAsignadoId)
    mydict={
    'paciente':paciente,
    'nombreDoctor':doctor.get_name,
    'telefonoDoctor':doctor.telefono,
    'direccionDoctor':doctor.direccion,
    'sintomas':paciente.sintomas,
    'especialidadDoctor':doctor.especialidad,
    'fechaAdmision':paciente.fechaAdmision,
    }
    return render(request,'clinica/paciente_dashboard.html',context=mydict)



@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_agenda_vista(request):
    paciente=models.Paciente.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'clinica/paciente_agenda.html',{'paciente':paciente})



@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_libro_agenda_vista(request):
    agendaForm=forms.PacienteAgendaForm()
    paciente=models.Paciente.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    mensaje=None
    mydict={'agendaForm':agendaForm,'paciente':paciente,'mensaje':mensaje}
    if request.method=='POST':
        agendaForm=forms.PacienteAgendaForm(request.POST)
        if agendaForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('descripcion')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            if doctor.especialidad == 'Cardiologia':
                if 'corazon' in desc:
                    pass
                else:
                    print('else')
                    message="Por favor elija al doctor según la enfermedad"
                    return render(request,'clinica/paciente_libro_agenda.html',{'agendaForm':agendaForm,'paciente':paciente,'mensaje':mensaje})


            if doctor.especialidad == 'Dermatologia':
                if 'piel' in desc:
                    pass
                else:
                    print('else')
                    message="Por favor elija al doctor según la enfermedad"
                    return render(request,'clinica/paciente_libro_agenda.html',{'agendaForm':agendaForm,'paciente':paciente,'mensaje':mensaje})

            if doctor.especialidad == 'Medicina Urgencias':
                if 'fiebre' in desc:
                    pass
                else:
                    print('else')
                    message="Por favor elija al doctor según la enfermedad"
                    return render(request,'clinica/paciente_libro_agenda.html',{'agendaForm':agendaForm,'paciente':paciente,'mensaje':mensaje})

            if doctor.especialidad == 'Alergia/Immunologia':
                if 'alergia' in desc:
                    pass
                else:
                    print('else')
                    message="Por favor elija al doctor según la enfermedad"
                    return render(request,'clinica/paciente_libro_agenda.html',{'agendaForm':agendaForm,'paciente':paciente,'mensaje':mensaje})

            if doctor.especialidad == 'Anestesiologia':
                if 'cirugia' in desc:
                    pass
                else:
                    print('else')
                    message="Por favor elija al doctor según la enfermedad"
                    return render(request,'clinica/paciente_libro_agenda.html',{'agendaForm':agendaForm,'paciente':paciente,'mensaje':mensaje})

            if doctor.especialidad == 'Oncologia':
                if 'cancer' in desc:
                    pass
                else:
                    print('else')
                    message="Por favor elija al doctor según la enfermedad"
                    return render(request,'clinica/paciente_libro_agenda.html',{'agendaForm':agendaForm,'paciente':paciente,'mensaje':mensaje})





            agenda=agendaForm.save(commit=False)
            agenda.doctorId=request.POST.get('doctorId')
            agenda.pacienteId=request.user.id #----user can choose any patient but only their info will be stored
            agenda.nombreDoctor=models.User.objects.get(id=request.POST.get('doctorId')).nombre
            agenda.nombrePaciente=request.user.nombre #----user can choose any patient but only their info will be stored
            agenda.status=False
            agenda.save()
        return HttpResponseRedirect('paciente-vista-agenda')
    return render(request,'clinica/paciente_libro_agenda.html',context=mydict)





@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_vista_agenda_vista(request):
    paciente=models.Paciente.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    agendas=models.Agenda.objects.all().filter(pacienteId=request.user.id)
    return render(request,'clinica/paciente_vista_agenda.html',{'agendas':agendas,'paciente':paciente})



@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_alta_vista(request):
    paciente=models.Paciente.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    detallesAlta=models.DetallesAltaPacienteAdmin.objects.all().filter(pacienteId=paciente.id).order_by('-id')[:1]
    pacienteDict=None
    if detallesAlta:
        pacienteDict ={
        'entrega_alta':True,
        'paciente':paciente,
        'pacienteId':paciente.id,
        'nombrePaciente':paciente.get_nombre,
        'nombreDoctorAsignado':detallesAlta[0].nombreDoctorAsignado,
        'direccion':paciente.direccion,
        'telefono':paciente.telefono,
        'sintomas':paciente.sintomas,
        'fechaAdmision':paciente.fechaAdmision,
        'fechaAlta':detallesAlta[0].fechaAlta,
        'diaTranscurrido':detallesAlta[0].diaTranscurrido,
        'costoMedicina':detallesAlta[0].costoMedicina,
        'cargoHabitacion':detallesAlta[0].cargoHabitacion,
        'tarifaDoctor':detallesAlta[0].tarifaDoctor,
        'otrosCargos':detallesAlta[0].otrosCargos,
        'total':detallesAlta[0].total,
        }
        print(pacienteDict)
    else:
        pacienteDict={
            'entrega_alta':False,
            'paciente':paciente,
            'pacienteId':request.user.id,
        }
    return render(request,'clinica/paciente_alta.html',context=pacienteDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def nosotros_view(request):
    return render(request,'clinica/nosotros.html')

def contactanos_view(request):
    sub = forms.ContactanosForm()
    if request.method == 'POST':
        sub = forms.ContactanosForm(request.POST)
        if sub.is_valid():
            Email = sub.cleaned_data['Email']
            Nombre=sub.cleaned_data['Nombre']
            Mensaje = sub.cleaned_data['Mensaje']
            send_mail(str(Nombre)+' || '+str(Email),Mensaje,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'clinica/contactanosexitoso.html')
    return render(request, 'clinica/contactanos.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------



