from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Import User UpdateForm, ProfileUpdatForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PacienteRegisterForm, \
    nuevoPacienteInstitucionForm, DonanteReposicionForm, DonanteAsistenciaForm
from .models import Paciente, PacienteInstitucion, Donantes
from .filters import PacienteFilter

def verListadoSolicitud(request, id):
    pacInstitucion = PacienteInstitucion.objects.get(pk=id)
    donantes = Donantes.objects.filter(pacienteInstitucion=pacInstitucion.id)
    print('*********************')
    print(donantes)
    context = {'pacInstitucion': pacInstitucion,
               'donantes': donantes}
    return render(request, 'users/verListadoSolicitud.html', context)


def editarListadoSolicitud(request, id):
    pacInstitucion = get_object_or_404(PacienteInstitucion, pk=id)
    if request.method == 'POST':
        pi_form = nuevoPacienteInstitucionForm(request.POST, instance=pacInstitucion)
        if pi_form.is_valid():
            pi_form.save()
            messages.success(request, f'El pedido de donantes ha sido actualizado correctamente!')
            return redirect('listadoSolicitud') # Redirect back to paciente page
    else:
        pi_form = nuevoPacienteInstitucionForm(instance=pacInstitucion)
    context = {
        'pi_form': pi_form
    }
    return render(request, 'users/editarListadoSolicitud.html', context)

def listadoSolicitud(request):
    startdate = date.today()
    paciente = Paciente.objects.filter(is_paciente=True, user_id=request.user.id)
    pacientesInstitucion = PacienteInstitucion.objects.filter(paciente__id__in=paciente.all()).order_by("fechaLimite")
    context = {'paciente': paciente,
               'pacientesInstitucion': pacientesInstitucion,
               'startdate':startdate}
    return render(request, 'users/listadoSolicitud.html', context)

def donanteAsistencia(request, id):
    donante = get_object_or_404(Donantes, pk=id)

    print('donante pk')
    print(donante)
    if request.method == 'POST':
        d_form = DonanteAsistenciaForm(request.POST, instance=donante)
        if d_form.is_valid():
            asistencia = d_form.save(commit=False)
            asistencia.confirmacionAsistencia = 'True'
            d_form.save()
            messages.success(request, f'Gracias por informarnos que te has presentado a donar. Compartiremos esta información con el paciente!')
            return redirect('listadoDonante')  # Redirect back to paciente page
    else:
        d_form = DonanteAsistenciaForm(instance=donante)
    context = {
        'd_form': d_form
    }
    return render(request, 'users/donanteAsistencia.html', context)


def donanteAsistenciaEliminar(request, id):
    donante = get_object_or_404(Donantes, pk=id)
    if donante:
        donante.delete()
    return redirect('listadoDonante')


def listadoDonante(request):

    donante = Donantes.objects.filter(user=request.user.id, is_donante=True)

    print('donante')
    print(donante)
    context = {'donante': donante}
    return render(request, 'users/listadoDonante.html', context)


def listadoPaciente(request):
    startdate = date.today()
    pacientes = Paciente.objects.filter(is_paciente=True)

    pacientesInstitucion = PacienteInstitucion.objects.filter(paciente__id__in=pacientes.all(), fechaLimite__gte=startdate, completo=False).order_by("fechaLimite")

    myFilter = PacienteFilter(request.GET, queryset=pacientesInstitucion)
    pacientesInstitucion = myFilter.qs

    donantes1 = Donantes.objects.filter(pacienteInstitucion__id__in=pacientesInstitucion.all(), user=request.user.id)
    donantes2 = Donantes.objects.filter(pacienteInstitucion__id__in=pacientesInstitucion.all(), confirmacionAsistencia=True)
    template_list = list(zip(pacientesInstitucion.all(), donantes1.all()))

    cantDon = str(len(donantes1))


    context = {
        'pacientes': pacientes,
        'myFilter': myFilter,
        'pacientesInstitucion': pacientesInstitucion,
        'donantes1': donantes1,
        'donantes2':donantes2,
        'template_list':template_list,
        'cantDon':cantDon
    }
    return render(request, 'users/paciente.html', context)


def donante(request, id):
    paciente = get_object_or_404(Paciente, user_id=id)

    pacienteInstitucion = get_object_or_404(PacienteInstitucion, paciente_id=paciente.id, completo=False)

    if request.method == 'POST':
        d_form = DonanteReposicionForm(request.POST)
        if d_form.is_valid():
            donante = d_form.save(commit=False)
            paciente = get_object_or_404(Paciente, user_id=id)

            pacienteInstitucion = get_object_or_404(PacienteInstitucion, paciente_id=paciente.id, completo=False)
            donante.is_donante = 'True'
            donante.fechaDonacionElegida = d_form.cleaned_data['fechaDonancionElegida']
            d_form.save()
            donante.user.add(request.user.id)

            donante.pacienteInstitucion.add(pacienteInstitucion.id)

            messages.success(request, f'Has aplicado para donar!')
            return redirect('listadoPaciente') # Redirect back to paciente page
    else:
        d_form = DonanteReposicionForm()

    context = {
        'd_form': d_form,
        'pacienteInstitucion':pacienteInstitucion,
        'paciente':paciente
    }
    return render(request, 'users/donante.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tu cuenta ha sido creada! Ahora puedes iniciar sesión')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# Update it here
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            patient = p_form.save(commit=False)
            patient.is_paciente = True
            patient.save()
            messages.success(request, f'Tu perfil de usuario ha sido actualizado!')
            return redirect('profile') # Redirect back to profile page
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def paciente(request):
    if request.method == 'POST':
        instPaclist = PacienteInstitucion.objects.filter(paciente__id=request.user.paciente.pk, completo=False)
        for instanciaPaciente in instPaclist:
            instanciaPaciente.completo = True
            instanciaPaciente.save()

    if request.method == 'POST':

        p_form = PacienteRegisterForm(request.POST, instance=request.user.paciente)
        pi_form = nuevoPacienteInstitucionForm(request.POST)
        if p_form.is_valid() and pi_form.is_valid():
            patientId1 = ((Paciente.objects.all()).order_by('-updated_at')[:1]).values_list('id')

            p = p_form.save(commit=False)
            p.updated_at =datetime.now()
            p.is_paciente = True
            p_form.save()
            #p_form.save_m2m()

            fs = pi_form.save(commit=False)
            fs.paciente_id = patientId1
            fs.completo = False
            pi_form.save()

            messages.success(request, f'El paciente se ha creado con éxito! Puedes editar la información ingresando a Información de Institución.')
            return redirect('paciente') # Redirect back to paciente page
    else:
        p_form = PacienteRegisterForm(instance=request.user.paciente)
        pi_form = nuevoPacienteInstitucionForm()

    context = {
        'p_form': p_form,
        'pi_form': pi_form
    }
    return render(request, 'users/nuevoPaciente.html', context)

###solo para consulta
def listadoPaciente1(request):
    startdate = date.today()

    pacientes = Paciente.objects.filter(is_paciente=True)

    pacientesInstitucion = PacienteInstitucion.objects.filter(paciente__id__in=pacientes.all(), fechaLimite__gte=startdate, completo=False).order_by("fechaLimite")

    return render(request, 'users/paciente.html', {'usersList': pacientes, 'pacientesInstitucion':pacientesInstitucion})

