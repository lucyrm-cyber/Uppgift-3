Antaganden som har gjorts: 

- Att personen som kör scriptet vet var på datorn .json-filen med datorernas kordinater befinner sig.
- Att datorn som är stulen är tillräckligt långt bort för att aggresivt vikta ett medelvärde så pass att det överstiger alla andra avstånd som beräkningar utförs på. Mer om detta i stycket under med mina reflektioner kring tröskelvärdet. 


Hur man kör programmet:

Programmet körs med fördel genom uv run solution.py. Till en början kommer den precis som i min inlämning på uppgift 2 att fråga om sökvägen för json-filen. Den validerar sen att det är en korrekt typ av fil med korrekt typ av data. Beräkningarna som sedan sker går ut på att räkna ut hur långt varje dator har till sin närmsta granne enligt koordinaterna vi har fått. Dessa avstånd mäts sedan mot ett tröskelvärde för att se om de är borta eller inte. När beräkningarna kommer den att dela med sig av sitt resultat och erbjuda att rita upp en scatterplot med alla datorer och tröskelvärdets area runt dem för att visualisera om det är andra datorer inom en dators närområde eller inte.


Tröskelvärdet: 

Jag har valt att sätta tröskelvärdet till ett medelvärde av avståndet till alla närmsta grannar. Detta då det gör scriptet dynamiskt, oavsett vilket json-fil vi petar in och hur stora avstånd vi har att göra med så kommer det att fungera utan att vi behöver justera vårt tröskelvärde. Valet att ta ett medelvärde bygger på att när alla datorer befinner sig väldigt nära varandra blir det svårt att avgöra om en dator är längre bort för att den är stulen eller om den bara har gått hem för dagen. Ju längre ifrån resten en dator befinner sig desto enklare blir det isåfall att avgöra om den är stulen eller inte. Jag har sedan valt att lägga in en multiplikativ faktor som man hellre bör justera om man vill göra tröskelvärdet aggresivare (faktor > 1) eller snällare (0 < faktor < 1). Är det så att json-filen man skickat in ger ett resultat som resulterar i 0 eller fler än 1 misstänkt dator skickas en uppmaning att man bör justera tröskelfaktorn som är definerad i solution()-funktionen. 

Hade jag inte valt ett dynamiskt tröskelvärde hade jag antagligen lutat mot att räkna ut alla avstånd och sedan titta på den dator som är näst längst bort om det är exakt en dator som kan anses vara lägnst ifrån sin närmsta granne och då sätta det näst längsta avståndet som tröskelvärdet. Dock faller båda dessa på antagandet att det bara borde vara en dator som är så pass långt bort.

Alternativ tre är att vi först räknar ut hur långt bort alla andra är och sätter ett värde manuellt utifrån det, men då går det inte dynamiskt att byta fil på samma sätt ifall man måste först köra det och sedan 

Alternativ fyra är att man bara chansar och slänger in en siffra, typ 1, eller i det här fallet hade vi antagligen behövt 0.1, men det förutsätter också att vi räknar på det innan eller nöjer oss med att inte hitta några svar. 

Resultat:

Efter körning av filen var resultatet att datorn "makar" var stulen.
