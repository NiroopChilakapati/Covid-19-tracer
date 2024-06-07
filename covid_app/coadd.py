import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable to point to your project's settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid_project.settings")

# Initialize Django
django.setup()

from covid_app.models import Country  # Replace 'covid_app' with your actual app name
import requests

l = []

response = requests.get('https://covid-19.dataflowkit.com/v1')
data = response.json()
for item in data:
    l.append(item.get('Country_text', 'N/A'))

print(l)

for i in l:
    Country.objects.create(
        country=i
    )
