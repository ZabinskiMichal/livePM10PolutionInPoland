import pandas as pd
import requests
import csv
import gspread

#pobiera informacje o wszystkich stacjach
stacje = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'

# #pobiera informacje o wszystkich stanowisskach pomarowych z danej stacji
# #PARAMETR -> ID_STACJI
# stanowiskoPomiarowe = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/14'

#pobiera informacje o PM10 dla danego stanowiska
#PARAMETR -> ID STANOWISKA
pomiarZeStanowiska = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/92'

#musimy zgarnac wszystkie id sacji pomiarowych
#kazdej stacji wziac jedno stanowisko
#pobrac z niego najnowszy pomiar


#1) zapisanie id itp wszystkich stacji do csv -----------------------------------------
wszystkieStacje = requests.get(stacje).json()

data_file = open('stacjeApi.csv', 'w')
csv_writer = csv.writer(data_file)
count = 0
for stacja in wszystkieStacje:
    if count == 0:
        # Writing headers of CSV file
        header = stacja.keys()
        csv_writer.writerow(header)
        count += 1
    # Writing data of CSV file
    csv_writer.writerow(stacja.values())
data_file.close()

#2) z pliku csv wezmiemy pierwsza kolumne ----------------------

# reading CSV file
data = pd.read_csv("stacjeApi.csv")

# converting column data to list
idStacji = data['id'].tolist()

# printing list data
print('IdTo:', idStacji)

#mamy liste z id istniejacych stacji pomiarowych

#3)dla kazdego id stacji wezmiemy dane z jednego stanowiska pomiarowego i zapiszemy do kolejnej listy

#pobiera informacje o wszystkich stanowisskach pomarowych z danej stacji
#PARAMETR -> ID_STACJI


stanowiskoPomiarowe = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
wynikiPomiarowZeStanowiska = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'

# listaStanowisk = []
listaStanowiskZPomiarem = []
# #dla kazdej stacji bierzemy t
for j in idStacji:
    # stanowiskoJson = requests.get(stanowiskoPomiarowe + str(j)).json()[0]
    stanowiskaJson = requests.get(stanowiskoPomiarowe + str(j)).json()

    #peetla sprawdzajaca czy stacja pmiarowa w danym stanowisku

    #stanowisko jest słownikiem
    for stanowisko in stanowiskaJson:

        #tutaj mozna ustalic dowolny parametr ktory chcemy zbadac
        if (stanowisko.get('param')).get('paramName') == 'pył zawieszony PM10':
            # print(stanowisko)

            #dla tego id stanowiska wykonujemy kolejne zapytanie o juz konkretne wyniki pomiarow
            idStanowiska = stanowisko.get('id')

            #jako argument w endpoincie przekazujemy sensonr ID czyli pole o nazwie id ze stanowiska
            wynikPomiaru = requests.get(wynikiPomiarowZeStanowiska + str(idStanowiska)).json()

            #mozna by wziac pomiar sprzed okolo 3/4 h poniewaz najnowesze nie zawsze sa zaktualzuzowane
            #tutaj mamy wyniki pomiarow sprzed 3h


            if(len(wynikPomiaru.get('values')) > 0):
                #sprzed 3h
                wynikiSprzedGodziny = wynikPomiaru.get('values')[3]
                stanowisko.update(wynikiSprzedGodziny)
                print(stanowisko)
                listaStanowiskZPomiarem.append(stanowisko)
                print('---')
            # stacjaZPomiarem["wyniki"].append(wynikiTrzeciejGodziny)


data_file1 = open('stanowiskaZPomiarami.csv', 'w')

csv_writer = csv.writer(data_file1)
count1 = 0
for stanowisko in listaStanowiskZPomiarem:
    if count1 == 0:
        # Writing headers of CSV file
        header = stanowisko.keys()
        csv_writer.writerow(header)
        count1 += 1
    # Writing data of CSV file
    csv_writer.writerow(stanowisko.values())
data_file1.close()


#pozostało wczytać plik csv z informacjami i stanowiskachZpomiarami
#i to zmergowac po id stacji


stacjeDoMerge = pd.read_csv("stacjeApi.csv")
stacjeDoMerge = stacjeDoMerge.fillna(value='0')

stanowiskaDoMerge = pd.read_csv('stanowiskaZPomiarami.csv')
stanowiskaDoMerge = stanowiskaDoMerge.fillna(value='0')

stcjeIStanowiskaZlaczone = pd.merge(stacjeDoMerge, stanowiskaDoMerge, left_on="id", right_on="stationId", how='right')
stcjeIStanowiskaZlaczone = stcjeIStanowiskaZlaczone.fillna(value='0')
# plik = stcjeIStanowiskaZlaczone
stcjeIStanowiskaZlaczone.to_csv("wynikiOrazStacje.csv")
# stcjeIStanowiskaZlaczone.to_csv("wynikiOrazStacje.csv")

plik = pd.read_csv('wynikiOrazStacje.csv')

plik = plik.fillna(value='0')
plik = plik.values.tolist()
sa = gspread.service_account()
sh = sa.open("geoportaleProjekt")
wks = sh.worksheet("Arkusz1")
wks.clear()
plik.insert(0, ['id', 'id_x', 'stationName', 'gegrLat', 'gegrLon', 'city', 'addressStreet', 'stance_id', 'stationId', 'param', 'date', 'value'])
wks.update(plik)








