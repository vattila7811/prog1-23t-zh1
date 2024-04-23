import json
import csv

varosok = ["Sopron", "Gyor", "Szombathely", "Budapest", "Veszprem", "Szekesfehervar", "Zalaegerszeg"]


def adatok_beolvas(varosok: list) -> list[dict]:
    adatok : list[dict] = []
    for varos in varosok:
        try:
            with open(varos + ".json", encoding="utf-8") as jsonfile:
                adat = json.load(jsonfile)
            adatok.append(adat)
        except Exception as ex:
            print(ex)
    return adatok


def print_csapadekos_napok(adatok: list[dict]):
    datumok = {adat['daily']['time'][idx] for adat in adatok for idx, csapadek in enumerate(adat['daily']['precipitation_hours']) if csapadek >= 1.0}
    print(f'Csapadékos napok száma: {len(datumok)}')


def print_max_szelsebesseg(adatok: list[dict]):
    maxwind = max([max(adat['daily']['windspeed_10m_max']) for adat in adatok])
    for varosidx, adat in enumerate(adatok):
        for idx, wind in enumerate(adat['daily']['windspeed_10m_max']):
            if wind == maxwind:
                print(f'Maximális szélsebesség: {wind} km/h, {varosok[varosidx]}, {adat["daily"]["time"][idx]}')
                return


def collect_max_szelsebesseg(adatok: list[dict]) -> dict:
    max_temps : dict = {}
    for varosidx, adat in enumerate(adatok):
        for idx, temp in enumerate(adat['daily']['temperature_2m_max']):
            datum = adat['daily']['time'][idx]
            napiadat = max_temps.get(datum, {})
            if napiadat == {} or napiadat['temp'] < temp:
                max_temps[datum] = {'temp' : temp, 'varos': varosok[varosidx]}
    return max_temps


def write_szeladatok_to_csv(szeladatok: dict):
    with open('max_temps.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for datum, ertek in szeladatok.items():
            filewriter.writerow([datum, ertek['temp'], ertek['varos']])



def main():
    adatok = adatok_beolvas(varosok)
    print_max_szelsebesseg(adatok)
    print_csapadekos_napok(adatok)
    szeladatok = collect_max_szelsebesseg(adatok)
    write_szeladatok_to_csv(szeladatok)

main()
    