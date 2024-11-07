from django.contrib.auth.forms import UserCreationForm
from .models import User
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("mail", "firstName", "lastName", "birth")
        labels = {
            "firstName": "Nombre",
            "lastName": "Apellido",
            "mail": "Correo electrónico",
            "birth": "Fecha de nacimiento",
        }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['mail'].widget.attrs.update({'placeholder': 'correo@ejemplo.com'})
        self.fields['birth'].widget.attrs.update({'type': 'date'})  # Si quieres un selector de fecha
