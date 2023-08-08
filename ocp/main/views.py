# views.py

from datetime import datetime, timedelta
import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Convocation, Stagiaire
from .forms import StagiaireForm
from django.contrib import messages
from django.utils import timezone
import calendar



def stagiaire_list(request):
    stagiaires = Stagiaire.objects.all()
    today = timezone.now().date()
    for stagiaire in stagiaires:
        if stagiaire.date_arr > today:
            stagiaire.status = "N'a pas encore commencé"
        elif stagiaire.date_arr <= today <= stagiaire.date_fin:
            stagiaire.status = "En période de stage"
        elif stagiaire.date_fin < today:
            stagiaire.status = "Terminé"
    return render(request, 'stagiaire_list.html', {'stagiaires': stagiaires})

def stagiaire_detail(request, pk):
    stagiaire = get_object_or_404(Stagiaire, pk=pk)
    cv = stagiaire.cv.path if stagiaire.cv and os.path.exists(stagiaire.cv.path) else None
    try:
        convocation = Convocation.objects.get(stagiaire=stagiaire)
    except Convocation.DoesNotExist:
        convocation = None
    return render(request, 'stagiaire_detail.html', {'stagiaire': stagiaire , 'cv':cv , 'convocation':convocation})



def stagiaire_add(request):
    if request.method == 'POST':
        form = StagiaireForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stagiaire added successfully.')
            return redirect('stagiaire_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = StagiaireForm()
    
    return render(request, 'stagiaire_add.html', {'form': form})



def stagiaire_edit(request, pk):
    stagiaire = get_object_or_404(Stagiaire, pk=pk)
    if request.method == 'POST':
        form = StagiaireForm(request.POST, request.FILES, instance=stagiaire)
        if form.is_valid():
            form.save()
            return redirect ('stagiaire_detail', pk=stagiaire.pk)
    else:
        form = StagiaireForm(instance=stagiaire)
    
    return render(request, 'stagiaire_edit.html', {'form': form})




def stagiaire_delete(request, pk):
    stagiaire = get_object_or_404(Stagiaire, pk=pk)
    if request.method == 'POST':
        stagiaire.delete()
        return redirect('stagiaire_list')
    return render(request, 'stagiaire_confirm_delete.html', {'stagiaire': stagiaire})






def home(request):
    # Get the current month and year
    current_date = timezone.now()
    year = current_date.year
    month = current_date.month

    # Handle navigation controls
    if 'month' in request.GET:
        try:
            new_date = datetime.strptime(request.GET['month'], '%Y-%m')
            year = new_date.year
            month = new_date.month
        except ValueError:
            pass

    # Fetch the stagiaire data from the database for the current month
    stagiaires = Stagiaire.objects.filter(date_arr__year=year, date_arr__month=month)

    # Create a list to hold the dates when stagiaires are present
    dates_with_stagiaires = []
    for stagiaire in stagiaires:
        date_arr = stagiaire.date_arr.day
        date_fin = stagiaire.date_fin.day

        # Add all the dates between date_arr and date_fin (inclusive)
        for day in range(date_arr, date_fin + 1):
            # Add leading zeros to the day numbers
            formatted_day = str(day).zfill(2)
            dates_with_stagiaires.append(formatted_day)

    # Get the total number of interns in the current month
    num_interns = len(stagiaires)

    # Create a calendar object for the current month
    cal = calendar.monthcalendar(year, month)

    # Handle previous and next month
    prev_month = (datetime(year, month, 1) - timedelta(days=1)).strftime('%Y-%m')
    next_month = (datetime(year, month, 28) + timedelta(days=35)).strftime('%Y-%m')

    # Format month name for display
    month_name = calendar.month_name[month]

    # Pass the data to the template context
    context = {
        'calendar': cal,
        'num_interns': num_interns,
        'dates_with_stagiaires': dates_with_stagiaires,
        'prev_month': prev_month,
        'next_month': next_month,
        'month_name': month_name,
        'year': year,
    }

    return render(request, 'home.html', context)
