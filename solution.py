import pytest
import matplotlib.pyplot as plt
from numpy import average as npmedel
import json
from math import dist
from pathlib import Path



def solution(sokvag):

    # Funktionen börjar med att definera de variabler och listor vi kommer att förlita oss på.
    # Direkt därefter kallas den första stödfunktionen för att validera att sökvägen som har angivits är en korrekt sökväg som existerar på systemet.
    # Om en korrekt sokväg hittas så läses json-filen in till en dictionary som i sin tur valideras i en till stödfunktion som kontrollerar att all data är i korrekt form.
    # Efter det mappas alla datorers namn och koordinater in i respektive lista så att samma index i samtliga listor motsvarar samma dator. 
    # Funktionen kallar sedan på nästa stödfunktion som mäter avståndet till varje punkts närmsta granne och får det svaret i form av en dictionary.
    # Funktionen definerar sen upp en tröskelfaktor (default är *1) och ett tröskelvärde som består av medelvärdet av avståndet till alla datapunkters närmsta granne. Min rekomendation är att man justerar tröskelvärdet upp eller ner beroende på om man hittar för många misstänkta eller för få misstänkta.
    # Med tröskelvärde och tröskelfaktorn samt en dictionary med alla datapunkters avstånd till närmsta granne kallas nästa hjälpfunktion som kollar om avståndet till närmsta granne är större än tröskelvärdet.  
    # In = Funktionen tar en sökväg som parameter.
    # Om programmet kallas på av en person så returners här värdet till kallaren oavsett om det är 1, 0 eller fler misstänkta med information om hur många misstänkta den nuvraande tröskelfaktorn har genererat.
    # Om programmet körs av pytest så utvärderas antalet misstänkta för att antingen höja ett exception eller returnera den enskilt misstänkta. 


    misstankt = None
    x_varden = []
    y_varden = []
    titlar = []
    fil = str(sokvag).rsplit('/',1)[-1]
    if validera_sokvag(sokvag) == True:
        print(f"Kontrollerar koordinater i filen {fil}")
        with open(sokvag, encoding="utf-8") as f:
            d = json.load(f)
            if data_validering(d) == True:
                for namn in d:
                    titlar.append(namn)
                    x_varden.append(d.get(namn)[0])
                    y_varden.append(d.get(namn)[1])

                alla_minsta_avstand = avstand(titlar, x_varden, y_varden)

                troskel_faktor = 1
                troskel = (troskel_faktor * npmedel(list(alla_minsta_avstand.values())))

                misstankt, antal_misstankta = kolla_ensam(alla_minsta_avstand, troskel)
                print(misstankt)
                if __name__ == "__main__":
                    return misstankt, antal_misstankta, titlar, x_varden, y_varden, troskel
                else:
                    if antal_misstankta == 1:
                        return misstankt
                    elif antal_misstankta == 0:
                        raise ValueError("Det finns inga misstänkta. Vänligen justera ditt tröskelvärde eller tröskelfaktorn.")
                    elif antal_misstankta > 1:
                        raise ValueError("Det finns fler än 1 misstänkt. Vänligen justera ditt tröskelvärde eller tröskelfaktorn.")
                    else:
                        return misstankt
            else:
                print("Något oväntat har hänt, du borde inte kunnat hamna här.")
                return

def avstand(titlar, x_varden, y_varden):

    # In = Funktionen tar listor med namn, x-koordinater och y-koordinater som parameter där samma index representerar samma datapunkt från den ursprungliga json-filen
    # Funktionen loopar över varje namn och dess koordinater och mäter avståndet till alla andra datapunkter för att hitta den närmsta grannen. 
    # Om loopen försöker jämföra en datapunkt med sig själv så kommer det varvet att skippas.
    # Avståndet till varje punkts närmsta granne läggs sen in tillsammans med punktens namn i en ny dictionary som returneras till den kallande funktionen.

    minsta_avstand_dict = {}
    for i in range(len(titlar)):
        minsta_avstand = None
        for n in range(len(titlar)):
            if titlar[i] is not titlar[n]:
                a = [x_varden[i], y_varden[i]]
                b = [x_varden[n], y_varden[n]]
                k = dist(a, b)
                if minsta_avstand == None:
                    minsta_avstand = k
                else:
                    if k > minsta_avstand:
                        continue
                    else:
                        minsta_avstand = k
            else:
                continue
        minsta_avstand_dict[titlar[i]] = minsta_avstand
    return minsta_avstand_dict


def kolla_ensam(minsta_avstand_dict, troskel):

    # Funktionen tar en dictionary som innehåller par av namn och avståndet till deras närmsta granne, samt tröskelvärdet som tidigare definerats
    # Funktionen jämför alla datornamns avstånd till närmsta granne och mäter det mot tröskelvärdet för att se om den ska räknas som "borta". 
    # Om datorn är borta läggs namnet till i en lista som senare returneras till kallaren.
    # Det finns en check för att kontrollera att det endast finns 1 misstänkt utifrån det angivna tröskelvärdet.

    avstand_samling = []
    misstankta = []
    antal_misstankta = 0
    for namn in minsta_avstand_dict.keys():
        avstand = minsta_avstand_dict[namn]
        avstand_samling.append(minsta_avstand_dict[namn])
        if avstand > troskel:
            misstankta.append(namn)
            antal_misstankta += 1
        else:
            continue
    if len(misstankta) > 1:
        misstankt = ", ".join(misstankta)
        print("Det finns fler än 1 misstänkt. Vänligen justera ditt tröskelvärde eller tröskelfaktorn.")
    elif len(misstankta) == 0:
        misstankt = None
        print("Det finns inga misstänkta. Vänligen justera ditt tröskelvärde eller tröskelfaktorn.")
    elif len(misstankta) == 1:
        misstankt = "".join(misstankta)
        print(f"{misstankt} är misstänkt!")
    return misstankt, antal_misstankta

def plot_map(misstankt, antal_misstankta, titlar, x_varden, y_varden, troskel):
    # Stöd-funktion som ritar upp en plot med alla datorers koordinater samt en cirkel runt vardera punkt motsvarande tröskelvärdets area för att visualisera fynd.
    # In, funktionen tar en sträng av misstänkta, en int med antal misstänkta, listan med titlar, x-värden, y-värden och tröskelvärdet.
    # Obs, man måste zooma in för att faktiskt se de olika punkterna i fall om att de ligger i ett kluster.
    while True:
        fraga_path = input("Vill du se en karta över var datorerna befinner sig? Ja/Nej ")
        if fraga_path.lower() == "ja":  
            break
        elif fraga_path.lower() == "nej":
            print("Ok, tack för att du använder det här programmet.")
            return
        else:
            print("Jag förstod inte det där svaret, vänligen försök igen")
    print("Ritar upp en karta. När du vill stänga av programmet så behöver du manuellt stänga ner kartan eller använda ctrl + c i terminalen för att avsluta.")
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    plt.scatter(x_varden, y_varden)
    if antal_misstankta == 1:
        plt.title(f"{misstankt} är ensam.")
    else:
        plt.title("Kunde inte identifiera en ensam dator.")
    for i, txt in enumerate(titlar):
        Drawing_colored_circle = plt.Circle(( x_varden[i] , y_varden[i] ), troskel, fill=False )
        ax.set_aspect( 1 )
        ax.add_artist( Drawing_colored_circle )
        ax.annotate(txt, (x_varden[i], y_varden[i]))
    plt.show()
    return


def get_path():
    # Det här är en stöd-funktion som frågar användaren om vilken fil som ska granskas.
    # Den försöker vara så snäll och hjälpsam som möjligt för att möjliggöra att vem som helst ska kunna ta över scriptet och köra det.
    # Funktionen börjar med en ja/nej frågar för att ta reda på om den ska använda current working directory (cwd) eller en absolut sökväg som användaren skriver in.
    # Om man väljer ja är funktionen snäll och skriver ut alla filer i cwd ifall man inte är helt säker på filnamnet man väntas skriva in.
    # Om man väljer nej ombeds man skriva in den absoluta sökvägen inklusive filnamnet och filändelsen.
    # Om man skulle skriva varken ja eller nej så loopas man tillbaka till början av loopen för att förhindra att programmet faller sönder.
    # När man har försett programmet med antingen filnamn eller absolut sökväg så kallas solution-funktionen med sökvägen som argument.

    while True:
        print(f"Programmet körs ifrån {Path.cwd()}")
        fraga_path = input("Ligger din fil i samma mapp som programmet körs ifrån? Ja / Nej: ")
        if fraga_path.lower() == "ja":
            for item in Path.cwd().iterdir():
                if item.is_dir():
                    continue
                else:
                    print(f"Fil: {item.name}")
            complete_file_path = Path.cwd() / input("Vad heter filen du vill granska? Svara med namn på din fil inklusive filmformat, exempel fil.txt: ")
            break
        elif fraga_path.lower() == "nej":
            complete_file_path = input("I filken mapp ligger din fil? Skriv den absoluta sökvägen inklusive filnamnet med filändelsen.\n Exempel: /home/ciso/kod/pythonkurs/inlamning/uppgift-2/access.log: ")
            break
        else:
            print("Jag förstod inte det där svaret, vänligen försök igen")
    sokvag = Path(complete_file_path)

    while True:
        try:
            with open(str(sokvag)) as f:
                print("Hittade en fil på den angivna platsen.")
        except FileNotFoundError:
            sokvag = Path(Path.cwd() / input("Det verkar som att något gick fel, vänligen skriv in filnamnet igen eller avbryt med ctrl+c om filen inte ligger i den nuvarande mappen. "))
        else:
            break
    return(sokvag)

def data_validering(d):
    # Stödfunktion som går igenom och kontrollerar all data som matas in via json-filen för att se att den följer korrekt format.
    # Kontrollerar att datan blir en dictionary, kontrollerar att det finns data alls, kontrollerar att det finns rätt antal fält samt att varje värde i respektive nyckel/värde-par är en lista.
    # Funktionen tar en dictionary och lyfter antingen en exception om något inte stämmer eller så returnerar den dictionaryt oförändrat.

    try:
        isinstance(d, dict)
    except TypeError:
        raise TypeError("Det verkar inte som att din datafil är i rätt format. Det förväntade formatet är en json-fil med data")
    else:
        if len(d) == 0:
            raise ValueError("Det verkar inte som att din datafil innehåller någon data.")
        else:
            for i, namn in enumerate(d):
                if len(d.get(namn)) > 2:
                    raise IndexError("Den angivna filen verkar har för många fält, filen behöver innehålla endast fälten {namn: [X, Y]}, vänligen kontrollera din fil och försök igen.")
                else:
                    try:
                        isinstance(namn, str) and isinstance(d.get(namn), list) and isinstance((d.get(namn)[0]), int) and isinstance((d.get(namn)[1]), int)
                    except IndexError:
                        raise IndexError(f"Den angivna filen verkar inte följa det förväntade formatet namn: [X, Y],vänligen kontrollera din fil och försök igen. Felet uppstod på rad {i}.")
                    except ValueError:
                        raise ValueError(f"Den angivna filen verkar inte innehålla data i det forväntade formatet namn: [X, Y], vänligen kontrollera din fil och försök igen. Felet uppstod på rad {i}.")
                    else:
                        return True
    
def validera_sokvag(sokvag=None):
    # En stödfunktion som testar att filen finns och att det är korrekt format.
    # In = sokvägen ifråga utfärderas som None ifall ingen sökväg angivits.
    # Finns inte filen returneras eller om den inte är .json höjs ett exception.
    # Finns filen och är en .json returneras True
    if sokvag is None:
        print("Det finns ingen sökväg angiven")
        return None
    else:
        print(f"Kontrollerar sökvägen: {sokvag}")
    try:
        with open(str(sokvag)) as f:
            print("Hittade en fil på den angivna platsen.")
            #time.sleep(1)
    except FileNotFoundError:
        print("Det finns ingen sådan fil, vänligen kontrollera din sökväg och ditt filnamn.")
        raise FileNotFoundError
    else: 
        if str(Path(sokvag).suffix) != ".json":
            print("Det verkar inte som att du har pekat på en .json-fil, vänligen kontrollera vad du skrev och försök igen.")
            raise ValueError
        else: 
            return True
        






if __name__ == "__main__":
    # Magin som får filen att köras när man kallar på den som människa.
    sokvag = get_path()
    misstankt, antal_misstankta, titlar, x_varden, y_varden, troskel = solution(sokvag)
    plot_map(misstankt, antal_misstankta, titlar, x_varden, y_varden, troskel) 



def test_solution(tmp_path):
    namn = solution("tracking.json")
    assert type(namn) == str, "solution() should return a string"
    with open("tracking.json") as fil:
        assert namn in json.load(fil), "The name should be one of the computers in the file"

    # Ett litet exempel med en egen testfil (tmp_path är en tillfällig mapp från pytest).
    fil = tmp_path / "exempel.json"
    fil.write_text(
        json.dumps(
            {
                "a": [59.3291, 18.0681],
                "b": [59.3293, 18.0687],
                "c": [57.7089, 11.9746],
            }
        )
    )
    assert solution(str(fil)) == "c"


def test_ingen_ensam(tmp_path):
    # Här står alla datorer på samma plats, så det finns ingen stulen dator att hitta.
    # Funktionen ska inte gissa. Det här testet godtar vilket undantag som helst:
    # i dina egna tester ska du vara mer exakt.
    fil = tmp_path / "ingen.json"
    fil.write_text(json.dumps({"a": [59.3291, 18.0681], "b": [59.3293, 18.0687]}))
    with pytest.raises(Exception):
        solution(str(fil))


# Egna tester: skriv minst tre här (se test_solution för hur man skriver en testfil).
# 3st egna tester i den här filen betyder 3st nya funktioner och inte enbart 3st extra assert rader


def test_flera_samma_avstand(tmp_path):
    # Här verifierar vi att den inte chansar om flera datorer är på samma avstånd.
    fil = tmp_path / "ingen.json"
    fil.write_text(json.dumps({"a": [59, 19], "b": [58, 18], "c":[59, 18], "d": [58, 19], "e": [58.5, 18.5], "f": [58.5, 18.5], "g": [58.5, 18.5], "h": [58.5, 18.5], "i": [58.5, 18.5]}))
    with pytest.raises(Exception):
        solution(str(fil))

def test_fel_format(tmp_path):
    # Här skickar vi in en fil som inte är en .json.fil för att se så att funktionen inte försöker läsa av den.
    fil = tmp_path / "ingen.txt"
    fil.write_text("")
    with pytest.raises(Exception):
        solution(str(fil))

def test_ingen_data(tmp_path):
    # Här testar vi att köra in en tom fil för att se så att den inte försöker dividera med 0 någonstans.
    fil = tmp_path / "ingen.json"
    fil.write_text(json.dumps({}))
    with pytest.raises(ValueError):
        solution(str(fil))

def test_fel_in_data(tmp_path):
    # Här verifierar vi att den inte chansar om flera datorer är på samma avstånd.
    fil = tmp_path / "ingen.json"
    fil.write_text(json.dumps({"a": [59, 57], "b": [58, "a"], "c":"b"}))
    with pytest.raises(Exception):
        solution(str(fil))





