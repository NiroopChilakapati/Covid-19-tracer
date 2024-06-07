from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import *
from django.core.mail import send_mail
import random
# Create your views here.
def index(request):
    return render(request, 'index.html')



import requests
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Country

# Constants
COVID_DATA_CACHE_KEY = 'covid_data'
COVID_DATA_TIMEOUT = 300  # 5 minutes cache timeout


def fetch_covid_data():
    # Check if data is cached
    cached_data = cache.get(COVID_DATA_CACHE_KEY)
    if cached_data is not None:
        return cached_data

    # Fetch data from the API
    response = requests.get('https://covid-19.dataflowkit.com/v1')
    data = response.json()

    # Clean and process the data as before
    cleaned_data = []
    for item in data:
        cleaned_item = {
            'Active_Cases_text': item.get('Active Cases_text', 'N/A').replace(',', ''),
            'Country_text': item.get('Country_text', 'N/A'),
            'Last_Update': item.get('Last Update', 'N/A'),
            'New_Cases_text': item.get('New Cases_text', 'N/A').replace(',', ''),
            'New_Deaths_text': item.get('New Deaths_text', 'N/A').replace(',', ''),
            'Total_Cases_text': item.get('Total Cases_text', 'N/A').replace(',', ''),
            'Total_Deaths_text': item.get('Total Deaths_text', 'N/A').replace(',', ''),
            'Total_Recovered_text': item.get('Total Recovered_text', 'N/A').replace(',', ''),
        }

        for key, value in cleaned_item.items():
            if value.strip() == '' or value.strip().lower() == 'n/a' or value.strip().lower() == 'none':
                cleaned_item[key] = '0'

        cleaned_data.append(cleaned_item)

    # Cache the cleaned data
    cache.set(COVID_DATA_CACHE_KEY, cleaned_data, COVID_DATA_TIMEOUT)

    return cleaned_data


def stats(request):
    oversatas = fetch_covid_data()

    countrynames = None
    countrydet = 'world'

    if request.method == 'POST':
        coname = request.POST.get('countrysearch').lower()

        # Fetch country names from the database (assuming a Country model)
        countrynames = [cou.country.lower() for cou in Country.objects.all()]

        if coname in countrynames:
            countrydet = coname
        else:
            messages.warning(request, 'Please enter a correct country name ')
            countrydet = 'world'

    response = requests.get('https://covid-19.dataflowkit.com/v1/' + countrydet)
    data = response.json()

    active_cases = data.get('Active Cases_text').replace('+', '')

    fields_with_commas = ['New Cases_text', 'New Deaths_text', 'Total Cases_text', 'Total Deaths_text',
                          'Total Recovered_text']
    for field in fields_with_commas:
        data[field] = data[field].replace(',', '')

    paginator = Paginator(oversatas, 9)

    page = request.GET.get('page')
    try:
        overalworld = paginator.page(page)
    except PageNotAnInteger:
        overalworld = paginator.page(1)
    except EmptyPage:
        overalworld = paginator.page(paginator.num_pages)

    context = {
        'Active': active_cases,
        'Update': data.get('Last Update').replace('+', ''),
        'new_cases': data.get('New Cases_text').replace('+', ''),
        'Country': data.get('Country_text'),
        'new_deaths': data.get('New Deaths_text').replace('+', ''),
        'total_cases': data.get('Total Cases_text').replace('+', ''),
        'total_deaths': data.get('Total Deaths_text').replace('+', ''),
        'recovered': data.get('Total Recovered_text').replace('+', ''),
        'overalworld': overalworld,
    }

    for key, value in context.items():
        if value == '':
            context[key] = "0"

    return render(request, 'stats.html', context)


def resorse(request):
    context = RandRdetails.objects.all()
    return render(request, 'Recovery & Resources.html', {'context': context})


def about(request):
    return render(request, 'about.html')


from datetime import datetime  # Import the datetime class from the datetime module

def contact(request):
    if request.method == 'POST':
        current_date = datetime.today()
        name1 = request.POST.get('name')
        phnum1 = request.POST.get('phnum')
        email1 = request.POST.get('email')
        feedback1 = request.POST.get('feedback')
        contact = Contact(date=current_date, name=name1, phnum=phnum1, email=email1, feedback=feedback1)
        contact.save()
        messages.success(request,'<strong>Success!</strong> Thank you for your submission! We will get back to you soon.')

        message = (
            f"Hello {name1},\n\nThank you for your submission! We have received your concern, and we respect it. "
            f"We will get back to you soon.\n\nPlease check your comments/Feedback/request below:\n\n{feedback1}\n\n"
            'py\n\n'
            "This is an automated email. Please do not reply to this message.\n\n"
            "Regards from the COVID-19 Tracking Website"
        )

        send_mail(
            "Thank you for your submission! We will get back to you soon.",
            message,
            "covid.19.4780177@gmail.com",
            [email1],
            fail_silently=True,
        )

        send_mail(
            f"contact form from {name1}",
            f"You have received a contact form from Mr. or Mrs. {name1}. For further details, please check the COVID-19 website.",
            "covid.19.4780177@gmail.com",
            ["covid.19.4780177@gmail.com"],
            fail_silently=True,
        )

    return render(request, 'contact.html')



def privacy(request):
    return render(request, 'privacy.html')


# get country names to auto fill

def get_country(request):
    search = request.GET.get('search')
    payload = []
    if search:
        objs = Country.objects.filter(country__icontains=search)

        for obj in objs:
            payload.append(
                {
                    'country': obj.country
                }
            )

    return JsonResponse(
        {
            'status': True,
            'payload': payload
        }
    )


def error_404(request, exception):
    return render(request, 'changepassword.html')


def adminlogin(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('welcome')
        else:
            messages.error(request, 'Invalid login credentials')


    if request.user.is_authenticated:
        return redirect('welcome')

    return render(request, 'adminlogin.html')

@login_required
def welcome(requests):
    return render(requests, 'welcome.html')


@login_required
def contactdet(requests):
    contacts = Contact.objects.all()

    return render(requests, 'contactdet.html', {'contacts': contacts})

contentforrandr =dict()


from django.contrib.auth import logout
@login_required
def custom_logout(requests):
    logout(requests)
    return redirect('adminlogin')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')
