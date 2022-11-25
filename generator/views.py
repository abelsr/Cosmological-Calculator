from django.shortcuts import render
from django.http import HttpResponse
from generator.functions import *
import pandas as pd
import datetime

# Home page
def home(request):
    return render(request, 'home.html')


# About page
def about(request):
    return render(request, 'about.html')

# Function to calculate the data
def calculations(request):
    # Get the data from the form
    redshift = float(request.GET.get('redshift'))
    hubble_c = request.GET.get('h0') if request.GET.get('h0') != '' else 69.6
    lambda_l = request.GET.get('lambda') if request.GET.get('lambda') != '' else 0.714
    lambda_m = request.GET.get('lambda_matter') if request.GET.get('lambda_matter') != '' else 0.286

    # Transform the data to float
    hubble_c = float(hubble_c)
    lambda_l = float(lambda_l)
    lambda_m = float(lambda_m)

    # Calculate the data
    data = get_luminosity_distance(redshift, lambda_l, lambda_m, hubble_c)

    # Format the data in scientific notation
    for key in data:
        data[key] = '{:.2e}'.format(data[key]).replace('e+', '\\times10^{').replace('e-', '\\times10^{-') + '}'

    return render(request, 'calculations.html', {'hubble': data['Dist Hubble'], 'luminosity': data['Dist lum'], 'angular': data['Dist ang'], 'diameter': data['Diam'], 'kpc': data['kpc/arcseg']})

# Function to get file from home page
def get_file(request):
    # Get the file from the form with POST method
    try:
        file = request.FILES['database_file']
    except:
        return render(request, 'home.html', {'error': 'No file selected'})

    # If the file is .csv open with pandas
    if file.name.endswith('.csv'):
        df = pd.read_csv(file, sep = ',', header = 0, index_col = 0)
        result = []
        for i in range(len(df)):
            result.append({'REDSHIFT': df.iloc[i, 0], **get_luminosity_distance(df.iloc[i, 0])})
        df = pd.DataFrame(result)
        df.to_csv(f"results_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        return render(request, 'get_file.html', {'df': df})
    else:
        return render(request, 'home.html', {'error': 'File must be .csv'})