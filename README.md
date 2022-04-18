# Rundown parser

Disclaimer: Althougt we develop this package as open sourc it is used internally for parsing specific type of
XML (know as Rundonws) exported from OpenMedia broadcast system. Feel free to read the source code.

## Install

&hellip;

## Usage

Use the `extract` command to:

> Extract the broadcast data from the OpenMedia XML files and store them in Excel.

    cro.broadcast.wrangling.extract --year <year> --week <week>   # e.g.,
    cro.broadcast.wrangling.extract --year 2021 --week 21

Note: The week number is without a preceding zero e.g., `1` and not a `01`.

For batch extracting use the `scripts\batch-extract.cmd` script e.g.

    batch-extract.cmd 1 2 3 4 5 6 7 8 9 10

## Rundown file documentation

Rundown XML soubor má následující strukturu.

Kořenovým uzlem je `<OPENMEDIA>`. Ten obsahuje vždy dva uzly `<SERVER>`, který nepotřebujeme a `<OM_OBJECT>` s atributem `TemplateName = "Radio Rundown"`. V něm je uložen veškerý další obsah, který chceme získat. Radio Rundown obsahuj hlavičku `<OM_HEADER>` a dále vždy pro každou plánovanou hodinu uzel `<OM_RECORD`>. Jako příklad, pro planované vysílání od 10 do 13 hodin, bude obsahovat tři uzly `<OM_RECORD>`, pro každou hodinu jeden tj. 10-11, 11-12, 12-13. Každý takový záznam tedy chceme získat a dále z každého získat pro danou hodinu všechny dostupné informace.

Z každého nejvýše položeného objektu `<OM_RECORD>` získáme primárně uzel `OM_OBJECT` (`Hourly Rundown`).

Z něho poté:
-
-
-


```
<OPENMEDIA>
  <SERVER>...<SERVER>
  <OM_OBJECT Radio Rundown>
    <OM_HEADER>...</OM_HEADER>
    <OM_RECORD>
      <OM_FIELD>...</OM_FIELD>
      ...
      <OM_OBJECT Hourly Rundown>
        <OM_HEADER>...</OM_HEADER>
        <OM_UPLINK />
        <OM_RECORD>
            <OM_FIELD>...</OM_FIELD>
            ...
            <OM_OBJECT Sub Rundown>
                <OM_HEADER>...</OM_HEADER>
                <OM_UPLINK />
                <OM_RECORD>
                    <OM_FIELD>...</OM_FIELD>
                    ...
                    <OM_OBJECT Radio Story>
                      <OM_HEADER>...</OM_HEADER>
                      <OM_UPLINK />
                      <OM_RECORD>
                        <OM_FIELD>...</OM_FIELD>
                        ...
                        <OM_OBJECT AudioClip>


```


### Stanice

- Plus
- Radiožurnál
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
