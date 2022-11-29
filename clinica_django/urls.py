"""clinica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clinica import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_vista,name=''),


    path('nosotros', views.nosotros_view),
    path('contactanos', views.contactanos_view),


    path('adminclick', views.adminclick_vista),
    path('doctorclick', views.doctorclick_vista),
    path('pacienteclick', views.pacienteclick_vista),

    path('adminsignup', views.admin_signup_vista),
    path('doctorsignup', views.doctor_signup_vista,name='doctorsignup'),
    path('pacientesignup', views.paciente_signup_vista),
    
    path('adminlogin', LoginView.as_view(template_name='clinica/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='clinica/doctorlogin.html')),
    path('pacientelogin', LoginView.as_view(template_name='clinica/pacientelogin.html')),


    path('afterlogin', views.afterlogin_vista,name='afterlogin'),
    path('logout/', LogoutView.as_view(template_name='clinica/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_vista,name='admin-dashboard'),

    path('admin-doctor', views.admin_doctor_vista,name='admin-doctor'),
    path('admin-vista-doctor', views.admin_vista_doctor_vista,name='admin-vista-doctor'),
    path('eliminar-doctor-del-hospital/<int:pk>', views.eliminar_doctor_del_hospital_vista,name='eliminar-doctor-del-hospital'),
    path('actualizar-doctor/<int:pk>', views.actualizar_doctor_vista,name='actualizar-doctor'),
    path('admin-agregar-doctor', views.admin_agregar_doctor_vista,name='admin-agregar-doctor'),
    path('admin-aprobar-doctor', views.admin_aprobar_doctor_vista,name='admin-aprobar-doctor'),
    path('aprobar-doctor/<int:pk>', views.aprobar_doctor_vista,name='aprobar-doctor'),
    path('rechazar-doctor/<int:pk>', views.rechazar_doctor_vista,name='rechazar-doctor'),
    path('admin-vista-doctor-especialidad',views.admin_vista_doctor_especialidad_vista,name='admin-vista-doctor-especialidad'),


    path('admin-paciente', views.admin_paciente_vista,name='admin-paciente'),
    path('admin-vista-paciente', views.admin_vista_paciente_vista,name='admin-vista-paciente'),
    path('eliminar-paciente-del-hospital/<int:pk>', views.eliminar_paciente_del_hospital_vista,name='eliminar-paciente-del-hospital'),
    path('actualizar-paciente/<int:pk>', views.actualizar_paciente_vista,name='actualizar-paciente'),
    path('admin-agregar-paciente', views.admin_agregar_paciente_vista,name='admin-paciente-doctor'),
    path('admin-aprobar-paciente/', views.admin_aprobar_paciente_vista,name='admin-aprobar-paciente'),
    path('aprobar-paciente/<int:pk>', views.aprobar_paciente_vista,name='aprobar-paciente'),
    path('rechazar-paciente/<int:pk>', views.rechazar_paciente_vista,name='rechazar-paciente'),
    path('admin-alta-paciente', views.admin_alta_paciente_vista,name='admin-alta-paciente'),
    path('alta-paciente/<int:pk>', views.alta_paciente_vista,name='alta-paciente'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-agenda', views.admin_agenda_vista,name='admin-agenda'),
    path('admin-vista-agenda', views.admin_vista_agenda_vista,name='admin-vista-agenda'),
    path('admin-agregar-agenda', views.admin_agregar_agenda_vista,name='admin-agregar-agenda'),
    path('admin-aprobar-agenda', views.admin_aprobar_agenda_vista,name='admin-aprobar-agenda'),
    path('aprobar-agenda/<int:pk>', views.aprobar_agenda_vista,name='aprobar-agenda'),
    path('rechazar-agenda/<int:pk>', views.rechazar_agenda_vista,name='rechazar-agenda'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_vista,name='doctor-dashboard'),

    path('doctor-paciente', views.doctor_paciente_vista,name='doctor-patient'),
    path('doctor-vista-paciente', views.doctor_vista_paciente_vista,name='doctor-vista-paciente'),
    path('doctor-vista-alta-paciente',views.doctor_vista_alta_paciente_vista,name='doctor-vista-alta-paciente'),

    path('doctor-agenda', views.doctor_agenda_vista,name='doctor-agenda'),
    path('doctor-vista-agenda', views.doctor_vista_agenda_vista,name='doctor-vista-agenda'),
    path('doctor-eliminar-agenda',views.doctor_eliminar_agenda_vista,name='doctor-eliminar-agenda'),
    path('eliminar-agenda/<int:pk>', views.eliminar_agenda_vista,name='eliminar-agenda'),
]




#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('paciente-dashboard', views.paciente_dashboard_vista,name='paciente-dashboard'),
    path('paciente-agenda', views.paciente_agenda_vista,name='paciente-agenda'),
    path('paciente-libro-agenda', views.paciente_libro_agenda_vista,name='paciente-libro-agenda'),
    path('paciente-vista-agenda', views.paciente_vista_agenda_vista,name='paciente-vista-agenda'),
    path('paciente-alta', views.paciente_alta_vista,name='paciente-alta'),

]

