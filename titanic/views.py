import pandas as pd
import numpy as np

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib import messages

from titanic.models import TitanicPassenger
from titanic.forms import TitanicPassengerForm

# Create your views here.

class TitanicView(View):
    def get(self, request):
        passengers = TitanicPassenger.objects.all()
        form = TitanicPassengerForm()
        return render(request, 'titanic/home.html', {
            'form': form,
            'passengers': passengers,
        })
        
    def post(self, request):
        form_type = request.POST.get('form-type')
        
        if form_type == "upload":
            if 'file' in request.FILES:
                excel_file = request.FILES['file']
                
                try:
                    df = pd.read_excel(excel_file)
                    df = df.replace({np.nan: None})
                    
                    for _, row in df.iterrows():
                        TitanicPassenger.objects.update_or_create(
                            passenger_id=row['PassengerId'],
                            defaults={
                                'survived': row['Survived'],
                                'pclass': row['Pclass'],
                                'name': row['Name'],
                                'sex': row['Sex'],
                                'age': row['Age'],
                                'sibsp': row['SibSp'],
                                'parch': row['Parch'],
                                'ticket': row['Ticket'],
                                'fare': row['Fare'],
                                'cabin': row['Cabin'],
                                'embarked': row['Embarked'],
                            }
                        )
                    messages.success(request, "Data uploaded successfully!")
                    
                except Exception as e:
                    messages.error(request, f"Error processing file: {e}")
                    
                return redirect('titanic-home')
            
            else:
                messages.error(request, "No file uploaded!")
                return redirect('titanic-home')
            
        elif form_type == "crud":
            submit_type = request.POST.get('submit-type')
            
            if submit_type == "create-update":
                passenger_id = request.POST.get('passenger_id')
                
                if passenger_id:
                    try:
                        passenger = TitanicPassenger.objects.get(passenger_id=passenger_id)
                        form = TitanicPassengerForm(request.POST, instance=passenger)
                        
                        if form.is_valid():
                            form.save()
                            messages.success(request, "Passenger updated successfully!")
                            
                        else:
                            messages.error(request, "Failed to update passenger. Check the form.")
                            
                    except TitanicPassenger.DoesNotExist:
                        form = TitanicPassengerForm(request.POST)
                        
                        if form.is_valid():
                            form.save()
                            messages.success(request, "Passenger created successfully!")
                            
                        else:
                            messages.error(request, "Failed to create passenger. Check the form.")
                            
                else:
                    messages.error(request, "Passenger ID is required for creation or update.")
            
            elif submit_type == "delete":
                passenger_id = request.POST.get('passenger_id')
                
                if passenger_id:
                    try:
                        passenger = TitanicPassenger.objects.get(passenger_id=passenger_id)
                        passenger.delete()
                        messages.success(request, "Passenger deleted successfully!")
                        
                    except TitanicPassenger.DoesNotExist:
                        messages.error(request, "Passenger not found!")
                        
                else:
                    messages.error(request, "Passenger ID is required for deletion.")
            
            return redirect('titanic-home')

        messages.error(request, "No valid form submission or file upload.")
        return redirect('titanic-home')


