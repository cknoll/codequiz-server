-> Model: TC_Membership

id = 2

task = T001:Funktions-Aufrufe

group = TC001:Test1

ordering = 10.0

- - - 

id = 3

task = T002:Funktions-Aufrufe (Wdh.)

group = TC001:Test1

ordering = 12.0

- - - 

id = 4

task = T004:Syntax-Fehler

group = TC002:Python Grundlagen 1

ordering = 10.0

- - - 

id = 5

task = T001:Funktions-Aufrufe

group = TC002:Python Grundlagen 1

ordering = 20.0

- - - 

id = 6

task = T003:Typ-Umwandlung 

group = TC002:Python Grundlagen 1

ordering = 30.0

- - - 

id = 7

task = T005:Funktion mit beliebigen vielen Argumenten

group = TC002:Python Grundlagen 1

ordering = 40.0

- - - 

id = 8

task = T006:Indizierung 1

group = TC002:Python Grundlagen 1

ordering = 50.0

- - - 

id = 9

task = T007:Indizierung 2

group = TC002:Python Grundlagen 1

ordering = 60.0

- - - 

- - - - - - - 

- -> Model: Task

id = 1

author = ck

title = Funktions-Aufrufe

versionstring = 1.0

pub_date = 2013-06-16 00:26:50+00:00

body_xml = <?xml version="1.0"?>
<data>
    <txt>
        Gegeben sei der Quelltext:
    </txt>
    <src>
def func(a = 5, b = 7):
    print a, b        
    </src>
    <txt>
        Ergänzen Sie die von folgenden Funktionsaufrufen erzeugten Ausgaben
    </txt>
    <input_list>
        <element>
            <src>func()</src><le len="10"/><sol>5 7</sol>
        </element>
        <element>
            <src>func(3)</src><le len="10"/><sol>3 7</sol>
        </element>
        <element>
            <src>func(3, 'test')</src><le len="10"/><sol>3 test</sol>
        </element>
    </input_list>
    <txt>
        <b>Hinweis:</b> siehe Kurs02 (Funktionen)
    </txt>
</data>

tag_list = beta,basics

- - - 

id = 2

author = ck

title = Funktions-Aufrufe (Wdh.)

versionstring = 1.0

pub_date = 2013-06-16 09:15:13+00:00

body_xml = <?xml version="1.0"?>
<data>
    <txt>
        Gegeben sei der Quelltext:
    </txt>
    <src>
def func(a = 8, b = 7):
    print a, b        
    </src>
    <txt>
        Ergaenzen Sie die von folgenden Funktionsaufrufen erzeugten Ausgaben
    </txt>
    <input_list>
        <element>
            <src>func()</src><le len="10"/><sol>8 7</sol>
        </element>
        <element>
            <src>func(3)</src><le len="10"/><sol>3 7</sol>
        </element>
        <element>
            <src>func(3, 'test')</src><le len="10"/><sol>3 test</sol>
        </element>
    </input_list>
    <txt>
        <b>Hinweis:</b> siehe Kurs02 (Funktionen)
    </txt>
</data>

tag_list = beta,functions

- - - 

id = 3

author = ck

title = Typ-Umwandlung 

versionstring = 1.0

pub_date = 2013-07-07 13:45:05+00:00

body_xml = <?xml version="1.0"?>
<data>
    <txt>
        Vervollständigen Sie folgenden Quelltext mit zwei geeigneten Typumwandlungen, sodass die Ausgabe am Ende lautet: <TT>101</TT>
    </txt>
    <src>
a=10
b=1
    </src>
    <input_list>
        <element>
            <le len="10"/><sol>a=str(a)</sol>
        </element>
        <element>
          <le len="10"/><sol>b=str(b)</sol>
        </element>
    </input_list>
    <src>
print a + b # -> 101
    </src>
</data>

tag_list = basics,beta

- - - 

id = 4

author = ck

title = Syntax-Fehler

versionstring = 1.0

pub_date = 2013-07-07 14:12:16+00:00

body_xml = <?xml version="1.0"?>
<data>
    <txt>
Die folgenden Code-Schnipsel enthalten zum Teil <i>Syntax</i>-Fehler. Korrigieren Sie ggf. den Quelltext (nur die fehlerhafte Zeile). Wenn kein Fehler vorliegen sollte, so lassen Sie das Eingabefeld leer.
    </txt>
<input_list>
        <element>
    <src>
def schöneFunktion(a):
    return 2*a 
    </src>
<le len="10"/><sol>def schoeneFunktion(a):</sol>
    </element>

        <element>
    <src>
if a=b: print "gleich"
    </src>
<le len="10"/><sol>if a==b: print "gleich"</sol>
    </element>

        <element>
    <src>
a, b, c = b, c, a 
    </src>
<le len="10"/><sol></sol>
    </element>
    </input_list>
</data>

tag_list = beta,basics

- - - 

id = 5

author = ck

title = Funktion mit beliebigen vielen Argumenten

versionstring = 1.0

pub_date = 2013-07-08 07:09:07+00:00

body_xml = <?xml version="1.0"?>
<data>
    <txt>
Schreiben Sie eine Funktion namens func1, die beliebig viele (unbenannte) Argumente empfangen kann nichts tut und nichts zurückgibt.
<br><br>
<b>Hinweise:</b> Die Muster-Lösung hat zwei Zeilen und verwendet vier Leerzeichen pro Einrückungsebene.
    </txt>
    <input_list>
        <element>
            <le len="10"/><sol>def func1(*args):</sol>
        </element>
        <element>
            <le len="10"/><sol>    pass</sol>
        </element>
    </input_list>
</data>

tag_list = beta, basics

- - - 

id = 6

author = ck

title = Indizierung 1

versionstring = 1.0

pub_date = 2013-07-08 07:56:34+00:00

body_xml = <?xml version="1.0"?>
<data>
    <txt>
        Ergänzen Sie jeweils das Ergebnis folgender Code-Zeilen.
<br><br>
<b>Hinweise:</b> Beispiel-Liste: <tt>[8,9,10]</tt>, Beispiel-String: <tt>"xyz"</tt> (inkl. "-Zeichen)
    </txt>
    <input_list>
        <element>
            <src>range(3)</src><le len="10"/><sol>[0,1,2]</sol>
        </element>
        <element>
            <src>"Hallo Welement"[1]</src><le len="10"/><sol>"a"</sol>
        </element>
        <element>
            <src>"Hallo Welement"[:4]</src><le len="10"/><sol>"Hall"</sol>
        </element>
        <element>
            <src>"Hallo Welement"[-3]</src><le len="10"/><sol>"e"</sol>
        </element>
        <element>
            <src>"Hallo Welement"[-3:]</src><le len="10"/><sol>"element"</sol>
        </element>
        <element>
            <src>"Hallo Welement"[1:5]</src><le len="10"/><sol>"allo"</sol>
        </element>
    </input_list>
</data>

tag_list = beta, basics

- - - 

id = 7

author = ck

title = Indizierung 2

versionstring = 1.0

pub_date = 2013-07-08 07:57:24+00:00

body_xml = <?xml version="1.0"?>
<data>
    <txt>
        Ergänzen sie jeweils das Ergebnis folgender Code-Zeilen (ohne Leerzeichen).
<br><br>
<b>Hinweise:</b> Beispiel-Liste: <tt>[8,9,10]</tt>, Beispiel-String: <tt>"Hallo Welement"</tt>, Beispiel-Bool: <tt>False</tt>
    </txt>
    <input_list>
        <element>
            <src>[1,5]*3</src><le len="10"/><sol>[1,5,1,5,1,5]</sol>
        </element>
        <element>
            <src>"-"*3</src><le len="10"/><sol>"---"</sol>
        </element>
        <element>
            <src>"abc" == 'abc'</src><le len="10"/><sol>True</sol>
        </element>
        <element>
            <src>8 in range(10)</src><le len="10"/><sol>True</sol>
        </element>
        <element>
            <src>"all" in 'Hallo'</src><le len="10"/><sol>True</sol>
        </element>
        <element>
            <src>"g" not in "[a-z]" </src><le len="10"/><sol>True</sol>
        </element>
    </input_list>
</data>

tag_list = beta, basics

- - - 

id = 8

author = ck

title = cbox_test

versionstring = 1.0

pub_date = 2013-07-08 21:40:32+00:00

body_xml = <?xml version="1.0"?>
<data>
    <txt>
        Richtig oder Falsch?
<br><br>
<b>Hinweise:</b> Denken Sie nach!
    </txt>
    <input_list>
        <element>
            <src>[1,5]*3</src><le len="10"/><sol>[1,5,1,5,1,5]</sol>
        </element>
        <element>
            <src>[1,5]***3</src><cbox label='Richtig?'/><sol>False</sol>
        </element>
    </input_list>
</data>

tag_list = test

- - - 

- - - - - - - 

- -> Model: TaskCollection

id = 1

author = ck

title = Test1

- - - 

id = 2

author = ck

title = Python Grundlagen 1

- - - 

- - - - - - - 

- 