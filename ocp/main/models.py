from django.db import models
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.db.models.signals import post_save
from django.dispatch import receiver
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO


class Ecole(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


class Departement(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Encadrent(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cin = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Stagiaire(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cin = models.CharField(max_length=100)
    date_arr = models.DateField()
    date_fin = models.DateField()
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    encadrent = models.ForeignKey(Encadrent, on_delete=models.CASCADE)
    sujet = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    

    def __str__(self):
        return self.name

   

class Convocation(models.Model):
    name=models.CharField(max_length=150, null=True, blank=True)
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='convocations/', blank=True, null=True)
    def generate_convocation(self):
        # Generate the PDF content
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, f"Hello {self.stagiaire.name} {self.stagiaire.last_name}!")
        c.drawString(100, 730, f"You started your intern on {self.stagiaire.date_arr} and will finish it on {self.stagiaire.date_fin}.")
        c.drawString(100, 710, f"Your encadrent is {self.stagiaire.encadrent}.")
        c.drawString(100, 690, f"You've come from {self.stagiaire.ecole.nom} which you study {self.stagiaire.filiere.nom} in.")
        c.drawString(100, 670, f"Your intern will be in {self.stagiaire.departement.nom} and your subject is {self.stagiaire.sujet}.")
        c.drawString(100, 650, "Welcome to OCP! We hope you find this internship valuable.")
        c.save()

        # Get the PDF content from the buffer and save it to the pdf_file attribute
        pdf_content = buffer.getvalue()
        self.name=f'{self.stagiaire.cin}.pdf'
        self.pdf_file.save(f'{self.stagiaire.cin}.pdf', ContentFile(pdf_content))
        


        # Close the buffer
        buffer.close()


@receiver(post_save, sender=Stagiaire)
def create_convocation(sender, instance, created, **kwargs):
    if created:
        convocation = Convocation(stagiaire=instance)
        convocation.generate_convocation()

