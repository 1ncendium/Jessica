#########################################################################
# Project titel: Jessica
# Datum: 14 april 2021
# Project auteur: Incendium
# Beschrijving: Jessica is een persoonlijke voice-assistant gemaakt met Python!
# Versie: 1.0
# Getest op: Windows 10
# Github: https://github.com/1ncendium
#########################################################################
from __future__ import print_function
import os
import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
from playsound import playsound
import operator
from googleapi import google
from gtts import gTTS
from Scripts import moppen
from Scripts import datum
from Scripts import corona
from Scripts import weerbericht
import locale
import os.path
import tkinter as tk
from tkinter import *
import threading
import webbrowser
import traceback

# Opties voor Jessica. Nederlandse tijdzone / benoemingen van tijd, Wikipedia op NL voor het raadplegen van informatie en natuurlijk een Nederlandse voice om gekke uitspraken te vermijden.
wikipedia.set_lang('NL')
nl_voice_id = "dutch" # Dutch Voice..
locale.setlocale(locale.LC_TIME, 'nl_NL.UTF-8')

# Hier maak ik een functie om Jessica te laten praten.
# De Google Text-to-Speech module stop ik in een tts (Text To Speech) variabele met de taal die ik hierboven heb gespecificeerd
# Ik maak een variabele aan voice.mp3 waar de output van Jessica altijd naar toe wordt opgeslagen. Daarna speel ik deze met de playsound module af om zo daadwerkelijk geluid uit Jessica te krijgen.
# Ik verwijder de file daarna omdat Windows anders stom doet met permissions voor het overschrijven.
def talk(text):
    tts = gTTS(text=text, lang='nl', slow=False)
    filename = "voice.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

# Hier maak ik een luister functie om commando's op te vangen van de gebruiker.
# De default microfoon van de host wordt gebruikt als source.
# Ik stel in dat achtergrond geluid geminimaliseerd wordt.
# Ik stel in dat Jessica maximaal 5 seconden luistert, daarna wordt de input verklaard als "None" als er niets wordt gezegd.
# Nederlands stel ik in als taal om de input op te baseren.
def listen():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            voice = r.listen(source, phrase_time_limit=4)
            command = r.recognize_google(voice, language="nl-NL")
            command = command.lower()
            return command
    except Exception as e:
        log = open('../log.txt', 'w')
        log.write(e)

# Nu alle opties klaar zijn om te kunnen praten met Jessica, maak ik een functie die het antwoord op de input definieert.
# Eerst roep ik de listen() functie aan.
# Op basis van de input (command) maak ik een antwoord.
# Eerst if/else ik om zeker te weten dat "Jessica" is vermeld in het hele commando.
def run_jessica():
        try:
            command = listen()

            # Met de pywhatkit module kan ik op basis van een string op youtube zoeken naar bepaalde videos.
            # Pywhatkit zoekt met een API op youtube naar de topic (commando) die is doorgegeven op youtube en kiest tussen de resultaten de bovenste video uit.
            if 'muziek' in command or 'speel af' in command:
                if 'start muziek' in command or 'speel af' in command:
                    song = command.replace('jessica start muziek', '').replace('jessica speel af', '').replace('speel af', '').replace('start muziek', '')
                    pywhatkit.playonyt(song, use_api=True)
                    talk('Ik speel ' + song + 'voor je af')

            # Wanneer er "hoe laat" of "de tijd" is gezegd verteld Jessica de tijd met datetime.
            # Tijd wordt aangegeven met %H = 0-23 en %M = 0-59
            elif 'hoe laat' in command or 'de tijd' in command:
                time = datetime.datetime.now().strftime('%H:%M')
                talk('Het is nu ' + time)
                print("test")

            # Wanneer de "datum" opgevraagd wordt, wordt de functie time() in datum.py aangeroepen.
            # Deze functie zorgt er in een notendop voor dat de datum in het Nederlands wordt vertaald door de maanden van het jaar te hernoemen.
            elif 'datum' in command:
                date = datum.time()
                talk(date)

            # Met de Wikipedia module en de Google API module kan ik gaan zoeken naar informatie online.
            # Eerst wordt het onderwerp dat in de vraag voorkomt gezocht op Wikipedia, als er geen (Nederlands) artikel van bestaat, wordt er gezocht op Google.
            # Google zal zoeken op de eerste pagina van de zoekresultaten, als resultaat 1 niet werkt, dan pakt hij resultaat 2 daarna 3.
            elif 'wat betekent' in command or 'wie is' in command or 'zoek op' in command or 'hoeveel kost' in command:
                command.replace('wat betekent', '').replace('wie is', '').replace('zoek op', '')
                try:
                    talk(pywhatkit.info(command))
                except wikipedia.PageError:
                    try:
                        num_page = 1
                        search_results = google.search(command, num_page)
                        talk(search_results[2].description)
                    except IndexError:
                        num_page = 1
                        search_results = google.search(command, num_page)
                        talk(search_results[3].description)

            # Jessica kan ook een mop vertellen!
            # Ook voor deze vraag worden er functies in een ander script aangeroepen. Deze functies hebben een lijst met moppen en wat er vooraf gezegd wordt. Met "Random" wordt er een willekeurig uitgekozen.
            # Vooraf en na  het vertellen van een mop wordt een geluid afgespeeld.
            elif 'mop' in command:
                mop = moppen.random_mop()
                vooraf = moppen.spraak()
                talk(vooraf)
                playsound('..\Files/drum_mop.mp3')
                talk(mop)
                playsound('..\Files/tada_mop.mp3')

            # Jessica is ook super slim! Jessica kan sneller rekenen dan wie dan ook.
            # Op basis van de rekensom vraag filter ik welke operator (wat voor som) er gebruikt dient te worden om de som uit te rekenen. Jessica ondersteunt tot nu (min, plus, keer, delen en machten)
            # Ik maak een if/else statement zodat "gedeeld door" omgezet wordt naar "gedeeld" en "tot de macht" omgezet wordt naar "macht"
            # De functie calculate() begint met get_operator_fn(). Hier definieer ik aan welke operator een string gelijk staat met de "operator" module.
            # Dan komt te functie eval_binary_expr(). Deze functie gebruik ik om de twee getallen + operator om te vormen naar een som.
            # Als laatste wordt doormiddel van de eval_binary_expr() functie en de "command" (de input van de gebruiker)
            elif 'bereken' in command or 'reken uit' in command:
                command = command.replace('jessica', '').replace('hey jessica', '').replace('jsk', '').replace('isca', '').strip()
                try:
                    command = command.replace('bereken', '').replace('reken uit', '')
                    if 'gedeeld door' in command:
                        command = command.replace('gedeeld door', 'gedeeld')
                    if 'tot de macht' in command:
                        command = command.replace('tot de macht', 'macht')

                    def calculate():
                        def get_operator_fn(op):
                            return {
                                'plus': operator.add,
                                'min': operator.sub,
                                'keer': operator.mul,
                                'gedeeld': operator.__truediv__,
                                'macht': operator.pow
                            }[op]

                        def eval_binary_expr(op1, oper, op2):
                            op1, op2 = int(op1), int(op2)
                            return get_operator_fn(oper)(op1, op2)

                        answer = eval_binary_expr(*(command.split()))
                        # Als het antwoord heel veel nullen (0'en) bevat dan duurt het heel lang om dit uit te spreken en lijkt het net alsof Jessica vastloopt.
                        # Om dit te voorkomen maak ik een if/else statement. Als het antwoord groter is dan 1 triljoen, wordt het antwoord niet uitgesproken.
                        if answer <= 999999999999:
                            talk('het antwoord is ' + str(answer))
                        else:
                            talk('Je antwoord is te groot om uit te spreken')
                    calculate()
                except:
                    talk('Probeer het nog eens asjeblieft.')

            # Op basis van BMI, kan Jessica bepalen wat de score is van jouw gewicht.
            # De BMI formule luidt als volgt: gewicht (in KG) / (meter in het kwadraat)
            # Ik vraag dus eerst aan de gebruiker wat zijn of haar lengte is. Hierbij maakt het niet uit wat de gebruiker naast de exacte aantal centimeters zegt.
            # Ik neem namelijk alleen alle integers mee naar het antwoord met re.sub.
            # Veel mensen hebben de neiging om 1 meter 80 te zeggen, daarom heb ik er voor gezorgd dat wanneer de lengte in CM onder de 100 komt, automatisch 100 centimeter erbij op wordt geteld.
            # De BMI score wordt verteld in een verhaaltje met een if/else statement, zodat er daadwerkelijk feedback is!
            elif 'ben ik dik' in command or 'werk dick' in command or 'heb ik overgewicht' in command or 'bmi' in command:
                def bmi():
                    try:
                        talk('Hoeveel kilogram weeg je?')
                        kilogram = listen()
                        res = re.sub("\D", '', kilogram)
                        kg = float(res)

                        talk('Hoeveel centimeter lang ben je?')
                        length = listen()
                        res = re.sub("\D", '', length)
                        meter = float(res) / 100.0
                        if meter < 1:
                            meter = meter + 1

                        answer = round(kg / (meter * meter), 2)
                        if answer >= 12.5 and answer <= 18.5:
                            talk('Je hebt ondergewicht, probeer aan te komen of zoek hulp')
                        elif answer > 18.5 and answer < 24.9:
                            talk('Je gewicht past mooi bij je lengte, hou dit vol')
                        elif answer > 24.9 and answer < 29.9:
                            talk('Je hebt overgewicht, probeer af te vallen')
                        elif answer > 29.9 and answer < 34.9:
                            talk('Je hebt obesitas bezoek een huisarts voor hulp')
                        elif answer > 34.9 and answer < 43:
                            talk('Je hebt zware obesitas bezoek snel een huisarts voor hulp')
                        else:
                            talk('Je houdt me voor de gek')
                    except Exception:
                        # Als het toch mis gaat, wordt met een if/else statement gevraagd of je het nog eens wilt proberen. Alleen bij Ja wordt de BMI() functie weer aangeroepen.
                        talk('Sorry, dat snap ik niet. Wil je dit nog eens proberen?')
                        command = listen()
                        if "ja" in command or "jahoor" in command or "jawel" in command or "oke" in command:
                            bmi()
                        else:
                            pass
                bmi()

            # Met een weer API van weerlive.nl haal ik de weer statistieken op met urllib. De gegevens worden ingeladen met json.
            # Op basis van alle informatie maak ik een weerbericht.
            elif 'weer' in command:
                command = command.replace('jessica', '').replace('hey jessica', '').replace('jsk', '').replace('isca', '').strip()
                try:
                    weer = weerbericht.weer(command)
                    talk(weer)
                except Exception:
                    talk("Ga naar de instellingen en voer de API code in om het weer op te vragen")

            # Ik kon dit gewoon niet laten :)
            elif 'incendium' in command and 'cool' in command or 'incendium' and 'awesome' in command:
                talk('Dat is hij zeker')

            # Met een covid-19 API haal ik de informatie van Nederland op. Dit op dezelfde manier als met weer API.
            # De coronastatistieken worden rond 14:00 vrijgegeven. Als de vraag dus voor 14:00 wordt gesteld, geeft Jessica de data van gisteren.
            # In corona.py staat het script op de coronastatistieken op te halen met json.
            elif 'corona' in command:
                timeNow = datetime.datetime.now().strftime('%H:%M')
                newTime = int(timeNow.replace(':', ''))

                if newTime < 1500:
                    talk('De coronacijfers van vandaag zijn nog niet bekend, daarom geef ik je de cijfers van gisteren')

                coronaVar = corona.coronaAPI()
                talk(coronaVar)

            # Met "goedemorgen" kun je een samenvatting ophalen van de dag, deze speelt Jessica dan achter elkaar af.
            # Ik heb nu 2 programma's, waar 2 langer is dan 1.
            elif 'goedemorgen' in command:
                def goedemorgen():
                    talk('Goedemorgen, welk programma kan ik voor je draaien? Kies tussen 1 of 2')
                    programma = listen()

                    # Programma 1 = Tijd + datum + Weerbericht.
                    # Het weerbericht heeft altijd een locatie nodig, daarom heb ik "Amsterdam" gekozen omdat dit de hoofdstad is.
                    if '1' in programma or 'een' in programma or 'één' in programma:
                        # Tijd + Datum
                        time = datetime.datetime.now().strftime('%H:%M')
                        datumvandaag = datum.time()
                        talk('Het is nu ' + time)
                        talk('De datum is' + datumvandaag)
                        weerbericht.weer("Amsterdam")

                    # Programma 2 = Tijd + datum + Weerbericht + Corona statistieken.
                    elif '2' in programma or 'twee' in programma:
                        # Tijd + Datum
                        time = datetime.datetime.now().strftime('%H:%M')
                        datumvandaag = datum.time()
                        talk('Het is nu ' + time)
                        talk('De datum is' + datumvandaag)

                        weerbericht.weer("Amsterdam")

                        # Corona statistieken
                        talk('Dan komen nu de Corona statistieken')
                        coronaStats = corona.coronaAPI()
                        talk(coronaStats)

                    # Wanneer er iets anders wordt gezegd dan 1 of 2, vraagt Jessica of je het nog eens wilt proberen. Hier kan vervolgens "Ja" of "Nee" op gezegd worden.
                    else:
                        talk('Dat programma bestaat niet, kies tussen 1 of 2')
                        talk('Wil je het nog een keer proberen?')
                        command = listen()

                        if "ja" in command or "jahoor" in command or "jawel" in command or "oke" in command:
                            goedemorgen()
                        else:
                            pass
                # Hier roep ik de functie aan
                goedemorgen()

                talk('Ik wens je voor de rest een fijne dag')

            # Wanneer Jessica een vraag niet kan beantwoorden moet er ook een antwoord komen inplaats van een error.
            # Als er niets wordt gezegd, wordt de input als "None" verklaard, dit pak ook op. En stuur een antwoord dat Jessica het niet snapt.
            elif 'None' in command or '' in command:
                print("test")
                talk('Dat snap ik niet helemaal')
            elif 'WikiFout' in command:
                talk('Daar kan ik geen informatie over vinden')
            else:
                talk('Dat snap ik niet helemaal')
                print("test")

        except Exception:
            log = open('../log.txt', 'w')
            log.write(traceback.format_exc())

"""
Hier maak ik een interface met tkinter voor een makkelijke interactie met Jessica.
Doormiddel van "Threading" zorg ik er voor dat de mainloop van tkinter niet vastloopt wanneer een ander proces zoals Jessica wordt gestart.

"""

# Ik maak eerst een "root" aan, dit is de basis van het programma. Hier vertel ik de omvang in pixels, achtergrond kleur, dat het programma niet resizable is (Venster kan dus niet groter gemaakt worden)
# Daarna definieer ik een aantal functies die later gebruikt zullen worden wanneer er op een knop wordt geklikt in de tkiner gui.
# Ik maak een frame aan die in de root staat. In de frame neem ik vervolgens de buttons en text mee.
# Ook definieer ik de titel + icon van het programma.
def interface():
    root = tk.Tk()

    canvas = tk.Canvas(root, height=600, width=400, bg="#87CEEB")
    root.resizable(False, False)
    canvas.pack()

    # Functie wanneer er op de "Jessica" button wordt geklikt. Deze functie start de functie (run_jessica()) in jessica.py
    # Ook wordt er een "Label" gemaakt die laat weten, dat Jessica aan het luisteren is. Dit wordt aangegeven met de tekst "Aan het luisteren..."
    def run():
        # Hier maak ik een Label aan die laat weten dat Jessica aan het luisteren is.
        titelLuisteren = Label(frameMain, text="Aan het luisteren...", bg="#87CEEB", fg="white")
        titelLuisteren.place(x=165, y=400, anchor="center")
        titelLuisteren.config(font=("Helvetica 18", 12))
        run_jessica()
        titelLuisteren.destroy()

    # Dit is de help functie, deze opent de help.html pagina. Hier zullen alle commandos die Jessica ondersteund opgenomen zijn.
    def help():
        os.system("..\help\index.html")

    # Met Thread draai ik de bovenstaande run() functie zodat de mainloop van tkinter hier geen last van heeft.
    def threadRun():
        tR = threading.Thread(target=run)
        tR.start()

    # Met Thread draai ik de bovenstaande help() functie zodat de mainloop van tkinter hier geen last van heeft.
    def threadHelp():
        tH = threading.Thread(target=help)
        tH.start()

    # Hier maak ik een instellingen window, voor bijvoorbeeld de weer API
    def instellingen():
        top = Toplevel()
        top.title('Instellingen')
        top.iconbitmap('icon.ico')
        # Canvas
        canvasSettings = tk.Canvas(top, height=600, width=400)
        # Frame voor settings
        canvasSettings.pack()
        frameInstellingen = tk.Frame(top, bg="#87CEEB", bd=0)
        frameInstellingen.place(relwidth=1, relheight=1)

        # Titel voor de instellingen
        titelInstellingen = Label(frameInstellingen, text="Instellingen", bg="#87CEEB", fg="black")
        titelInstellingen.place(x=40, y=40)
        titelInstellingen.config(font=("Helvetica 18 bold", 18))

        # Text voor API key weer
        titelAPIKey = Label(frameInstellingen, text="Weer API key", bg="#87CEEB", fg="black")
        titelAPIKey.place(x=40, y=90)
        titelAPIKey.config(font=("Helvetica 18 bold", 12))

        # Maak een functie voor de API key
        apiKey = Entry(frameInstellingen, width=40)
        placeholder = open('../Scripts/weerapikey.txt').read()
        apiKey.insert(0, placeholder)
        apiKey.place(x=40, y=120)

        # Maak een functie om de API key op te halen
        def saveKey():
            key = apiKey.get()
            filename = open('../Scripts/weerapikey.txt', "w")
            filename.write(key)
            filename.close()

        def getKey():
            webbrowser.open('https://weerlive.nl/api/toegang/')

        # Maak een button om de API key door te geven
        SaveButton = Button(frameInstellingen, text="Opslaan", command=saveKey)
        SaveButton.place(x=40, y=160)

        # Maak een button om de API key op te vragen
        krijgAPIButton = Button(frameInstellingen, text="Opvragen", command=getKey)
        krijgAPIButton.place(x=120, y=160)

    # Hier maak ik een menu in die boven in de tkinter GUI komt te staan.
    menu = Menu(root)
    root.config(menu=menu)
    root.title('Jessica')
    icon = PhotoImage(file='.\icon.png')
    root.iconphoto(False, icon)

    # Ik voeg aan het menu "Help" toe met het commando "ThreadHelp()" (deze functie wordt dan dus aangeroepen)
    menu.add_command(label="Help", command=threadHelp)

    menu.add_command(label="Instellingen", command=instellingen)

    # Hier maak ik de frame aan.
    frameMain = tk.Frame(root, bg="#87CEEB", bd=0)
    frameMain.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # Dit is een "label" / text. Dit geeft de text "Klik om iets te zeggen" weer.
    titel = Label(frameMain, text="Klik om iets te zeggen", bg="#87CEEB", fg="white")
    titel.place(x=160, y=450, anchor="center")
    titel.config(font=("Helvetica 18", 18))

    # Dit is de button voor Jessica
    photo = PhotoImage(file=".\jessica.png")
    jessica = Button(frameMain, text='Click Me !', image=photo, borderwidth=0, bg="#87CEEB", command=threadRun)
    jessica.place(x=100, y=225)

    root.mainloop()

interface()