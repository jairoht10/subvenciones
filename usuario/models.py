from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core import validators

# Create your models here.

class Perfil(models.Model):
    telefono = models.CharField(
        max_length=16, help_text=_("Número telefónico de contacto con el usuario"),
        validators=[
            validators.RegexValidator(
                r'^\+\d{3}-\d{3}-\d{7}$',
                _("Número telefónico inválido. Solo se permiten números y los símbolos: + -")
            ),
        ]
    )

    telefono_casa = models.CharField(
        max_length=16, help_text=_("Número telefónico de contacto con el usuario"),
        validators=[
            validators.RegexValidator(
                r'^\+\d{3}-\d{3}-\d{7}$',
                _("Número telefónico inválido. Solo se permiten números y los símbolos: + -")
            ),
        ]
    )

    ocupacion = models.CharField(
    #    label=_("Ocupación:"),
        max_length=100,
    )

    profesion = models.CharField(
    #    label=_("Ocupación:"),
        max_length=100,
    )

    user = models.OneToOneField(
        User, related_name="perfil",
        help_text=_("Relación entre los datos de registro y el usuario con acceso al sistema"),
        on_delete=models.CASCADE
    )

class Meta:

        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfiles")
        def __str__(self):

            return "%s, %s" % (self.user.first_name, self.user.last_name)
