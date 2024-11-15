import requests
from datetime import datetime

def H_Comp(h_value, q_m_f, q_m_I):
    # h_value = H-verdi
    # q_m_f = Quiet mean F
    # q_m_I = Quiet mean I
    
    return float(h_value) - (float(q_m_f) * float(q_m_I))



# Få dagens dato
today = datetime.today()
year = today.year
month = today.month
day = today.day

# Variabel for oppløsning
resolution = "1min"  # Du kan endre denne til ønsket verdi

# URL og parametere
url = "http://flux.phys.uit.no/cgi-bin/mkascii.cgi"
params = {
    "site": "dob1a",
    "year": year,
    "month": month,
    "day": day,
    "res": resolution,
    "pwd": "NonComPass99",
    "format": "html",
    "comps": "DHZ",
    "RTData": "+Get+Realtime+Data+",
}

try:
    # Gjør GET-forespørselen
    response = requests.get(url, params=params)
    response.raise_for_status()  # Hev feil for dårlig respons

    # Hent og prosesser responsdata
    data = response.text

    # Del dataen inn i linjer
    lines = data.splitlines()

    # Hent Quiet-verdier fra de første 6 linjene
    quiet_dec = None
    quiet_inc = None
    quiet_tot = None

    for line in lines[:6]:
        if "Quiet mean Dec:" in line:
            quiet_dec = float(line.split(":")[1].strip())
        elif "Quiet mean Inc:" in line:
            quiet_inc = float(line.split(":")[1].strip())
        elif "Quiet mean Tot:" in line:
            quiet_tot = float(line.split(":")[1].strip())

    # Nå er quiet-verdiene lagret i variablene
    # quiet_dec, quiet_inc, quiet_tot

    print("\nFørste komplette måledatasett:")

    # Iterer fra slutten for å finne første gyldige datasett
    for line in reversed(lines):
        parts = line.split()
        if len(parts) >= 7:  # Sørg for at linjen har nok kolonner
            date, time = parts[0], parts[1]
            values = parts[2:]  # Resten av verdiene

            # Sjekk om verdier inneholder "99999.9"
            if "99999.9" not in values:
                # Mappe verdier til spesifikke navn
                mapped_values = {
                    "Dec": values[0],
                    "Horizontal": values[1],
                    "Vertical": values[2],
                    "Incl": values[3],
                    "Total": values[4]
                }
                print(f"Dato: {date}, Tid: {time}, Verdier: {mapped_values}")
                print("Quiet mean Dec:", quiet_dec)
                print("Quiet mean Inc:", quiet_inc)
                print("Quiet mean Tot:", quiet_tot)
                print("H comp:", H_Comp(mapped_values["Horizontal"], quiet_dec, quiet_inc))
                
                break  # Stopp etter første gyldige datasett

except requests.exceptions.RequestException as e:
    # Håndter feil
    print("En feil oppstod:", e)
