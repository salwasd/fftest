from datetime import datetime
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
    status = models.CharField(max_length=100, blank=True, null=True)
    year = models.PositiveIntegerField(default=datetime.now().year)
    month = models.PositiveIntegerField(default=1)  
    

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

        c.drawString(400, 750, f"{self.stagiaire.date_arr}")

        # Recipient's name and address
        c.drawString(100, 700, f"To:")
        c.drawString(150, 700, f"{self.stagiaire.name} {self.stagiaire.last_name}")
        
       # Body of the letter
        c.drawString(100, 600, f"Dear {self.stagiaire.name} {self.stagiaire.last_name},")
        c.drawString(100, 580, "We are delighted to extend our warmest congratulations to you on your")
        c.drawString(100, 560, "successful selection for the internship program at OCP.")

        c.drawString(100, 540, f"This letter confirms your acceptance into the internship program, which")
        c.drawString(100, 520, f"commences on {self.stagiaire.date_arr} and concludes on {self.stagiaire.date_fin}.")

        c.drawString(100, 500, f"Throughout this internship, you will have the privilege to work under")
        c.drawString(100, 480, f"the guidance of your assigned mentor, {self.stagiaire.encadrent}, who")
        c.drawString(100, 460, f"will help you enhance your skills and knowledge in {self.stagiaire.departement.nom} department.")

        c.drawString(100, 440, f"We have taken note of your academic pursuits at {self.stagiaire.ecole.nom},")
        c.drawString(100, 420, f"where you are studying {self.stagiaire.filiere.nom}.")
        c.drawString(100, 400, f"Your academic background will undoubtedly contribute to the success of this program.")
        c.drawString(100, 380, f"Your assigned project topic, {self.stagiaire.sujet}, holds great significance for us.")

        c.drawString(100, 340, "We look forward to working with you and are confident that your contributions")
        c.drawString(100, 320, "will be invaluable. Please feel free to reach out if you have any questions.")

        c.drawString(100, 280, "Once again, congratulations on your acceptance. We eagerly await your arrival.")

        c.drawString(100, 250, "Sincerely,")
        c.drawString(400, 250, "Signature ")  # Replace with your actual signature image or text

        c.save()
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

