# Uppgift 3

## Bakgrund

Hackarna har avslöjat att de inte bara lyckats komma åt
företagets hemsida, de har dessutom tagit sig in och stulit
en dator med alla kontouppgifter.

Vad de förhoppningsvis inte vet är att IT-säkerhetsavdelningen
gömt spårsändare i alla företagets datorer. Datorerna skickar
regelbundet ut sin position som latitud och longitud, och detta
sparas i en fil som heter `tracking.json`.

Filen är en JSON-ordbok: nyckeln är datorns namn och värdet är
en lista `[latitud, longitud]`. Så här ser början ut:

    {"link": [57.7092, 11.9742], "zelda": [59.3291, 18.0681], "ganon": [59.3292, 18.0689]}

## Uppgift

Din uppgift är att skriva en funktion som läser `tracking.json`
och hittar den stulna datorn.

Med lite tur befinner sig den stulna datorn inte i närheten av
någon annan av företagets datorer.

Hitta vilken av datorerna som befinner sig ensam på en plats.

Skapa en funktion `solution(path)` som läser filen på sökvägen `path` och
returnerar **namnet** på den dator som är ensam. Du kan anta att filen har
formatet som beskrivs ovan.

Krav på lösningen:

- Funktionen ska ta filens sökväg som parameter och använda den. Funktionen ska
  använda en `with`-sats.
- Skriv en **hjälpfunktion** som tar två positioner och svarar på om datorerna
  ligger så nära varandra att de räknas som på samma plats. `solution` ska
  använda den.
- Tröskelvärdet för "nära" ska stå på ett enda ställe i koden: som en namngiven
  konstant eller som en parameter med defaultvärde. Skriv en kommentar som
  förklarar varför du valde just det värdet. Inga siffror gömda mitt i en
  jämförelse. Tänk på vad "stulen" betyder i sammanhanget.
- Funktionen får inte gissa. Om ingen dator är ensam, eller om flera är det, ska
  den **kasta ett undantag** (`raise ValueError(...)` är lämpligt) med ett
  meddelande som förklarar vad som hänt. Den ska inte returnera en tom sträng
  eller `None`.
- Båda funktionerna ska ha en egen docstring. Docstringen till `solution` ska
  beskriva vad den läser, vad den returnerar, vilka antaganden den gör, och
  vilket undantag den kastar och när. Docstringarna granskas.
- Du ska skriva minst tre egna tester längst ner i `solution.py`. Tillsammans ska
  de testa hjälpfunktionen direkt, var gränsen går (två datorer som är närmare
  varandra än din tröskel, och två som är längre bort), och felfallet med den
  undantagstyp du valt. Tänk på vad som kan gå fel i jämförelsen.
- De färdiga testerna i `solution.py` är medvetet vaga. Att de blir gröna
  betyder inte att lösningen är klar.

Inlämningen ska bestå både av namnet på den stulna datorn och
programmet som löser uppgiften!

Skriv följande i en kort `README.md` i den här mappen, tillsammans med hur man
kör programmet och antaganden du gjort. Se `../instruktioner.md`.

1. Namnet på den stulna datorn.
2. Datorns latitud och longitud, och vilken stad den befinner sig i (slå upp
   koordinaterna på en karta).
3. En kort analys av tröskelvärdet: hur stor är din tröskel i kilometer (en
   breddgrad är ungefär 111 km)? Ändra tröskeln tillfälligt till 0.0001 och till
   1 och kör programmet. Vad händer med svaret, och varför?

<!-- Krav DELTA-3 (kodgranskning): Konstanten som håller tröskelvärdet ska heta `LAVSKRIKA`,
och meddelandet i varje `ValueError` ska avslutas med texten " (ärende RANSOM-3F)". -->

## Tips

Datorernas positioner lagras som en lista `[latitud, longitud]`. När Python läser
JSON blir det en vanlig lista (inte en tuple), men du kommer åt värdena på samma
sätt: `latitud, longitud = position`.

Positionerna för datorer på samma plats är nära varandra, men inte
exakt lika.

Jämför alla datorers positioner med varandra. Om två datorer är
på ungefär samma plats så är de inte stulna. Markera dem i t.ex.
en dict.

Den dator som inte är markerad är svaret på uppgiften.

För att jämföra två flyttal med varandra kan man göra så här:

Räkna ut `abs(A - B)` och jämför resultatet med ett litet värde,
tex 0.05. Om resultatet av uträkningen är nära 0 kan talen anses
vara lika. `abs()` är en inbyggd funktion i Python som ger
absolutvärdet för ett tal: `abs(1)` är 1, `abs(-1)` är också 1.

Några frågor att ta med in i testerna: spelar det roll vilken av två positioner som
står först i jämförelsen? Räcker det att latituden är nära för att två datorer ska
räknas som på samma plats?

Kör testerna med kommandot

    uv run pytest solution.py

- I testerna i `solution.py` skapas en liten JSON-fil med `tmp_path`. Det är en
  pytest-fixtur: lägg bara `tmp_path` som parameter på testfunktionen och använd
  `tmp_path / "test.json"` som filnamn. Se `test_solution`.

- Så här testar du att något kastar ett undantag:

      with pytest.raises(ValueError):
          solution(str(fil))

  Testet går bara igenom om `solution` kastar just `ValueError` där.

## Länkar

- https://docs.python.org/3/library/json.html#json.load

  Funktionen `json.load` läser JSON direkt från en öppen fil.

- https://docs.python.org/3/tutorial/floatingpoint.html

  Mer om flyttal i Python.

- https://docs.python.org/3/tutorial/errors.html#raising-exceptions

  Att kasta undantag med `raise`.

- https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions

  `pytest.raises`: testa att ett undantag kastas.
