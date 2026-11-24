# Web Restaurace Via Ferrata

Statický web ve třech jazycích (CS / EN / DE), navazuje na vizuál Penzionu Via Ferrata
(písma Merriweather + Catamaran, bílá / uhlová / šedá, akcent #da532c).

## Struktura a odkazy pro kampaně

| Stránka | CS | EN | DE |
|---|---|---|---|
| Úvod | `index.html` | `en/index.html` | `de/index.html` |
| Týdenní menu | `menu.html` | `en/menu.html` | `de/speisekarte.html` |
| Rezervace stolu | `rezervace.html` | `en/reservation.html` | `de/reservierung.html` |
| Pronájem prostor | `pronajem.html` | `en/private-hire.html` | `de/raumvermietung.html` |

Každá podstránka funguje samostatně, takže se dá použít jako cílová stránka placené reklamy.
Kotvy na úvodní stránce: `#menu`, `#o-nas`, `#pronajem`, `#recenze`, `#kontakt`.

## Úpravy

- **Texty, kontakty, otevírací doba:** `src/build.py` (slovník `SITE` a `T`), pak `python3 src/build.py` → složka `dist/`.
- **Týdenní menu každý týden:** nahraďte `dist/assets/tydenni-menu.png` novým PNG (stejný název; teď 1080 × 1350 – formát z `jidelni_listek`).
- **Fotky:** ve funkci `ph()` doplňte parametr `img="assets/foto/nazev.jpg"`, jinak se zobrazí zástupná plocha s popisem.

## Rezervační systém

Formulář (výběr dne, časů po 30 min podle otevírací doby, počtu hostů, místa, kontaktů, souhlasu GDPR) je hotový.
Teď běží v **ukázkovém režimu**, takže nic neodesílá. Napojení: v `src/build.py` vyplňte `RESERVATION["endpoint"]`.
Formulář na tuto adresu pošle JSON (date, time, guests, area, name, phone, email, note, lang). Možnosti napojení:
1. Formspree / Basin a podobné služby: rezervace chodí e-mailem, bez programování.
2. Make / Zapier + Google Sheets: e-mail restauraci, tabulka rezervací a automatické potvrzení hostovi.
3. Vlastní backend s administrací (kapacita stolů, potvrzování a rušení rezervací).

Pronájem celé restaurace: poptávkový formulář připraví e-mail. Kdyby se e-mail neotevřel, nabídne text ke zkopírování.

## Zástupné údaje k doplnění / ověření

- [ ] **Telefon:** web používá +420 793 325 970 z jídelního lístku, ale Google Maps uvádí +420 792 325 970 – sjednotit
- [ ] Otevírací doba (teď Po–Ne 11:30–22:00 – zástupná); denní nabídka Po–Pá 11:30–15:00, polévka 65 Kč, hlavní jídlo 179 Kč (z lístku)
- [ ] E-mail `restaurace@penzionferrata.cz` – ověřit nebo nahradit
- [ ] Odkazy na Facebook a Instagram (v patičce teď vedou na `#`)
- [x] Doména www.viaferratarestaurant.cz (z jídelního lístku)
- [ ] Stálý jídelní lístek: položky a ceny (teď ukázka)
- [ ] Pronájem: ceník a balíčky, kapacita terasy
- [x] Fotky z `klient_raw` (zmenšené ve `src/assets/foto/`, výběr v `PHOTOS` v build.py)
- [ ] Chybí fotka terasy s výhledem na ferratu – u bloku „Terasa pod skalou“ je zatím Aperol spritz
- [x] Logo z `FILES_IN` (karabina): hlavička, patička, favicon
- [ ] Mapa v kontaktu je zatím jen odkaz na Google Maps
- [ ] Recenze: Vojtěch K. a Conrad H. jsou z Googlu. Česká verze recenze Jardy L. je zpětně přeložená z anglického překladu Googlu, nahraďte ji originálem.
- [ ] Hodnocení 4,5 / 37 recenzí na Google (stav k 24. 11. 2026) – průběžně aktualizovat
- [ ] Stránka Ochrana osobních údajů (odkaz v patičce)
