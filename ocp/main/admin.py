from django.contrib import admin
from .models import Convocation, Ecole, Filiere, Departement, Encadrent, Stagiaire

admin.site.register(Ecole)
admin.site.register(Filiere)
admin.site.register(Departement)
admin.site.register(Encadrent)
admin.site.register(Stagiaire)
admin.site.register(Convocation)
admin.site.site_header = "Administration de l'application OCP"