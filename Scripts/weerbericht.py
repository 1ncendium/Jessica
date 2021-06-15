import urllib.request
import json

# Met een weer API van weerlive.nl haal ik de weer statistieken op met urllib. De gegevens worden geladen met json.
# Als er een foutmelding uit de locatie voorkomt, wordt de locatie naar Amsterdam gezet. En wordt dus het weerbericht van Amsterdam verteld.
# Uit de API wordt de temperatuur, gevoelstemperatuur, windrichting, windsnelheid en de samenvatting opgehaald.
# Omdat de API werkt met afkortingen van de windrichtingen, vertaal ik deze naar het hele woord.
# Op basis van alle informatie maak ik een weerbericht.
def weer(command):
    apikey = open('..\Scripts/weerapikey.txt').read()
    location = command
    new = location.replace('weer in', '').strip()
    apiurl = 'http://weerlive.nl/api/json-data-10min.php?key={apikey}&locatie={location}'.format(apikey=apikey,
                                                                                                 location=new)
    try:
        jso = urllib.request.urlopen(apiurl)
    except Exception:
        apiurl = 'http://weerlive.nl/api/json-data-10min.php?key={apikey}&locatie=amsterdam'.format(apikey=apikey)
        jso = urllib.request.urlopen(apiurl)
    print(apiurl)
    data = json.load(jso)
    temp = round(float(data['liveweer'][0]['temp']))
    temp = str(temp)
    gtemp = round(float(data['liveweer'][0]['gtemp']))
    gtemp = str(gtemp)
    windr = data['liveweer'][0]['windr']

    if windr == 'NNO':
        windr = 'Noord noord oosten'
    elif windr == 'NO':
        windr = 'Noord oosten'
    elif windr == 'ONO':
        windr = 'Oost noord oosten'
    elif windr == 'OZO':
        windr = 'Oost zuid oosten'
    elif windr == 'ZO':
        windr = 'Zuid oosten'
    elif windr == 'ZZO':
        windr = 'Zuid zuid oosten'
    elif windr == 'ZZW':
        windr = 'Zuid zuid westen'
    elif windr == 'ZW':
        windr = 'Zuid westen'
    elif windr == 'WZW':
        windr = 'West zuid westen'
    elif windr == 'WNW':
        windr = 'West noord westen'
    elif windr == 'NW':
        windr = 'Noord westen'
    elif windr == 'NNW':
        windr = 'Noord noord westen'
    elif windr == 'Noord':
        windr = 'Noorden'
    elif windr == 'West':
        windr = 'Westen'
    elif windr == 'Oost':
        windr = 'Oosten'
    elif windr == 'Zuid':
        windr = 'Zuiden'

    # Ik rond de windsnelheid af en ik converteer het daarna weer naar een string.
    windsnlh = round(float(data['liveweer'][0]['windkmh']))
    windsnlh = str(windsnlh)

    samenv = data['liveweer'][0]['verw']

    # Hier maak ik een weerbericht van de informatie die is opgehaald.
    weer = 'De temperatuur ligt rond de ' + temp + ' graden ' + 'waarbij de gevoelstemperatuur rond de ' + gtemp + ' graden ligt. ' + 'De wind komt uit het ' + windr + ' met een snelheid van ' + windsnlh + ' kilometer per uur ' + 'Voor de rest ' + samenv
    return weer