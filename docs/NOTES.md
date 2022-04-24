
# Extrakce dat z Rundown XML

## Co chceme získat

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

## Zdroj Rundown XML souborů

Zdrojem je systém OpenMedia. Každý den exportováno asi 70 XML seoborů do daného adresáře.
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

## Popis Rundown XML souborů

Rundown XML soubor má následující strukturu:

Kořenovým uzlem je `<OPENMEDIA>`. Ten obsahuje vždy dva uzly `<SERVER>`, který nepotřebujeme a `<OM_OBJECT>` s atributem `TemplateName = "Radio Rundown"`, který nazýváme _Radio Rundown_. V něm je uložen veškerý další obsah, který chceme získat.

Uzel _Radio Rundown_ obsahuj hlavičku `<OM_HEADER>` s informacemi

- _textový kód stanice_, _datum_ a _hodinobý blok_ v uzlu

  ```xml
  <OM_FIELD FieldType="1" FieldID="8" FieldName="Název" IsEmpty="no">
    <OM_STRING>10-13 Plus - Mon, 04.04.2022</OM_STRING>
  </OM_FIELD>
  ```

- _číselný kód stanice_ v

  ```xml
  <OM_FIELD FieldType="2" FieldID="5081" FieldName="Stanice" IsEmpty="no">
    <OM_INT32>13</OM_INT32>
  </OM_FIELD>
  ```

(Co další pole 1005, 1009, 1010?)

Ve strutuře XML jsme u bodu __[1]__:

```xml
<OPENMEDIA>
  <OM_SERVER>...</OM_SERVER>
  <OM_OBJECT TemplateName = "Radio Rundown">
    <!-- [1] -->
    <OM_HEADER>
        <OM_FIELD FieldID="8"><OM_STRING>10-13 Plus - Mon, 04.04.2022</OM_STRING></OM_FIELD>
        <OM_FIELD FieldType="2" FieldID="5081" FieldName="Stanice" IsEmpty="no"><OM_INT32>13</OM_INT32></OM_FIELD>
        ...
    </OM_HEADER>
    <!-- END -->
    <!-- [2] -->
    <OM_RECORD RecordID="3">...</OM_RECORD>
    <OM_RECORD RecordID="4">...</OM_RECORD>
    <OM_RECORD RecordID="5">...</OM_RECORD>
    <!-- END -->
  </OM_OBJECT>
</OPENMEDIA>
```

Pro každou plánovanou hodinu je v uzlu _Radio Rundown_ vložen uzel `<OM_RECORD`>. Jako příklad, pro planované vysílání od 10 do 13 hodin, bude obsahovat tři uzly `<OM_RECORD>` viz bod __[2]__, pro každou hodinu jeden tj. 10-11, 11-12, 12-13. Každý takový záznam tedy chceme získat a dále z každého získat pro danou hodinu všechny dostupné informace. _Record_ obsahuje pole `<OM_FIELD>` z nihž nic nepotřebujeme a dále uzel `<OM_OBJECT TemplateName="Hourly Rundown">`, který nazýváme _Hourly Rundown_. Objekt _Hourly Rundown_ obsahuje v hlavičce jedinou využitelnou informaci pro _hodinový blok_

```xml
<OM_HEADER>
  <OM_FIELD FieldType="1" FieldID="8" FieldName="Název" IsEmpty="no">
    <OM_STRING>12:00-13:00</OM_STRING>
  </OM_FIELD>
</OM_HEADER>
```

Objekt _Hourly Rundown_ dále obsahuje kolekci uzlů `<OM_RECORD>` např. pět...

Ze uzlu _Record_ získáme

```xml
<OM_FIELD FieldType="1" FieldID="5001" FieldName="Template Name (String)" IsEmpty="no">
    <OM_STRING>Radio Story</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="5079" FieldName="Cíl výroby" IsEmpty="no">
    <OM_STRING>Proud</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="5" FieldName="Vytvořil" IsEmpty="no">
    <OM_STRING>Vintr Stanislav (svintr)</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="6" FieldName="Autor" IsEmpty="no">
    <OM_STRING>Boudhen Senková Zita (zsenkova)</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="8" FieldName="Název" IsEmpty="no">
    <OM_STRING>0404 JTV Kubáček</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="12" FieldName="Redakce" IsEmpty="no">
    <OM_STRING>Plus</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="13" FieldName="Moderátor" IsEmpty="no">
    <OM_STRING>Vintr Stanislav (svintr)</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="2" FieldID="321" FieldName="Formát" IsEmpty="no">
    <OM_INT32>2919</OM_INT32>
</OM_FIELD>

<OM_FIELD FieldType="4" FieldID="1036" FieldName="Audio stopáž" IsEmpty="no">
    <OM_TIMESPAN>1524000</OM_TIMESPAN>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="5016" FieldName="Téma" IsEmpty="no">
    <OM_STRING>01-Politika, státní správa a samospráva</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="5070" FieldName="Schválil redakce" IsEmpty="no">
    <OM_STRING>Vintr Stanislav (svintr)</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="5071" FieldName="Schválil stanice" IsEmpty="no">
    <OM_STRING>Vintr Stanislav (svintr)</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="5079" FieldName="Cíl výroby" IsEmpty="no">
    <OM_STRING>Proud</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="2" FieldID="5081" FieldName="Stanice" IsEmpty="no">
    <OM_INT32>13</OM_INT32>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="5082" FieldName="ItemCode" IsEmpty="no">
    <OM_STRING>PS5362007</OM_STRING>
</OM_FIELD>


```

K němu je příslušný zanořený objekt `<OM_OBJECT TemplateName="Radio Story">`. V něm se opakují některé informace z Recordu a můžeme z hlavičky získat:

```xml
<OM_FIELD FieldType="1" FieldID="14" FieldName="Plain Text" IsEmpty="no">
    <OM_STRING>((PROMO: Sto dní vlády kabinetu premiéra Petra Fialy a jak ovlivnila agrese Ruska proti Ukrajině českou politicku scénu, o tom dnes mluvil politog Jan Kubáček v pořadu Jak to vidí. Ve vysílání Dvojky se ptala Zita Senková.

Ohlášení:))


((Respondenti:

Audio:

Začíná: Sto dní
Končí: rozhlasu

Odhlášení:))

((--------------------------------------------------
SPOJÁKY/SCÉNÁŘ:

))</OM_STRING>
</OM_FIELD>


<OM_FIELD FieldType="1" FieldID="16" FieldName="Druh" IsEmpty="no">
    <OM_STRING>Domácí; Zahraniční</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="2" FieldID="321" FieldName="Formát" IsEmpty="no">
    <OM_INT32>2919</OM_INT32>
</OM_FIELD>

<OM_FIELD FieldType="4" FieldID="1036" FieldName="Audio stopáž" IsEmpty="no">
    <OM_TIMESPAN>1524000</OM_TIMESPAN>
</OM_FIELD>
<!-- Stopáž a spočtená stopáž jsou zdá se vždy stejné -->

<OM_FIELD FieldType="1" FieldID="5016" FieldName="Téma" IsEmpty="no">
    <OM_STRING>01-Politika, státní správa a samospráva</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="8" FieldName="Název" IsEmpty="no">
    <OM_STRING>Kubáček, Jan</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="304" FieldName="Poznámka" IsEmpty="no">
    <OM_STRING>Charismatický, dobrý popularizátor politologie</OM_STRING>
</OM_FIELD>

<!-- Trochu se liší od informace v rodičovském záznamu. -->

<OM_FIELD FieldType="1" FieldID="421" FieldName="Jméno" IsEmpty="no">
    <OM_STRING>Jan</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="422" FieldName="Příjmení" IsEmpty="no">
    <OM_STRING>Kubáček</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="5001" FieldName="Template Name (String)" IsEmpty="no">
    <OM_STRING>Contact Item</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="5015" FieldName="Politická příslušnost" IsEmpty="no">
    <OM_STRING>BEZPP</OM_STRING>
</OM_FIELD>

<OM_FIELD FieldType="1" FieldID="5016" FieldName="Téma" IsEmpty="no">
    <OM_STRING>01-Politika, státní správa</OM_STRING>
</OM_FIELD>

```

Obsahuje pak možné dva záznamy
- `<OM_RECORD> <OM_FIELD>TemplateName="Contact Item" /> ... </OM_RECORD>`
- `<OM_RECORD> <OM_FIELD>TemplateName="Audio" /> ...</OM_RECORD>`.

které obsahují buď `<OM_OBJECT Contact Item>` nebo `<OM_OBJECT Audioclip>`


## Poznámky

- `<OM_OBJECT>` obsahuje pole `<OM_FIELD>` uzavřená v hlavičce `<OM_HEADER>`.
- `<OM_RECORD>` obsahuje pole `<OM_FIELD>` neuzavřená v hlavičce `<OM_HEADER>`.
