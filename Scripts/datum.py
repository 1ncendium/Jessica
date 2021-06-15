import datetime

# Met datetime geef ik de tijd als volgende vorm: Eerst de dag, dan de maand, dan het jaar.
# Ik vervang de naam van de maand naar het Nederlands
def time():
    today = datetime.datetime.now().strftime('%d %B %Y')
    datum = today.replace('January', 'Januari').replace('February', 'Februari').replace('March', 'Maart').replace('May', 'Mei').replace('June', 'Juni').replace('July', 'Juli').replace('August', 'Augustus').replace('October' , 'Oktober')
    return datum