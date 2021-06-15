import urllib.request
import json

# Hier maak ik een functie aan die later aangeroepen kan worden vanaf jessica.py voor het ophalen van Corona statistieken
# Met deze API haal ik de nieuwe besmettingen en overleden mensen op uit Nederland. Daarnaast de totale aantal besmettingen en doden van Nederland.
def coronaAPI():
   # API data
   covid_api = 'https://api.covid19api.com/summary'
   jso = urllib.request.urlopen(covid_api)
   data = json.load(jso)

   # Hier geef ik de lengte op van de lijst met landen. Ook definieer ik hier het land waar naar gezocht moet worden.
   scope = data['Countries']
   country = 'Netherlands'

   # Hier zoek in Nederland op in de API en vervolgens haal ik de data op.
   for i in range(len(scope)):
       if country in data['Countries'][i]['Country']:
           infectedToday = str(data['Countries'][i]['NewConfirmed'])
           deceasedToday = str(data['Countries'][i]['NewDeaths'])
           infectedTotal = str(data['Countries'][i]['TotalConfirmed'])
           deceasedTotal = str(data['Countries'][i]['TotalDeaths'])
           coronaVar = 'vandaag zijn er' + infectedToday + 'besmettingen en' + deceasedToday + 'doden bijgekomen.' + 'In totaal zitten we op' + infectedTotal + 'besmettingen en' + deceasedTotal + 'doden.'
           return coronaVar

