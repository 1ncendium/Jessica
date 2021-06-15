"""

1. Ga naar https://weerlive.nl/api/toegang/index.php
2. Registreer op de website
3. Binnen een aantal uren zou er een mail gestuurd moeten worden naar het mail-adres waarmee is geregistreerd.
Of login op https://weerlive.nl/api/toegang/login.php en kijk of de API key inmiddels is te raadplegen.

"""
def weerAPI():
    API_key = open('Scripts/weerapikey.txt').read()
    print(API_key)
    return API_key
weerAPI()