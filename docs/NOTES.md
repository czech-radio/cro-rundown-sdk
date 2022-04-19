# Popis Rundown XML souboru

Rundown XML soubor má následující strukturu:

Kořenovým uzlem je `<OPENMEDIA>`. Ten obsahuje vždy dva uzly `<SERVER>`, který nepotřebujeme a `<OM_OBJECT>` s atributem `TemplateName = "Radio Rundown"`. V něm je uložen veškerý další obsah, který chceme získat. Radio Rundown obsahuj hlavičku `<OM_HEADER>` a dále vždy pro každou plánovanou hodinu uzel `<OM_RECORD`>. Jako příklad, pro planované vysílání od 10 do 13 hodin, bude obsahovat tři uzly `<OM_RECORD>`, pro každou hodinu jeden tj. 10-11, 11-12, 12-13. Každý takový záznam tedy chceme získat a dále z každého získat pro danou hodinu všechny dostupné informace.

Z každého nejvýše položeného objektu `<OM_RECORD>` získáme primárně uzel `OM_OBJECT` (`Hourly Rundown`).

Potřebujem získat atributy
- stanice station (id)
- datum date
- čas time
- trvání duration
- název title
- podnázev subtitle


- Audioclip
- Radio Story
- Contact Item


V názvech XML souborů a v jeoch datech se vyskytují tyto stanice:

- Plus, Radiožurnál
- Dvojka
- Vltava
- Pohoda
- Wave
- RŽ_Sport

- ČRo_Brno
- ČRo_DAB_Praha
- ČRo_Sever
- ČRo_Plzeň
- ČRo_Budějovice
- ČRo_Ostrava
- ČRo_Vysočina
- ČRo_Zlín
- ČRo_Region_SC
- ČRo_Liberec
- ČRo_Hradec_Králové
- ČRo_Pardubice
- ČRo_Olomouc
- ČRo_Karlovy_Vary
