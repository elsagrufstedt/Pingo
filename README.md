# Pingo
Detta är en Python-webbapplikation som använder ramverket Bottle

## Krav
* Python 3
* Bottle
* En webbläsare

## Installation
1. Klona repostorien eller ladda ner ZIP-filen från https://github.com/elsagrufstedt/Pingo
2. Öppna terminalen i er textredigerare/lokalt på er maskin
3. Installera Bottle och Beaker med följande kommando:
```
pip install bottle
pip install Beaker
```
4. Navigera till projektet och kör följande kommando:
```
python3 bottle_app.py
```
5. Öppna en webbläsare och gå till http://localhost:8080

## Användning
* Vid start av Webbserver blir användaren introducerad till två alternativ, Spela eller registrera konto
* Klicka på knappen Spela bingo för att gå till kategorisidan.
* På kategorisidan klickar du på en kategori för att spela ett bingospel.
* På sidan för bingospel visas ett bingokort med olika utmaningar som rör den valda kategorin.
* Klicka på varje utmaning för att markera den som slutförd.
* För att avsluta spelet stänger du helt enkelt webbläsaren eller använder tillbaka pilen.

## Filstruktur
* `bottle_app.py` - den huvudsakliga Pythonfilen som innehåller koden för Bottle-applikationen.
* `views/` - en mapp som innehåller HTML-mallar och statiska filer som används av programmet.
    * `index.html` - mallen för startsidan.
    * `login.html` - mallen för inloggningssidan.
    * `categories.html` - mallen för kategorisidan.
    * `bingo.html` - sidmall för bingospel.
    * `static/` - en mapp som innehåller de statiska filer som används av programmet.
        * `styles.css` - CSS-Stilarna som används av index.html.
        * `categories.css` - CSS-Stil för kategorisidan
        * `bingo.css` - CSS-Stil för bingospelet
        * `categories.json` - en JSON-fil som innehåller de kategorier och utmaningar som används av under bingospelet.
        * `arrow.svg` - SVG fil som liknar en pil
        
