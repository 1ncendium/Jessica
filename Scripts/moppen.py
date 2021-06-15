import random

# Maak een lijst voor wat er vooraf gezegd wordt..
vooraf = {
    "spraak1": "Laat mij even denken",
    "spraak2": "Je humeur bevalt mij, eens even kijken of ik nog iets weet",
    "spraak3": "Jaja deze ken je echt nog niet!",
    "spraak4": "Eens even denken"
}

# Maak een lijst voor de moppen..
moppen = {
    "mop1": "Er zitten 2 vliegen op de kale kop van een oude man zegt de een tegen de ander: " + "Weet je nog dat we hier vroeger verstoppertje speelden",
    "mop2": "Het loopt in de wei, en helpt tegen menstuatie? " + 'Een tampony',
    "mop3": "Loopt een 0 over straat, komt ie een 8 tegen: " + "Zeg, zit je riem niet een beetje te strak?",
    "mop4": "Er zijn 15 visjes 5 verdrinken er hoeveel blijven er dan over." + "15, visjes kunnen niet verdrinken",
    "mop5": "vrouwen zijn net als typex,eerst zijn ze je type en dan je ex",
    "mop6": "Er lope 2 tomaten op straat en steken over aan de overkant is een vrouwen tomaat zegt de ene tomaat tegen de andere tomaat je hoeft niet zo rood te worden hoor",
    "mop7": "Leven met obesitas is best wel zwaar",
    "mop8": "Heeft een brandweerman ook recht op een rookvrije werkplek?",
    "mop9": "Een kampeerwinkel die de tent moet sluiten is nooit grappig",
    "mop10": "Het leven is net als Lucille Werner. Het kan raar lopen!"
}

# Ik maak een functie aan die willekeurig een zin kiest uit de bovenstaande lijst. Deze zin wordt afgespeeld voordat de mop wordt verteld.
def spraak():
    spraak = random.choice(list(vooraf.values()))
    return spraak

# Ik maak een functie aan die willekeurig een mop kiest uit de bovenstaande lijst
def random_mop():
    mop = random.choice(list(moppen.values()))
    return mop