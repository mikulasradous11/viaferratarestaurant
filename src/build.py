#!/usr/bin/env python3
"""Generátor webu Restaurace Via Ferrata (CS / EN / DE).

Spuštění:  python3 build.py   →  vytvoří složku ../dist
Texty se mění ve slovníku T, kontakty a otevírací doba v SITE.
"""
import json, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT.parent / "dist"

# ------------------------------------------------------------------ data
SITE = {
    "name": "Restaurace Via Ferrata",
    "street": "Labské nábřeží 317/19",
    "city": "405 02 Děčín 2",
    "phone": "+420 793 325 970",                       # z jídelního lístku (Google uvádí 792 – sjednotit!)
    "phone_href": "+420793325970",
    "email": "restaurace@penzionferrata.cz",          # ZÁSTUPNÝ – ověřit
    "facebook": "#",                                    # ZÁSTUPNÝ – doplnit odkaz
    "instagram": "#",                                   # ZÁSTUPNÝ – doplnit odkaz
    "penzion": "https://www.penzionferrata.cz/",
    "maps": "https://www.google.com/maps/place/Restaurace+Via+Ferrata/@50.7789691,14.2047512,17z/data=!3m1!4b1!4m6!3m5!1s0x47099f0138e5aefb:0x6d8750c28675e295!8m2!3d50.7789691!4d14.2047512!16s%2Fg%2F11z9j22n8m",
    "directions": "https://www.google.com/maps/dir/?api=1&destination=50.7789691,14.2047512",
    "geo": [50.7789691, 14.2047512],
    "rating": "4,5", "rating_en": "4.5", "reviews_count": 37,
    # Otevírací doba: pondělí … neděle, None = zavřeno.  ZÁSTUPNÉ – ověřit
    "hours": [["11:30", "22:00"]] * 7,
    "lunch": "11:30–15:00",                             # dle jídelního lístku
    "base_url": "https://www.viaferratarestaurant.cz/", # dle jídelního lístku
}
RESERVATION = {
    # Sem patří adresa backendu (např. Formspree, Make, vlastní API).
    # Prázdné = ukázkový režim: formulář se jen potvrdí, nic se neodešle.
    "endpoint": "",
    "step": 30,             # interval časů v minutách
    "lastBeforeClose": 90,  # poslední rezervace X minut před zavírací dobou
    "leadMinutes": 60,      # dnes nejdřív za X minut
    "daysAhead": 60,        # rezervace nejvýše X dní dopředu
    "maxGuests": 8,         # větší skupiny → telefon / pronájem
}

LANGS = ["cs", "en", "de"]
PAGES = {  # klíč → název souboru v daném jazyce
    "home":   {"cs": "index.html",     "en": "index.html",       "de": "index.html"},
    "menu":   {"cs": "menu.html",      "en": "menu.html",        "de": "speisekarte.html"},
    "reserve":{"cs": "rezervace.html", "en": "reservation.html", "de": "reservierung.html"},
    "rental": {"cs": "pronajem.html",  "en": "private-hire.html","de": "raumvermietung.html"},
}
def prefix(lang): return "" if lang == "cs" else lang + "/"

# ------------------------------------------------------------------ texty
T = {
"cs": {
  "theme_toggle": "Přepnout světlý / tmavý režim",
  "locale": "cs-CZ", "sub": "restaurace",
  "nav": {"menu": "Týdenní menu", "about": "O nás", "rental": "Pronájem prostor", "reviews": "Recenze", "contact": "Kontakt"},
  "cta": "Rezervovat stůl", "skip": "Přeskočit na obsah", "menu_toggle": "Otevřít menu",
  "days": ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"],
  "closed": "Zavřeno",
  "home_title": "Restaurace Via Ferrata Děčín – poctivé jídlo s výhledem",
  "home_desc": "Restaurace Via Ferrata na Labském nábřeží v Děčíně. Výborné a poctivé jídlo, týdenní menu, terasa s výhledem na ferratu a zámek. Rezervujte stůl online.",
  "hero_h": "Gastronomický zážitek s výhledem na děčínský zámek",
  "hero_p": "Restaurace v přízemí Penzionu Via Ferrata na Labském nábřeží. Vaříme výborně, ale především opravdu poctivě.",
  "hero_ph": "Foto: terasa nebo signature jídlo",
  "see_menu": "Týdenní menu",
  "f_hours": "Dnes otevřeno", "f_where": "Kde nás najdete", "f_call": "Rezervace telefonem", "f_menu": "Tento týden",
  "f_menu_txt": "Nové menu každý týden", "f_nav": "Navigovat", "f_all_hours": "Celá otevírací doba", "f_show": "Zobrazit menu",
  "menu_label": "Týdenní menu", "menu_h": "Každý týden nová nabídka",
  "menu_p": "Polední menu měníme každý týden podle sezóny a toho, co se zrovna dá dobře nakoupit. Aktuální nabídka je vždy tady.",
  "menu_lunch": "Polední menu", "menu_weekdays": "Po–Pá", "menu_price": "Cena za osobu", "menu_price_v": "300–400 Kč",
  "menu_zoom": "Zvětšit menu", "menu_alt": "Týdenní menu Restaurace Via Ferrata",
  "menu_full": "Celé menu a stálý lístek", "close": "Zavřít",
  "about_label": "O nás", "about_h": "Výborné, ale hlavně poctivé jídlo",
  "about_p1": "Jsme rodinná restaurace a sesterský podnik Penzionu Via Ferrata. Vaříme tak, jak bychom chtěli jíst sami: pořádné porce, chuť, na které se dá spolehnout, a žádné zkratky.",
  "about_p2": "Přijďte na polední menu, na večeři s přáteli nebo jen na kávu na terase. Nad hlavou vám šplhají lezci na ferratě a přes Labe se díváte na děčínský zámek.",
  "about_ph": "Foto: kuchař při práci / talíř zblízka",
  "feats": [
    ["Terasa pod skalou", "Z terasy sledujete lezce na via ferratě přímo nad sebou. V létě nejlepší místo v Děčíně.", "Foto: terasa s výhledem na ferratu"],
    ["Výhled na zámek", "Uvnitř i venku máte před sebou Labe a děčínský zámek. Klidné místo, kde se dobře povídá.", "Foto: interiér s výhledem"],
    ["Snídaně pro hosty penzionu", "Hostům Penzionu Via Ferrata podáváme každý den snídani od 8:00 do 10:00.", "Foto: snídaně"],
  ],
  "gallery": ["Foto: pečená kachna", "Foto: kulajda", "Foto: burger", "Foto: interiér restaurace", "Foto: terasa večer"],
  "rental_label": "Pronájem prostor", "rental_h": "Celá restaurace jen pro vaši oslavu",
  "rental_p": "Narozeniny, firemní večírek nebo rodinné setkání. Pronajměte si celé prostory i s terasou a o jídlo i pití se postaráme my.",
  "rental_cap": "hostů uvnitř", "rental_cap_t": "plus terasa",
  "rental_list": ["Narozeniny a výročí", "Firemní akce", "Rodinné oslavy", "Křtiny a svatební hostiny"],
  "rental_more": "Pronájem a ceny", "rental_ph": "Foto: slavnostně prostřený sál",
  "reviews_label": "Recenze", "reviews_h": "Co říkají naši hosté",
  "reviews_count": "{n} recenzí na Google", "reviews_all": "Všechny recenze na Google",
  "reviews": [
    ["Velmi jsem si užil pečenou kachnu, moc dobré. Všem doporučuji, skvělé místo, kde se o své hosty výtečně postarají.", "Vojtěch K.", "Google, před měsícem"],
    ["Úžasný výhled, kvůli kterému stojí za to posedět. Ceny jsou vzhledem k místu rozumné, jídlo výborné. Kulajda, těstoviny i burger. Káva jako v Itálii.", "Jarda L.", "Google, před 3 měsíci"],
    ["Zastavili jsme se tu spontánně a moc se nám tu líbilo. Jídlo bylo výborné a servírka velmi milá a ochotná. Doporučujeme.", "Conrad H.", "Google, před 4 měsíci · přeloženo"],
  ],
  "contact_label": "Kontakt", "contact_h": "Těšíme se na Vás",
  "c_addr": "Adresa", "c_phone": "Telefon", "c_email": "E-mail", "c_parking": "Parkování",
  "c_parking_v": "Bezplatné parkování na ulici",
  "hours_h": "Otevírací doba", "hours_note": "Snídaně jen pro hosty penzionu, denně 8:00–10:00.",
  "map_ph": "Mapa – Restaurace Via Ferrata, Labské nábřeží 317/19, Děčín",
  "f_about": "Rodinná restaurace v přízemí Penzionu Via Ferrata v Děčíně. Výborné a poctivé jídlo s výhledem na ferratu a zámek.",
  "f_visit": "Navštivte", "f_follow": "Sledujte nás", "f_penzion": "Penzion Via Ferrata", "f_privacy": "Ochrana osobních údajů",
  "rights": "Všechna práva vyhrazena.",
  # menu stránka
  "menu_title": "Týdenní menu – Restaurace Via Ferrata Děčín",
  "menu_desc": "Aktuální týdenní polední menu Restaurace Via Ferrata v Děčíně. Poctivá kuchyně, nové menu každý týden.",
  "menu_sub_h": "Týdenní menu", "menu_sub_p": "Nové polední menu každý týden. Stálý lístek najdete níže.",
  "carte_h": "Stálý lístek", "carte_note": "Ukázka struktury lístku, položky a ceny doplníme.",
  "carte": [
    ["Polévky", [["Kulajda", "s vejcem a koprem", "— Kč"], ["Hovězí vývar", "s nudlemi a zeleninou", "— Kč"]]],
    ["Hlavní jídla", [["Pečená kachna", "červené zelí, knedlíky", "— Kč"], ["Burger Via Ferrata", "hovězí, slanina, cheddar, hranolky", "— Kč"], ["Těstoviny dle sezóny", "", "— Kč"], ["Smažený sýr", "hranolky, tatarská omáčka", "— Kč"]]],
    ["Dezerty a káva", [["Domácí dezert dne", "", "— Kč"], ["Espresso", "", "— Kč"]]],
  ],
  "menu_cta_h": "Chcete mít jistotu volného stolu?", "menu_cta_p": "Zarezervujte si stůl online během minuty.",
  # rezervace
  "res_title": "Rezervace stolu – Restaurace Via Ferrata Děčín",
  "res_desc": "Rezervujte si stůl v Restauraci Via Ferrata v Děčíně online. Vyberte den, čas a počet hostů.",
  "res_h": "Rezervace stolu", "res_p": "Vyberte den, čas a počet hostů. Rezervaci vám potvrdíme e-mailem.",
  "r_date": "Datum", "r_time": "Čas", "r_guests": "Počet hostů", "r_area": "Kde chcete sedět", "r_opt": "(nepovinné)",
  "r_big": "9 a více", "r_big_msg": "Pro skupiny od 9 osob nám prosím zavolejte na {phone}, nebo si prohlédněte pronájem celé restaurace.",
  "r_name": "Jméno a příjmení", "r_phone": "Telefon", "r_email": "E-mail", "r_note": "Poznámka", "r_note_ph": "Oslava, dětská židlička, alergie…",
  "r_gdpr": "Souhlasím se zpracováním osobních údajů pro účely rezervace.",
  "r_submit": "Odeslat rezervaci", "r_done_h": "Děkujeme, rezervaci jsme přijali",
  "r_done_p": "Potvrzení vám pošleme e-mailem. Pokud se cokoli změní, zavolejte nám prosím.",
  "r_demo": "Ukázkový režim: rezervační formulář zatím není napojený na systém, rezervace se nikam neodeslala.",
  "r_again": "Nová rezervace",
  "aside_h": "Dobré vědět", "aside_list": ["Stůl vám podržíme 15 minut.", "Pro 9 a více hostů volejte.", "Snídaně jsou jen pro hosty penzionu."],
  "aside_rental": "Plánujete větší oslavu?", "aside_rental_a": "Pronájem celé restaurace",
  "areas": {"inside": "Uvnitř", "terrace": "Terasa"}, "nopref": "Je mi to jedno",
  # pronájem
  "rent_title": "Pronájem restaurace pro oslavy a firemní akce – Via Ferrata Děčín",
  "rent_desc": "Pronájem celé Restaurace Via Ferrata v Děčíně až pro 40 hostů i s terasou. Oslavy, firemní akce, rodinná setkání. Menu na míru.",
  "rent_h": "Pronájem celé restaurace", "rent_p": "Prostor až pro 40 hostů uvnitř a terasa s výhledem na ferratu. Postaráme se o jídlo, pití i obsluhu, vy se věnujte hostům.",
  "rent_for_h": "Pro jaké akce", "rent_for": ["Narozeninové oslavy a výročí", "Firemní večírky a setkání", "Rodinné oslavy a křtiny", "Menší svatební hostiny", "Smuteční hostiny", "Akce pro skupiny lezců a turistů"],
  "rent_inc_h": "Co zajistíme", "rent_inc": ["Menu na míru: raut, servírované menu nebo grill", "Nápoje a obsluhu po celou dobu akce", "Prostor uspořádaný podle vašich představ", "Terasu podle počasí a domluvy"],
  "rent_inc_note": "Ceník a konkrétní balíčky doplníme.",
  "steps_h": "Jak to funguje", "steps": [["Ozvěte se nám", "Zavolejte nebo napište termín, počet hostů a typ akce."], ["Domluvíme detaily", "Navrhneme menu a uspořádání prostoru přesně pro vás."], ["Potvrdíme termín", "Po odsouhlasení vám termín závazně zarezervujeme."]],
  "q_h": "Nezávazná poptávka", "q_p": "Vyplňte pár údajů a připravíme vám e-mail k odeslání. Nebo rovnou zavolejte.",
  "q_type": "Typ akce", "q_types": ["Narozeniny / výročí", "Firemní akce", "Rodinná oslava", "Svatební hostina", "Jiné"],
  "q_date": "Předpokládaný termín", "q_guests": "Počet hostů", "q_name": "Jméno", "q_contact": "Telefon nebo e-mail",
  "q_note": "Co plánujete", "q_submit": "Připravit e-mail s poptávkou",
  "q_fallback": "Pokud se e-mail neotevřel, zkopírujte text a pošlete ho na {email}.", "q_copy": "Zkopírovat text",
  "rent_ph": "Foto: celá restaurace připravená na oslavu",
  "js": {
    "openNow": "Otevřeno, dnes do {t}", "opensAt": "Dnes otevíráme v {t}", "closedNext": "Zavřeno, otevíráme {d} v {t}", "closed": "Zavřeno",
    "noSlots": "V tento den už nemáme volné časy. Zkuste prosím jiný den.",
    "errDate": "Vyberte prosím datum.", "errTime": "Vyberte prosím čas.", "errGuests": "Vyberte počet hostů.",
    "errBig": "Pro 9 a více hostů nám prosím zavolejte.", "errName": "Vyplňte prosím jméno.",
    "errPhone": "Zadejte prosím platné telefonní číslo.", "errEmail": "Zadejte prosím platný e-mail.",
    "errGdpr": "Bez souhlasu nemůžeme rezervaci přijmout.", "errRequired": "Vyplňte prosím.",
    "errSend": "Rezervaci se nepodařilo odeslat. Zkuste to prosím znovu, nebo nám zavolejte.",
    "sending": "Odesílám…", "submit": "Odeslat rezervaci",
    "fDate": "Datum", "fTime": "Čas", "fGuests": "Počet hostů", "fArea": "Místo", "fName": "Jméno", "fContact": "Kontakt",
    "noPref": "Bez preference",
    "qHello": "Dobrý den, mám zájem o pronájem restaurace.", "qType": "Typ akce", "qNote": "Poznámka", "qSubject": "Poptávka pronájmu",
    "copied": "Zkopírováno",
  },
},
"en": {
  "theme_toggle": "Toggle light / dark mode",
  "locale": "en-GB", "sub": "restaurant",
  "nav": {"menu": "Weekly menu", "about": "About", "rental": "Private hire", "reviews": "Reviews", "contact": "Contact"},
  "cta": "Book a table", "skip": "Skip to content", "menu_toggle": "Open menu",
  "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
  "closed": "Closed",
  "home_title": "Restaurant Via Ferrata Děčín – honest food with a view",
  "home_desc": "Restaurant Via Ferrata on the Elbe embankment in Děčín. Great, honest cooking, a weekly menu and a terrace overlooking the via ferrata and the castle. Book a table online.",
  "hero_h": "A culinary experience with a view of Děčín Castle",
  "hero_p": "A restaurant on the ground floor of Penzion Via Ferrata on the Elbe embankment. We cook great food and, above all, honest food.",
  "hero_ph": "Photo: terrace or signature dish",
  "see_menu": "Weekly menu",
  "f_hours": "Open today", "f_where": "Find us", "f_call": "Book by phone", "f_menu": "This week",
  "f_menu_txt": "A new menu every week", "f_nav": "Directions", "f_all_hours": "All opening hours", "f_show": "See the menu",
  "menu_label": "Weekly menu", "menu_h": "A new menu every week",
  "menu_p": "Our lunch menu changes every week with the season and the best produce we can get. The current menu is always here. (The menu is in Czech; our staff will gladly translate.)",
  "menu_lunch": "Lunch menu", "menu_weekdays": "Mon–Fri", "menu_price": "Price per person", "menu_price_v": "CZK 300–400",
  "menu_zoom": "Enlarge menu", "menu_alt": "Weekly menu of Restaurant Via Ferrata",
  "menu_full": "Full menu", "close": "Close",
  "about_label": "About us", "about_h": "Great food, and above all honest food",
  "about_p1": "We are a family restaurant and the sister business of Penzion Via Ferrata. We cook the way we like to eat: proper portions, flavour you can rely on and no shortcuts.",
  "about_p2": "Drop in for the lunch menu, dinner with friends or just a coffee on the terrace. Climbers make their way up the via ferrata above you, and across the Elbe you look straight at Děčín Castle.",
  "about_ph": "Photo: chef at work / plate close-up",
  "feats": [
    ["A terrace below the rock", "From the terrace you can watch climbers on the via ferrata right above you. In summer, the best seat in Děčín.", "Photo: terrace with via ferrata view"],
    ["Castle views", "Inside and out, the Elbe and Děčín Castle are right in front of you. A calm place for a good conversation.", "Photo: interior with a view"],
    ["Breakfast for guesthouse guests", "Guests of Penzion Via Ferrata get breakfast every day from 8:00 to 10:00.", "Photo: breakfast"],
  ],
  "gallery": ["Photo: roast duck", "Photo: kulajda soup", "Photo: burger", "Photo: restaurant interior", "Photo: terrace at night"],
  "rental_label": "Private hire", "rental_h": "The whole restaurant, just for your party",
  "rental_p": "Birthdays, company parties or family get-togethers. Hire the whole place, terrace included, and leave the food and drinks to us.",
  "rental_cap": "guests inside", "rental_cap_t": "plus the terrace",
  "rental_list": ["Birthdays and anniversaries", "Company events", "Family celebrations", "Christenings and weddings"],
  "rental_more": "Private hire details", "rental_ph": "Photo: room set for a celebration",
  "reviews_label": "Reviews", "reviews_h": "What our guests say",
  "reviews_count": "{n} reviews on Google", "reviews_all": "All reviews on Google",
  "reviews": [
    ["I really enjoyed the roast duck, it was excellent. I recommend it to everyone, a great place where they take excellent care of their guests.", "Vojtěch K.", "Google, a month ago · translated"],
    ["An amazing view that is worth sitting down for. Prices are reasonable for the location, and the food is excellent. Kulajda, pasta and burger. Coffee like in Italy.", "Jarda L.", "Google, 3 months ago · translated"],
    ["We came here spontaneously and found it to be very nice. The food was delicious and our waitress was very friendly and helpful. We would recommend.", "Conrad H.", "Google, 4 months ago"],
  ],
  "contact_label": "Contact", "contact_h": "We look forward to seeing you",
  "c_addr": "Address", "c_phone": "Phone", "c_email": "Email", "c_parking": "Parking",
  "c_parking_v": "Free street parking",
  "hours_h": "Opening hours", "hours_note": "Breakfast is for guesthouse guests only, daily 8:00–10:00.",
  "map_ph": "Map – Restaurant Via Ferrata, Labské nábřeží 317/19, Děčín",
  "f_about": "A family restaurant on the ground floor of Penzion Via Ferrata in Děčín. Great, honest food with a view of the via ferrata and the castle.",
  "f_visit": "Visit", "f_follow": "Follow us", "f_penzion": "Penzion Via Ferrata", "f_privacy": "Privacy policy",
  "rights": "All rights reserved.",
  "menu_title": "Weekly menu – Restaurant Via Ferrata Děčín",
  "menu_desc": "This week's lunch menu at Restaurant Via Ferrata in Děčín. Honest cooking, new menu every week.",
  "menu_sub_h": "Weekly menu", "menu_sub_p": "A new lunch menu every week. The regular menu is below.",
  "carte_h": "Regular menu", "carte_note": "Sample layout; dishes and prices will be added.",
  "carte": [
    ["Soups", [["Kulajda", "creamy dill and mushroom soup with egg", "— CZK"], ["Beef broth", "with noodles and vegetables", "— CZK"]]],
    ["Mains", [["Roast duck", "red cabbage, dumplings", "— CZK"], ["Via Ferrata burger", "beef, bacon, cheddar, fries", "— CZK"], ["Seasonal pasta", "", "— CZK"], ["Fried cheese", "fries, tartar sauce", "— CZK"]]],
    ["Desserts and coffee", [["Homemade dessert of the day", "", "— CZK"], ["Espresso", "", "— CZK"]]],
  ],
  "menu_cta_h": "Want to be sure of a table?", "menu_cta_p": "Book online in under a minute.",
  "res_title": "Book a table – Restaurant Via Ferrata Děčín",
  "res_desc": "Book a table at Restaurant Via Ferrata in Děčín online. Choose the day, time and number of guests.",
  "res_h": "Book a table", "res_p": "Choose the day, time and number of guests. We will confirm your booking by email.",
  "r_date": "Date", "r_time": "Time", "r_guests": "Guests", "r_area": "Where would you like to sit", "r_opt": "(optional)",
  "r_big": "9 or more", "r_big_msg": "For groups of 9 or more, please call us on {phone} or have a look at hiring the whole restaurant.",
  "r_name": "Full name", "r_phone": "Phone", "r_email": "Email", "r_note": "Note", "r_note_ph": "Celebration, high chair, allergies…",
  "r_gdpr": "I agree to the processing of my personal data for the purpose of this booking.",
  "r_submit": "Send booking", "r_done_h": "Thank you, we have received your booking",
  "r_done_p": "We will send you a confirmation by email. If anything changes, please give us a call.",
  "r_demo": "Demo mode: the booking form is not yet connected to a system, so nothing has been sent.",
  "r_again": "New booking",
  "aside_h": "Good to know", "aside_list": ["We hold your table for 15 minutes.", "For 9 or more guests, please call.", "Breakfast is for guesthouse guests only."],
  "aside_rental": "Planning a bigger party?", "aside_rental_a": "Hire the whole restaurant",
  "areas": {"inside": "Inside", "terrace": "Terrace"}, "nopref": "No preference",
  "rent_title": "Private hire for parties and company events – Via Ferrata Děčín",
  "rent_desc": "Hire the whole Restaurant Via Ferrata in Děčín for up to 40 guests, terrace included. Parties, company events, family gatherings. Tailored menus.",
  "rent_h": "Hire the whole restaurant", "rent_p": "Room for up to 40 guests inside, plus a terrace with a view of the via ferrata. We take care of the food, drinks and service so you can focus on your guests.",
  "rent_for_h": "Perfect for", "rent_for": ["Birthdays and anniversaries", "Company parties and meetings", "Family celebrations and christenings", "Small wedding receptions", "Funeral receptions", "Groups of climbers and hikers"],
  "rent_inc_h": "What we take care of", "rent_inc": ["A tailored menu: buffet, served menu or grill", "Drinks and service throughout the event", "The room arranged the way you want it", "The terrace, weather permitting"],
  "rent_inc_note": "Prices and packages will be added.",
  "steps_h": "How it works", "steps": [["Get in touch", "Call or write with the date, number of guests and type of event."], ["We agree the details", "We suggest a menu and room layout made for you."], ["We confirm the date", "Once everything is agreed, the date is yours."]],
  "q_h": "Send an enquiry", "q_p": "Fill in a few details and we will prepare an email for you to send. Or just give us a call.",
  "q_type": "Type of event", "q_types": ["Birthday / anniversary", "Company event", "Family celebration", "Wedding reception", "Other"],
  "q_date": "Preferred date", "q_guests": "Number of guests", "q_name": "Name", "q_contact": "Phone or email",
  "q_note": "What are you planning", "q_submit": "Prepare enquiry email",
  "q_fallback": "If no email window opened, copy the text and send it to {email}.", "q_copy": "Copy text",
  "rent_ph": "Photo: the whole restaurant ready for a party",
  "js": {
    "openNow": "Open, today until {t}", "opensAt": "Opening today at {t}", "closedNext": "Closed, opening {d} at {t}", "closed": "Closed",
    "noSlots": "No times are left on this day. Please try another day.",
    "errDate": "Please choose a date.", "errTime": "Please choose a time.", "errGuests": "Please choose the number of guests.",
    "errBig": "For 9 or more guests, please call us.", "errName": "Please enter your name.",
    "errPhone": "Please enter a valid phone number.", "errEmail": "Please enter a valid email.",
    "errGdpr": "We cannot accept the booking without your consent.", "errRequired": "Please fill this in.",
    "errSend": "The booking could not be sent. Please try again or call us.",
    "sending": "Sending…", "submit": "Send booking",
    "fDate": "Date", "fTime": "Time", "fGuests": "Guests", "fArea": "Seating", "fName": "Name", "fContact": "Contact",
    "noPref": "No preference",
    "qHello": "Hello, I am interested in hiring the restaurant.", "qType": "Type of event", "qNote": "Note", "qSubject": "Private hire enquiry",
    "copied": "Copied",
  },
},
"de": {
  "theme_toggle": "Hell- / Dunkelmodus umschalten",
  "locale": "de-DE", "sub": "restaurant",
  "nav": {"menu": "Wochenmenü", "about": "Über uns", "rental": "Raumvermietung", "reviews": "Bewertungen", "contact": "Kontakt"},
  "cta": "Tisch reservieren", "skip": "Zum Inhalt springen", "menu_toggle": "Menü öffnen",
  "days": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
  "closed": "Geschlossen",
  "home_title": "Restaurant Via Ferrata Děčín – ehrliche Küche mit Aussicht",
  "home_desc": "Restaurant Via Ferrata am Elbufer in Děčín (Tetschen). Hervorragende, ehrliche Küche, Wochenmenü und Terrasse mit Blick auf den Klettersteig und das Schloss. Tisch online reservieren.",
  "hero_h": "Kulinarisches Erlebnis mit Blick auf das Schloss Děčín",
  "hero_p": "Das Restaurant im Erdgeschoss der Pension Via Ferrata am Elbufer. Wir kochen hervorragend und vor allem ehrlich.",
  "hero_ph": "Foto: Terrasse oder Signature-Gericht",
  "see_menu": "Wochenmenü",
  "f_hours": "Heute geöffnet", "f_where": "So finden Sie uns", "f_call": "Telefonisch reservieren", "f_menu": "Diese Woche",
  "f_menu_txt": "Jede Woche ein neues Menü", "f_nav": "Route planen", "f_all_hours": "Alle Öffnungszeiten", "f_show": "Menü ansehen",
  "menu_label": "Wochenmenü", "menu_h": "Jede Woche ein neues Angebot",
  "menu_p": "Unser Mittagsmenü wechselt jede Woche, je nach Saison und den besten Zutaten. Das aktuelle Angebot finden Sie immer hier. (Das Menü ist auf Tschechisch, unser Team übersetzt gern.)",
  "menu_lunch": "Mittagsmenü", "menu_weekdays": "Mo–Fr", "menu_price": "Preis pro Person", "menu_price_v": "300–400 CZK",
  "menu_zoom": "Menü vergrößern", "menu_alt": "Wochenmenü des Restaurants Via Ferrata",
  "menu_full": "Komplette Speisekarte", "close": "Schließen",
  "about_label": "Über uns", "about_h": "Hervorragend und vor allem ehrlich gekocht",
  "about_p1": "Wir sind ein Familienrestaurant und das Schwesterunternehmen der Pension Via Ferrata. Wir kochen so, wie wir selbst gern essen: ordentliche Portionen, verlässlicher Geschmack und keine Abkürzungen.",
  "about_p2": "Kommen Sie zum Mittagsmenü, zum Abendessen mit Freunden oder auf einen Kaffee auf der Terrasse. Über Ihnen klettern Kletterer am Klettersteig, und über die Elbe blicken Sie auf das Schloss Děčín.",
  "about_ph": "Foto: Koch bei der Arbeit / Teller in Nahaufnahme",
  "feats": [
    ["Terrasse unter dem Felsen", "Von der Terrasse aus sehen Sie die Kletterer am Klettersteig direkt über sich. Im Sommer der schönste Platz in Děčín.", "Foto: Terrasse mit Blick auf den Klettersteig"],
    ["Blick aufs Schloss", "Drinnen wie draußen haben Sie die Elbe und das Schloss Děčín vor sich. Ein ruhiger Ort für gute Gespräche.", "Foto: Innenraum mit Aussicht"],
    ["Frühstück für Pensionsgäste", "Gäste der Pension Via Ferrata frühstücken bei uns täglich von 8:00 bis 10:00 Uhr.", "Foto: Frühstück"],
  ],
  "gallery": ["Foto: gebratene Ente", "Foto: Kulajda-Suppe", "Foto: Burger", "Foto: Innenraum", "Foto: Terrasse am Abend"],
  "rental_label": "Raumvermietung", "rental_h": "Das ganze Restaurant nur für Ihre Feier",
  "rental_p": "Geburtstag, Firmenfeier oder Familientreffen. Mieten Sie die gesamten Räume samt Terrasse, um Essen und Getränke kümmern wir uns.",
  "rental_cap": "Gäste drinnen", "rental_cap_t": "plus Terrasse",
  "rental_list": ["Geburtstage und Jubiläen", "Firmenveranstaltungen", "Familienfeiern", "Taufen und Hochzeiten"],
  "rental_more": "Vermietung und Preise", "rental_ph": "Foto: festlich gedeckter Raum",
  "reviews_label": "Bewertungen", "reviews_h": "Was unsere Gäste sagen",
  "reviews_count": "{n} Bewertungen auf Google", "reviews_all": "Alle Bewertungen auf Google",
  "reviews": [
    ["Die gebratene Ente hat mir sehr geschmeckt, ausgezeichnet. Ich kann es allen empfehlen, ein toller Ort, an dem man sich hervorragend um die Gäste kümmert.", "Vojtěch K.", "Google, vor einem Monat · übersetzt"],
    ["Eine traumhafte Aussicht, für die es sich lohnt, hier zu sitzen. Die Preise sind für die Lage angemessen, das Essen ausgezeichnet. Kulajda, Pasta und Burger. Kaffee wie in Italien.", "Jarda L.", "Google, vor 3 Monaten · übersetzt"],
    ["Wir sind spontan hier eingekehrt und fanden es sehr schön. Das Essen war köstlich und unsere Kellnerin sehr freundlich und hilfsbereit. Wir empfehlen es weiter.", "Conrad H.", "Google, vor 4 Monaten · übersetzt"],
  ],
  "contact_label": "Kontakt", "contact_h": "Wir freuen uns auf Sie",
  "c_addr": "Adresse", "c_phone": "Telefon", "c_email": "E-Mail", "c_parking": "Parken",
  "c_parking_v": "Kostenlose Parkplätze an der Straße",
  "hours_h": "Öffnungszeiten", "hours_note": "Frühstück nur für Pensionsgäste, täglich 8:00–10:00 Uhr.",
  "map_ph": "Karte – Restaurant Via Ferrata, Labské nábřeží 317/19, Děčín",
  "f_about": "Familienrestaurant im Erdgeschoss der Pension Via Ferrata in Děčín. Hervorragende, ehrliche Küche mit Blick auf Klettersteig und Schloss.",
  "f_visit": "Besuchen", "f_follow": "Folgen Sie uns", "f_penzion": "Pension Via Ferrata", "f_privacy": "Datenschutz",
  "rights": "Alle Rechte vorbehalten.",
  "menu_title": "Wochenmenü – Restaurant Via Ferrata Děčín",
  "menu_desc": "Das aktuelle Mittagsmenü des Restaurants Via Ferrata in Děčín. Ehrliche Küche, jede Woche neu.",
  "menu_sub_h": "Wochenmenü", "menu_sub_p": "Jede Woche ein neues Mittagsmenü. Die feste Speisekarte finden Sie unten.",
  "carte_h": "Speisekarte", "carte_note": "Beispielhafter Aufbau, Gerichte und Preise folgen.",
  "carte": [
    ["Suppen", [["Kulajda", "Dill-Pilz-Rahmsuppe mit Ei", "— CZK"], ["Rinderbrühe", "mit Nudeln und Gemüse", "— CZK"]]],
    ["Hauptgerichte", [["Gebratene Ente", "Rotkraut, Knödel", "— CZK"], ["Via Ferrata Burger", "Rind, Speck, Cheddar, Pommes", "— CZK"], ["Saisonale Pasta", "", "— CZK"], ["Gebackener Käse", "Pommes, Remoulade", "— CZK"]]],
    ["Desserts und Kaffee", [["Hausgemachtes Dessert des Tages", "", "— CZK"], ["Espresso", "", "— CZK"]]],
  ],
  "menu_cta_h": "Sicher einen Tisch haben?", "menu_cta_p": "In einer Minute online reservieren.",
  "res_title": "Tisch reservieren – Restaurant Via Ferrata Děčín",
  "res_desc": "Reservieren Sie online einen Tisch im Restaurant Via Ferrata in Děčín. Tag, Uhrzeit und Personenzahl wählen.",
  "res_h": "Tisch reservieren", "res_p": "Wählen Sie Tag, Uhrzeit und Personenzahl. Wir bestätigen Ihre Reservierung per E-Mail.",
  "r_date": "Datum", "r_time": "Uhrzeit", "r_guests": "Personen", "r_area": "Wo möchten Sie sitzen", "r_opt": "(optional)",
  "r_big": "9 oder mehr", "r_big_msg": "Für Gruppen ab 9 Personen rufen Sie uns bitte unter {phone} an, oder sehen Sie sich die Vermietung des ganzen Restaurants an.",
  "r_name": "Vor- und Nachname", "r_phone": "Telefon", "r_email": "E-Mail", "r_note": "Anmerkung", "r_note_ph": "Feier, Kinderstuhl, Allergien…",
  "r_gdpr": "Ich stimme der Verarbeitung meiner personenbezogenen Daten zum Zweck der Reservierung zu.",
  "r_submit": "Reservierung senden", "r_done_h": "Vielen Dank, wir haben Ihre Reservierung erhalten",
  "r_done_p": "Die Bestätigung senden wir Ihnen per E-Mail. Falls sich etwas ändert, rufen Sie uns bitte an.",
  "r_demo": "Demo-Modus: Das Reservierungsformular ist noch nicht an ein System angebunden, es wurde nichts gesendet.",
  "r_again": "Neue Reservierung",
  "aside_h": "Gut zu wissen", "aside_list": ["Wir halten Ihren Tisch 15 Minuten frei.", "Ab 9 Personen bitte anrufen.", "Frühstück nur für Pensionsgäste."],
  "aside_rental": "Eine größere Feier geplant?", "aside_rental_a": "Das ganze Restaurant mieten",
  "areas": {"inside": "Drinnen", "terrace": "Terrasse"}, "nopref": "Egal",
  "rent_title": "Restaurant mieten für Feiern und Firmenevents – Via Ferrata Děčín",
  "rent_desc": "Mieten Sie das ganze Restaurant Via Ferrata in Děčín für bis zu 40 Gäste samt Terrasse. Feiern, Firmenevents, Familientreffen. Menü nach Wunsch.",
  "rent_h": "Das ganze Restaurant mieten", "rent_p": "Platz für bis zu 40 Gäste drinnen und eine Terrasse mit Blick auf den Klettersteig. Wir kümmern uns um Essen, Getränke und Service, Sie um Ihre Gäste.",
  "rent_for_h": "Ideal für", "rent_for": ["Geburtstage und Jubiläen", "Firmenfeiern und Meetings", "Familienfeiern und Taufen", "Kleine Hochzeitsfeiern", "Trauerfeiern", "Gruppen von Kletterern und Wanderern"],
  "rent_inc_h": "Darum kümmern wir uns", "rent_inc": ["Menü nach Wunsch: Buffet, serviertes Menü oder Grill", "Getränke und Service während der ganzen Feier", "Raumgestaltung nach Ihren Vorstellungen", "Terrasse je nach Wetter und Absprache"],
  "rent_inc_note": "Preise und Pakete folgen.",
  "steps_h": "So funktioniert es", "steps": [["Kontakt aufnehmen", "Rufen Sie an oder schreiben Sie uns Termin, Gästezahl und Art der Feier."], ["Details abstimmen", "Wir schlagen Menü und Raumaufteilung ganz nach Ihnen vor."], ["Termin bestätigen", "Nach der Abstimmung reservieren wir den Termin verbindlich."]],
  "q_h": "Unverbindliche Anfrage", "q_p": "Füllen Sie ein paar Angaben aus und wir bereiten eine E-Mail zum Versenden vor. Oder rufen Sie einfach an.",
  "q_type": "Art der Feier", "q_types": ["Geburtstag / Jubiläum", "Firmenevent", "Familienfeier", "Hochzeitsfeier", "Sonstiges"],
  "q_date": "Gewünschter Termin", "q_guests": "Anzahl Gäste", "q_name": "Name", "q_contact": "Telefon oder E-Mail",
  "q_note": "Was planen Sie", "q_submit": "Anfrage-E-Mail vorbereiten",
  "q_fallback": "Falls sich kein E-Mail-Fenster geöffnet hat, kopieren Sie den Text und senden Sie ihn an {email}.", "q_copy": "Text kopieren",
  "rent_ph": "Foto: das ganze Restaurant festlich vorbereitet",
  "js": {
    "openNow": "Geöffnet, heute bis {t}", "opensAt": "Heute ab {t} geöffnet", "closedNext": "Geschlossen, wir öffnen {d} um {t}", "closed": "Geschlossen",
    "noSlots": "An diesem Tag sind keine Zeiten mehr frei. Bitte wählen Sie einen anderen Tag.",
    "errDate": "Bitte wählen Sie ein Datum.", "errTime": "Bitte wählen Sie eine Uhrzeit.", "errGuests": "Bitte wählen Sie die Personenzahl.",
    "errBig": "Ab 9 Personen rufen Sie uns bitte an.", "errName": "Bitte geben Sie Ihren Namen ein.",
    "errPhone": "Bitte geben Sie eine gültige Telefonnummer ein.", "errEmail": "Bitte geben Sie eine gültige E-Mail ein.",
    "errGdpr": "Ohne Ihre Zustimmung können wir die Reservierung nicht annehmen.", "errRequired": "Bitte ausfüllen.",
    "errSend": "Die Reservierung konnte nicht gesendet werden. Bitte versuchen Sie es erneut oder rufen Sie uns an.",
    "sending": "Wird gesendet…", "submit": "Reservierung senden",
    "fDate": "Datum", "fTime": "Uhrzeit", "fGuests": "Personen", "fArea": "Platz", "fName": "Name", "fContact": "Kontakt",
    "noPref": "Keine Präferenz",
    "qHello": "Guten Tag, ich interessiere mich für die Anmietung des Restaurants.", "qType": "Art der Feier", "qNote": "Anmerkung", "qSubject": "Anfrage Raumvermietung",
    "copied": "Kopiert",
  },
},
}

# ------------------------------------------------------------------ fotky a popisky (alt)
PHOTOS = {"hero": "hero-kavarna-bar.jpg", "about": "steak-vyhled-zamek.jpg",
          "feats": ["aperol.jpg", "vyhled-zamek.jpg", "snidane.jpg"],
          "gallery": ["kachna.jpg", "polevka.jpg", "burger.jpg", "interier.jpg", "bar.jpg"],
          "rental": "oslava-stul.jpg", "rent_hero": "oslava-sal.jpg"}
ALT = {
 "cs": dict(hero_ph="Interiér Restaurace Via Ferrata večer", about_ph="Steak s výhledem na děčínský zámek",
            rental_ph="Slavnostně prostřená tabule", rent_ph="Restaurace připravená na oslavu",
            feat_alt=["Aperol spritz", "Výhled z restaurace na zámek", "Snídaně"],
            gallery=["Pečená kachna s noky", "Krémová polévka", "Burger s hranolky", "Interiér restaurace", "Bar"],
            menu_price="Polévka / hlavní jídlo", menu_price_v="65 Kč / 179 Kč",
            menu_allday="Během celého dne můžete vybírat i ze stálého jídelního lístku."),
 "en": dict(hero_ph="Restaurant Via Ferrata interior in the evening", about_ph="Steak with a view of Děčín Castle",
            rental_ph="A festive long table", rent_ph="The restaurant set for a celebration",
            feat_alt=["Aperol spritz", "View of the castle from the restaurant", "Breakfast"],
            gallery=["Roast duck with gnocchi", "Cream soup", "Burger with fries", "Restaurant interior", "Bar"],
            menu_price="Soup / main course", menu_price_v="CZK 65 / 179",
            menu_allday="All day long you can also order from our regular menu."),
 "de": dict(hero_ph="Innenraum des Restaurants Via Ferrata am Abend", about_ph="Steak mit Blick auf das Schloss Děčín",
            rental_ph="Festlich gedeckte Tafel", rent_ph="Das Restaurant für eine Feier vorbereitet",
            feat_alt=["Aperol Spritz", "Blick vom Restaurant auf das Schloss", "Frühstück"],
            gallery=["Gebratene Ente mit Gnocchi", "Cremesuppe", "Burger mit Pommes", "Innenraum", "Bar"],
            menu_price="Suppe / Hauptgericht", menu_price_v="65 / 179 CZK",
            menu_allday="Den ganzen Tag können Sie auch aus unserer festen Speisekarte wählen."),
}
for _l, _a in ALT.items():
    T[_l].update(_a)

e = html.escape

# ------------------------------------------------------------------ pomocné
UP = ""  # nastavuje se při generování stránky ("" nebo "../")
def ph(label, cls="", img=None, eager=False, pos=None):
    """Fotografie z assets/foto/. Bez img se zobrazí zástupná plocha s popisem."""
    if img:
        st = f' style="object-position:{pos}"' if pos else ""
        inner = f'<img src="{UP}assets/foto/{img}" alt="{e(label)}"{st} loading="{"eager" if eager else "lazy"}" decoding="async">'
        return f'<div class="ph has-img {cls}">{inner}</div>'
    return f'<div class="ph {cls}" role="img" aria-label="{e(label)}"><i>{e(label)}</i></div>'

def link(lang, page, from_lang, anchor=""):
    """Relativní odkaz ze stránky v jazyce from_lang na stránku page v jazyce lang."""
    up = "" if from_lang == "cs" else "../"
    return up + prefix(lang) + PAGES[page][lang] + anchor

def hours_rows(t):
    rows = []
    for i, h in enumerate(SITE["hours"]):
        v = f"{h[0]}–{h[1]}" if h else t["closed"]
        rows.append(f'<tr data-day="{i}"><td>{t["days"][i]}</td><td>{v}</td></tr>')
    return "".join(rows)

def jsonld(lang):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data = {
        "@context": "https://schema.org", "@type": "Restaurant", "name": SITE["name"],
        "url": SITE["base_url"] + prefix(lang), "telephone": SITE["phone"], "priceRange": "300–400 CZK",
        "servesCuisine": ["Czech", "European"], "acceptsReservations": True,
        "address": {"@type": "PostalAddress", "streetAddress": "Labské nábřeží 317/19", "addressLocality": "Děčín",
                    "postalCode": "405 02", "addressCountry": "CZ"},
        "geo": {"@type": "GeoCoordinates", "latitude": SITE["geo"][0], "longitude": SITE["geo"][1]},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": days[i],
                                       "opens": h[0], "closes": h[1]} for i, h in enumerate(SITE["hours"]) if h],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": SITE["rating_en"], "reviewCount": SITE["reviews_count"]},
    }
    return json.dumps(data, ensure_ascii=False)

# ------------------------------------------------------------------ rámec stránky
def page(lang, key, title, desc, body, active=None, solid=False):
    t = T[lang]
    up = "" if lang == "cs" else "../"
    nav_items = [
        ("menu", link(lang, "menu", lang)), ("about", link(lang, "home", lang, "#o-nas")),
        ("rental", link(lang, "rental", lang)), ("reviews", link(lang, "home", lang, "#recenze")),
        ("contact", link(lang, "home", lang, "#kontakt")),
    ]
    cur = {"menu": "menu", "rental": "rental"}.get(key)
    nav = "".join(f'<a href="{h}"{" aria-current=page" if cur == k else ""}>{t["nav"][k]}</a>' for k, h in nav_items)
    langs = "".join(f'<a href="{link(l, key, lang)}" hreflang="{l}" lang="{l}"{" aria-current=true" if l == lang else ""}>{l.upper()}</a>' for l in LANGS)
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE["base_url"]}{prefix(l)}{PAGES[key][l]}">' for l in LANGS)
    data = {
        "lang": lang, "locale": t["locale"], "email": SITE["email"], "hours": SITE["hours"],
        "strings": {**t["js"], "days": t["days"], "areas": t["areas"]},
        "reservation": RESERVATION,
    }
    tel = f'<a class="btn" href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a>'
    mcta = "" if key == "reserve" else f'<div class="mcta"><a class="btn ghost" href="tel:{SITE["phone_href"]}">{t["c_phone"]}</a><a class="btn" href="{link(lang, "reserve", lang)}">{t["cta"]}</a></div>'
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#ffffff">
<link rel="icon" type="image/png" href="{up}assets/favicon.png">
<meta property="og:image" content="{SITE["base_url"]}assets/foto/hero-interier.jpg">
<link rel="canonical" href="{SITE["base_url"]}{prefix(lang)}{PAGES[key][lang]}">
{alts}
<link rel="preload" href="{up}assets/fonts/merriweather.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}assets/fonts/catamaran.woff2" as="font" type="font/woff2" crossorigin>
<script>try{{var t=localStorage.getItem("vf-theme");if(t!=="light"&&t!=="dark")t=matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="stylesheet" href="{up}assets/style.css">
<script type="application/ld+json">{jsonld(lang)}</script>
</head>
<body class="{'has-mcta' if mcta else ''}">
<a class="skip" href="#obsah">{t["skip"]}</a>
<header class="hdr{' always' if solid else ''}">
  <div class="wrap">
    <a class="brand" href="{link(lang, 'home', lang)}" aria-label="Restaurace Via Ferrata"><img class="ic-l" src="{up}assets/icon-light.png" alt="" width="27" height="40"><img class="ic-d" src="{up}assets/icon-dark.png" alt="" width="27" height="40"><span><small>{t["sub"].upper()}</small><b>VIA FERRATA</b></span></a>
    <nav class="nav" aria-label="Hlavní">{nav}<div class="langs mob">{langs}</div><a class="btn mob" href="{link(lang, 'reserve', lang)}">{t["cta"]}</a></nav>
    <button class="theme-btn" type="button" aria-label="{t['theme_toggle']}" title="{t['theme_toggle']}"><svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg><svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></svg></button>
    <div class="langs desk">{langs}</div>
    <a class="btn desk" href="{link(lang, 'reserve', lang)}">{t["cta"]}</a>
    <button class="menu-btn" aria-expanded="false" aria-label="{t['menu_toggle']}"><span></span><span></span></button>
  </div>
</header>
<main id="obsah">
{body}
</main>
<footer class="ftr">
  <div class="wrap">
    <div>
      <div><a class="flogo" href="{link(lang, 'home', lang)}"><img src="{up}assets/logo-light.png" alt="Restaurace Via Ferrata" width="200" height="126"></a><p>{t["f_about"]}</p></div>
      <div><h4>{t["f_visit"]}</h4><ul><li>{SITE["street"]}</li><li>{SITE["city"]}</li><li><a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a></li><li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li></ul></div>
      <div><h4>{t["nav"]["menu"]}</h4><ul><li><a href="{link(lang, 'menu', lang)}">{t["nav"]["menu"]}</a></li><li><a href="{link(lang, 'reserve', lang)}">{t["cta"]}</a></li><li><a href="{link(lang, 'rental', lang)}">{t["nav"]["rental"]}</a></li></ul></div>
      <div><h4>{t["f_follow"]}</h4><ul><li><a href="{SITE["facebook"]}">Facebook</a></li><li><a href="{SITE["instagram"]}">Instagram</a></li><li><a href="{SITE["maps"]}">Google</a></li><li><a href="{SITE["penzion"]}">{t["f_penzion"]}</a></li></ul></div>
    </div>
    <div class="base"><span>© 2026 {SITE["name"]}. {t["rights"]}</span><a href="#">{t["f_privacy"]}</a></div>
  </div>
</footer>
{mcta}
<script id="site-data" type="application/json">{json.dumps(data, ensure_ascii=False)}</script>
<script src="{up}assets/app.js"></script>
</body>
</html>"""

# ------------------------------------------------------------------ úvodní stránka
def home(lang):
    t = T[lang]; up = "" if lang == "cs" else "../"
    feats = "".join(f'<div class="feat rv">{ph(t["feat_alt"][i], img=PHOTOS["feats"][i], pos="center 25%" if i == 1 else None)}<h3>{f[0]}</h3><p>{f[1]}</p></div>' for i, f in enumerate(t["feats"]))
    gal = "".join(ph(g, img=PHOTOS["gallery"][i]) for i, g in enumerate(t["gallery"]))
    revs = "".join(f'<figure class="review rv"><div class="stars" aria-label="5/5">★★★★★</div><blockquote>„{e(r[0])}“</blockquote><figcaption><b>{e(r[1])}</b><br>{e(r[2])}</figcaption></figure>' for r in t["reviews"])
    ticks = "".join(f"<li>{x}</li>" for x in t["rental_list"])
    rating = SITE["rating"] if lang != "en" else SITE["rating_en"]
    body = f"""
<section class="hero">
  {ph(t["hero_ph"], img=PHOTOS["hero"], eager=True)}
  <div class="wrap">
    <h1>{t["hero_h"]}</h1>
    <p>{t["hero_p"]}</p>
    <div class="btns"><a class="btn light" href="{link(lang, 'reserve', lang)}">{t["cta"]}</a><a class="btn line-light" href="#menu">{t["see_menu"]}</a></div>
  </div>
</section>

<section class="facts" aria-label="{t['f_hours']}">
  <div class="wrap">
    <a class="fact" href="#kontakt"><span class="label">{t["f_hours"]}</span><strong data-today-hours>{SITE["hours"][0][0]}–{SITE["hours"][0][1]}</strong><span class="more">{t["f_all_hours"]}</span></a>
    <a class="fact" href="{SITE["directions"]}"><span class="label">{t["f_where"]}</span><strong>{SITE["street"]}, Děčín</strong><span class="more">{t["f_nav"]}</span></a>
  </div>
</section>

<section class="band" id="menu">
  <div class="wrap menu-card">
    <div class="rv">
      <p class="label">{t["menu_label"]}</p>
      <h2>{t["menu_h"]}</h2>
      <p class="lead">{t["menu_p"]}</p>
      <ul class="menu-meta">
        <li><span>{t["menu_lunch"]}</span><span>{t["menu_weekdays"]} {SITE["lunch"]}</span></li>
        <li><span>{t["menu_price"]}</span><span>{t["menu_price_v"]}</span></li>
      </ul>
      <p class="note" style="margin-top:-14px">{t["menu_allday"]}</p>
      <div class="btns"><a class="btn" href="{link(lang, 'menu', lang)}">{t["menu_full"]}</a><a class="btn ghost" href="{link(lang, 'reserve', lang)}">{t["cta"]}</a></div>
    </div>
    <button class="menu-img rv" data-open-menu aria-label="{t['menu_zoom']}"><img src="{up}assets/tydenni-menu.png" alt="{t['menu_alt']}" width="1080" height="1350" loading="lazy"></button>
  </div>
</section>
{menu_dialog(lang)}

<section class="band alt" id="o-nas">
  <div class="wrap">
    <div class="split">
      <div class="rv"><p class="label">{t["about_label"]}</p><h2>{t["about_h"]}</h2><p class="lead">{t["about_p1"]}</p><p>{t["about_p2"]}</p></div>
      {ph(t["about_ph"], "rv", img=PHOTOS["about"])}
    </div>
    <div class="feats">{feats}</div>
    <div class="gallery">{gal}</div>
  </div>
</section>

<section class="band dark" id="pronajem">
  <div class="wrap split rev">
    <div class="rv">
      <p class="label">{t["rental_label"]}</p>
      <h2>{t["rental_h"]}</h2>
      <p class="lead">{t["rental_p"]}</p>
      <p><span class="big-num">40</span>&nbsp; {t["rental_cap"]} · {t["rental_cap_t"]}</p>
      <ul class="ticks">{ticks}</ul>
      <a class="btn light" href="{link(lang, 'rental', lang)}">{t["rental_more"]}</a>
    </div>
    {ph(t["rental_ph"], "rv", img=PHOTOS["rental"])}
  </div>
</section>

<section class="band alt" id="recenze">
  <div class="wrap">
    <div class="rev-head">
      <div><p class="label">{t["reviews_label"]}</p><h2 style="margin:0">{t["reviews_h"]}</h2></div>
      <div class="score"><span class="big-num">{rating}</span><div><div class="stars" aria-hidden="true">★★★★★</div><div class="note">{t["reviews_count"].format(n=SITE["reviews_count"])}</div></div></div>
    </div>
    <div class="reviews">{revs}</div>
    <p style="margin-top:32px"><a class="btn ghost" href="{SITE["maps"]}">{t["reviews_all"]}</a></p>
  </div>
</section>

{contact_block(lang)}
"""
    return page(lang, "home", t["home_title"], t["home_desc"], body)

def menu_dialog(lang):
    t = T[lang]; up = "" if lang == "cs" else "../"
    return f'<dialog id="menu-dialog" aria-label="{t["menu_alt"]}"><form method="dialog"><button class="btn light">{t["close"]} ✕</button></form><img src="{up}assets/tydenni-menu.png" alt="{t["menu_alt"]}" width="1080" height="1350"></dialog>'

def contact_block(lang):
    t = T[lang]
    return f"""
<section class="band" id="kontakt">
  <div class="wrap contact">
    <div class="rv">
      <p class="label">{t["contact_label"]}</p>
      <h2>{t["contact_h"]}</h2>
      <ul class="c-list">
        <li><span>{t["c_addr"]}</span><a href="{SITE["directions"]}">{SITE["street"]}, {SITE["city"]}</a></li>
        <li><span>{t["c_phone"]}</span><a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a></li>
        <li><span>{t["c_email"]}</span><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
        <li><span>{t["c_parking"]}</span><span>{t["c_parking_v"]}</span></li>
      </ul>
      <h3>{t["hours_h"]}</h3>
      <table class="hours">{hours_rows(t)}</table>
      <p class="note">{t["hours_note"]}</p>
    </div>
    <div class="map rv">
      <a class="map-fallback" href="{SITE["maps"]}">{ph(t["map_ph"], "map")}</a>
      <iframe title="{e(t["map_ph"])}" src="https://maps.google.com/maps?q=Restaurace%20Via%20Ferrata%2C%20Labsk%C3%A9%20n%C3%A1b%C5%99e%C5%BE%C3%AD%20317%2F19%2C%20D%C4%9B%C4%8D%C3%ADn&z=16&hl={lang}&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      <a class="btn map-btn" href="{SITE["directions"]}">{t["f_nav"]}</a>
    </div>
  </div>
</section>"""

# ------------------------------------------------------------------ menu
def menu_page(lang):
    t = T[lang]; up = "" if lang == "cs" else "../"
    carte = ""
    for sec, items in t["carte"]:
        carte += f"<h3>{sec}</h3>" + "".join(
            f'<div class="dish"><div><b>{n}</b>{f"<small>{d}</small>" if d else ""}</div><span class="price">{p}</span></div>' for n, d, p in items)
    body = f"""
<section class="sub-hero">
  <div class="wrap">
    <p class="crumbs"><a href="{link(lang, 'home', lang)}">Via Ferrata</a> / {t["menu_sub_h"]}</p>
    <h1>{t["menu_sub_h"]}</h1>
    <p class="lead">{t["menu_sub_p"]}</p>
  </div>
</section>
<section class="band">
  <div class="wrap menu-card">
    <div>
      <ul class="menu-meta" style="margin-top:0">
        <li><span>{t["menu_lunch"]}</span><span>{t["menu_weekdays"]} {SITE["lunch"]}</span></li>
        <li><span>{t["f_hours"]}</span><span data-today-hours></span></li>
        <li><span>{t["menu_price"]}</span><span>{t["menu_price_v"]}</span></li>
      </ul>
      <p class="note">{t["menu_allday"]}</p>
      <p class="muted">{t["menu_p"]}</p>
      <div class="btns"><a class="btn" href="{link(lang, 'reserve', lang)}">{t["cta"]}</a><a class="btn ghost" href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a></div>
    </div>
    <button class="menu-img" data-open-menu aria-label="{t['menu_zoom']}"><img src="{up}assets/tydenni-menu.png" alt="{t['menu_alt']}" width="1080" height="1350"></button>
  </div>
</section>
{menu_dialog(lang)}
<section class="band alt">
  <div class="wrap">
    <h2>{t["carte_h"]}</h2>
    <p class="note">{t["carte_note"]}</p>
    <div class="carte">{carte}</div>
  </div>
</section>
<section class="band">
  <div class="wrap" style="text-align:center">
    <h2>{t["menu_cta_h"]}</h2>
    <p class="lead" style="margin:0 auto 28px">{t["menu_cta_p"]}</p>
    <a class="btn" href="{link(lang, 'reserve', lang)}">{t["cta"]}</a>
  </div>
</section>"""
    return page(lang, "menu", t["menu_title"], t["menu_desc"], body, solid=True)

# ------------------------------------------------------------------ rezervace
def reserve_page(lang):
    t = T[lang]
    guests = "".join(f'<option value="{i}"{" selected" if i == 2 else ""}>{i}</option>' for i in range(1, RESERVATION["maxGuests"] + 1))
    guests += f'<option value="big">{t["r_big"]}</option>'
    aside = "".join(f"<li>{x}</li>" for x in t["aside_list"])
    big_msg = t["r_big_msg"].format(phone=f'<a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a>')
    body = f"""
<section class="sub-hero">
  <div class="wrap">
    <p class="crumbs"><a href="{link(lang, 'home', lang)}">Via Ferrata</a> / {t["res_h"]}</p>
    <h1>{t["res_h"]}</h1>
    <p class="lead">{t["res_p"]}</p>
  </div>
</section>
<section class="band" style="padding-top:56px">
  <div class="wrap form-grid">
    <div>
      <form id="reservation-form" novalidate>
        <div class="row">
          <div class="field"><label for="r-date">{t["r_date"]}</label><input type="date" id="r-date" name="date" required><span class="msg"></span></div>
          <div class="field"><label for="r-guests">{t["r_guests"]}</label><select id="r-guests" name="guests">{guests}</select><span class="msg"></span></div>
        </div>
        <p class="big-group">{big_msg} <a href="{link(lang, 'rental', lang)}">{t["aside_rental_a"]}</a></p>
        <fieldset class="field"><legend>{t["r_time"]}</legend><input type="hidden" id="r-time" name="time"><div class="slots" id="r-slots"></div><span class="msg"></span></fieldset>
        <fieldset class="field"><legend>{t["r_area"]} <span class="opt">{t["r_opt"]}</span></legend>
          <div class="seg">
            <label><input type="radio" name="area" value="" checked><span>{t["nopref"]}</span></label>
            <label><input type="radio" name="area" value="inside"><span>{t["areas"]["inside"]}</span></label>
            <label><input type="radio" name="area" value="terrace"><span>{t["areas"]["terrace"]}</span></label>
          </div>
        </fieldset>
        <div class="field"><label for="r-name">{t["r_name"]}</label><input id="r-name" name="name" autocomplete="name" required><span class="msg"></span></div>
        <div class="row">
          <div class="field"><label for="r-phone">{t["r_phone"]}</label><input id="r-phone" name="phone" type="tel" autocomplete="tel" placeholder="+420" required><span class="msg"></span></div>
          <div class="field"><label for="r-email">{t["r_email"]}</label><input id="r-email" name="email" type="email" autocomplete="email" required><span class="msg"></span></div>
        </div>
        <div class="field"><label for="r-note">{t["r_note"]} <span class="opt">{t["r_opt"]}</span></label><textarea id="r-note" name="note" placeholder="{t['r_note_ph']}"></textarea></div>
        <div class="field"><label class="check"><input type="checkbox" id="r-gdpr" required><span>{t["r_gdpr"]}</span></label><span class="msg"></span></div>
        <div><button class="btn" type="submit">{t["r_submit"]}</button></div>
      </form>
      <div class="done" aria-live="polite">
        <h2>{t["r_done_h"]}</h2>
        <p class="muted">{t["r_done_p"]}</p>
        <dl></dl>
        <button class="btn ghost" type="button" data-again>{t["r_again"]}</button>
        <p class="demo">{t["r_demo"]}</p>
      </div>
    </div>
    <aside class="aside">
      <h3>{t["aside_h"]}</h3>
      <ul class="ticks" style="grid-template-columns:1fr;margin-top:12px">{aside}</ul>
      <ul class="c-list">
        <li><span>{t["c_phone"]}</span><a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a></li>
        <li><span>{t["c_addr"]}</span><a href="{SITE["directions"]}">{SITE["street"]}, Děčín</a></li>
        <li><span>{t["f_hours"]}</span><span data-today-hours></span></li>
      </ul>
      <p style="margin:0"><b>{t["aside_rental"]}</b><br><a href="{link(lang, 'rental', lang)}">{t["aside_rental_a"]} →</a></p>
    </aside>
  </div>
</section>"""
    return page(lang, "reserve", t["res_title"], t["res_desc"], body, solid=True)

# ------------------------------------------------------------------ pronájem
def rental_page(lang):
    t = T[lang]
    fors = "".join(f"<li>{x}</li>" for x in t["rent_for"])
    incs = "".join(f"<li>{x}</li>" for x in t["rent_inc"])
    steps = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in t["steps"])
    types = "".join(f"<option>{x}</option>" for x in t["q_types"])
    body = f"""
<section class="sub-hero" style="border:0">
  <div class="wrap">
    <p class="crumbs"><a href="{link(lang, 'home', lang)}">Via Ferrata</a> / {t["nav"]["rental"]}</p>
    <div class="split" style="align-items:end">
      <div><h1>{t["rent_h"]}</h1><p class="lead">{t["rent_p"]}</p>
      <div class="btns"><a class="btn" href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a><a class="btn ghost" href="#poptavka">{t["q_h"]}</a></div></div>
      <div><p class="big-num" style="margin:0">40</p><p class="muted" style="margin:0">{t["rental_cap"]} · {t["rental_cap_t"]}</p></div>
    </div>
  </div>
</section>
<div class="wrap">{ph(t["rent_ph"], "photo-hero", img=PHOTOS["rent_hero"], eager=True)}</div>
<section class="band">
  <div class="wrap split" style="align-items:start">
    <div class="rv"><h2>{t["rent_for_h"]}</h2><ul class="ticks" style="grid-template-columns:1fr">{fors}</ul></div>
    <div class="rv"><h2>{t["rent_inc_h"]}</h2><ul class="ticks" style="grid-template-columns:1fr">{incs}</ul><p class="note">{t["rent_inc_note"]}</p></div>
  </div>
</section>
<section class="band alt">
  <div class="wrap"><h2>{t["steps_h"]}</h2><ol class="steps">{steps}</ol></div>
</section>
<section class="band" id="poptavka">
  <div class="wrap form-grid">
    <div>
      <h2>{t["q_h"]}</h2><p class="lead">{t["q_p"]}</p>
      <form id="rental-form" novalidate>
        <div class="row">
          <div class="field"><label for="q-type">{t["q_type"]}</label><select id="q-type" name="q-type">{types}</select></div>
          <div class="field"><label for="q-date">{t["q_date"]}</label><input type="date" id="q-date" name="q-date"></div>
        </div>
        <div class="row">
          <div class="field"><label for="q-guests">{t["q_guests"]}</label><input type="number" id="q-guests" name="q-guests" min="1" max="200" inputmode="numeric"></div>
          <div class="field"><label for="q-name">{t["q_name"]}</label><input id="q-name" name="q-name" autocomplete="name"><span class="msg"></span></div>
        </div>
        <div class="field"><label for="q-contact">{t["q_contact"]}</label><input id="q-contact" name="q-contact"><span class="msg"></span></div>
        <div class="field"><label for="q-note">{t["q_note"]} <span class="opt">{t["r_opt"]}</span></label><textarea id="q-note" name="q-note"></textarea></div>
        <div><button class="btn" type="submit">{t["q_submit"]}</button></div>
        <div class="copy-box"><p class="note">{t["q_fallback"].format(email=SITE["email"])}</p><textarea readonly></textarea><button type="button" class="btn ghost" data-copy>{t["q_copy"]}</button></div>
      </form>
    </div>
    <aside class="aside">
      <h3>{t["contact_label"]}</h3>
      <ul class="c-list">
        <li><span>{t["c_phone"]}</span><a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a></li>
        <li><span>{t["c_email"]}</span><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
        <li><span>{t["c_addr"]}</span><a href="{SITE["directions"]}">{SITE["street"]}, Děčín</a></li>
      </ul>
    </aside>
  </div>
</section>"""
    return page(lang, "rental", t["rent_title"], t["rent_desc"], body, solid=True)

# ------------------------------------------------------------------ build
def main():
    if DIST.exists(): shutil.rmtree(DIST)
    shutil.copytree(ROOT / "assets", DIST / "assets")
    for lang in LANGS:
        out = DIST / prefix(lang); out.mkdir(parents=True, exist_ok=True)
        global UP
        UP = "" if lang == "cs" else "../"
        for key, fn in [("home", home), ("menu", menu_page), ("reserve", reserve_page), ("rental", rental_page)]:
            (out / PAGES[key][lang]).write_text(fn(lang), encoding="utf-8")
    print("hotovo:", sorted(str(p.relative_to(DIST)) for p in DIST.rglob("*.html")))

if __name__ == "__main__":
    main()
