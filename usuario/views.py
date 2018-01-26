from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Perfil
from .forms import UsuarioForm, UsuarioUpdateForm
from django.views.generic import CreateView, UpdateView

# Create your views here.

class UsuarioCreate(CreateView):
    model = User
    form_class = UsuarioForm
    template_name = "usuario.registro.html"
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.username = form.cleaned_data['cedula']
        self.object.first_name = form.cleaned_data['nombre']
        self.object.last_name = form.cleaned_data['apellido']
        self.object.email = form.cleaned_data['correo']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()

        #user = User.objects.get(username=self.request.user.username)
        Perfil.objects.create(
            telefono=form.cleaned_data['telefono'],
            telefono_casa=form.cleaned_data['telefono_casa'],
            ocupacion=form.cleaned_data['ocupacion'],
            profesion=form.cleaned_data['profesion'],
            user= self.object,
        )
        return super(UsuarioCreate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(UsuarioCreate, self).form_invalid(form)

class UsuarioUpdate(UpdateView):
    model = User
    form_class = UsuarioUpdateForm
    template_name = "usuario.registro.html"
    #success_url = reverse_lazy('usuario_lista')

    def get_initial(self):
        datos_iniciales = super(UsuarioUpdate, self).get_initial()
        user = User.objects.get(pk=self.object.id)
        datos_iniciales['cedula'] = user.username
        datos_iniciales['nombre'] = user.first_name
        datos_iniciales['apellido'] = user.last_name
        datos_iniciales['correo'] = user.email
        perfil = Perfil.objects.get(user=user)
        datos_iniciales['telefono'] = perfil.telefono
        datos_iniciales['telefono_casa'] = perfil.telefono_casa
        datos_iniciales['ocupacion'] = perfil.ocupacion
        datos_iniciales['profesion'] = perfil.profesion
        return datos_iniciales

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.first_name = form.cleaned_data['nombre']
        self.object.last_name = form.cleaned_data['apellido']
        self.object.email = form.cleaned_data['correo']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.telefono_casa = form.cleaned_data['telefono_casa']
            perfil.ocupacion = form.cleaned_data['ocupacion']
            perfil.profesion = form.cleaned_data['profesion']
            perfil.save()
        return super(UsuarioUpdate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(UsuarioUpdate, self).form_invalid(form)
