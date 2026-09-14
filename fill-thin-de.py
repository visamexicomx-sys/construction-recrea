# -*- coding: utf-8 -*-
"""Erweitert dünne DE-Blogartikel um zwei substanzielle Abschnitte."""
import re, sys

C = {}

C['hausrenovierung-playa-del-carmen'] = [
("Was die Bausubstanz in Playa wirklich kostet",
"""<p>Der Posten, der in Playa del Carmen fast jede Renovierungskalkulation sprengt, steht in keinem Angebot: die Substanz hinter dem Putz. Häuser aus den Jahren 2005–2014 wurden im Boom schnell gebaut, oft mit unterdimensionierter Bewehrung und ohne saubere Abdichtung der Flachdächer. Wenn wir eine Wohnung im Erdgeschoss öffnen, finden wir in etwa vier von zehn Fällen Salpeterschäden am Mauerfuß (<em>salitre</em>) und korrodierte Bewehrungseisen an den Balkonunterseiten.</p>
<p>Kalkulieren Sie deshalb realistisch in zwei Schichten. Die sichtbare Renovierung — Küche, Bäder, Böden, Anstrich — lässt sich vorab ziemlich genau beziffern. Für die unsichtbare Schicht sollten Sie eine Rücklage von 15 bis 20 Prozent der Bausumme einplanen. Diese Rücklage deckt typischerweise:</p>
<ul>
<li><strong>Bewehrungssanierung:</strong> Rost abtragen, passivieren, mit Reparaturmörtel neu aufbauen — 900 bis 1.600 MXN pro Laufmeter Balkonkante.</li>
<li><strong>Dachabdichtung:</strong> alte Acryl-Schichten komplett runter, Kehlen neu ausbilden, Elastomerbahn plus Schutzanstrich — 450 bis 750 MXN/m².</li>
<li><strong>Elektrik:</strong> Häuser vor 2012 haben selten einen echten Schutzleiter. Eine Nachrüstung nach NOM-001-SEDE kostet bei 120 m² rund 45.000 bis 80.000 MXN.</li>
<li><strong>Abwasser:</strong> PVC-Fallrohre mit zu geringem Gefälle sind der Klassiker hinter wiederkehrendem Geruch im Bad.</li>
</ul>
<p>Unser Rat: Lassen Sie vor der Vertragsunterzeichnung ein einstündiges Aufmaß mit Feuchtemessgerät und Bewehrungssuchgerät machen. Diese Stunde verschiebt das Budget in 80 Prozent der Fälle — aber vor dem Kauf, nicht mittendrin.</p>"""),
("Reihenfolge der Gewerke: warum die meisten Renovierungen zu spät fertig werden",
"""<p>Renovierungen in der Riviera Maya scheitern selten am Geld und fast immer an der Reihenfolge. Die Feuchtigkeit diktiert den Takt: Estrich, Putz und Fliesenkleber brauchen hier länger zum Durchtrocknen als in Europa, weil die Umgebungsluft im Sommer 80 Prozent relative Feuchte hat. Wer Parkett oder Vinyl auf einen Estrich legt, der nur nach Gefühl trocken ist, holt sich Beulen — im Juni oft schon nach vier Wochen.</p>
<p>Die Reihenfolge, mit der wir arbeiten:</p>
<ol>
<li><strong>Abbruch und Entsorgung</strong> (1–2 Wochen). Container sind in Playa knapp; ohne Vorbestellung steht der Schutt im Treppenhaus.</li>
<li><strong>Rohinstallation</strong> Wasser, Abwasser, Elektro, Klimaleitungen (2–3 Wochen). Alles schlitzen, bevor irgendetwas verputzt wird.</li>
<li><strong>Abdichtung Nassbereiche und Dach</strong> (1 Woche), danach 72 Stunden Wasserprobe im Bad. Ohne diesen Test kein Fliesenkleber.</li>
<li><strong>Putz und Estrich</strong> (2 Wochen), anschließend Feuchtemessung: unter 4 Prozent CM-Wert, sonst wird gewartet.</li>
<li><strong>Fliesen, Schreiner, Sanitär</strong> (3–4 Wochen). Küchen aus lokaler Fertigung brauchen vier bis sechs Wochen Vorlauf — Maß nehmen, sobald der Putz steht.</li>
<li><strong>Malerarbeiten und Feinmontage</strong> (1–2 Wochen).</li>
</ol>
<p>Für eine komplette 100-m²-Wohnung ergibt das zehn bis vierzehn Wochen bei durchgehender Besetzung. Angebote mit sechs Wochen sind in aller Regel Angebote ohne Trocknungszeiten — der Preis dafür wird ein Jahr später fällig.</p>""")]

C['dachterrasse-playa-del-carmen'] = [
("Statik: was Ihre bestehende Decke tatsächlich trägt",
"""<p>Die erste Frage bei jedem Rooftop-Projekt in Playa del Carmen ist nicht die Gestaltung, sondern die Reserve der bestehenden Decke. Die meisten Häuser hier haben eine <em>losa de vigueta y bovedilla</em> — Fertigbalken mit Füllkörpern — die für eine Nutzlast von 190 bis 250 kg/m² ausgelegt wurde. Eine begehbare Terrasse mit Fliesenaufbau, Möbeln und Menschen liegt bei etwa 300 kg/m². Ein Whirlpool für vier Personen bringt gefüllt 1.400 bis 1.900 kg auf zwei Quadratmeter — das Vierfache dessen, wofür die Decke gerechnet wurde.</p>
<p>Deshalb steht bei uns am Anfang immer ein Statiknachweis durch einen <em>Director Responsable de Obra</em>. Er kostet 8.000 bis 18.000 MXN und liefert drei mögliche Ergebnisse: die Decke trägt wie sie ist, sie trägt mit punktueller Verstärkung (Stahlträger unter dem Lastbereich, 25.000–60.000 MXN), oder die Lasten müssen über eine eigene Unterkonstruktion bis auf das Fundament geführt werden. Nur der dritte Fall ist wirklich teuer — und genau der wird von Anbietern ohne Statiker regelmäßig übersehen.</p>
<p>Ein praktischer Hinweis zum Gewicht: Ein Pool auf dem Dach ist fast immer machbar, wenn er von Anfang an in den Rohbau gerechnet wurde, und fast nie sinnvoll nachzurüsten. Ein <em>plunge pool</em> aus GFK mit 1,20 m Tiefe wiegt gefüllt so viel wie ein Kleinwagen pro Quadratmeter.</p>"""),
("Materialien, die die Sonne von Playa überleben",
"""<p>Auf einer Dachterrasse addieren sich UV-Strahlung, Salzluft und Temperaturwechsel von 25 Grad zwischen Nacht und Mittag. Materialien, die im Innenhof zehn Jahre halten, sind oben nach zwei Saisons erledigt. Was sich bei uns bewährt hat:</p>
<ul>
<li><strong>Boden:</strong> durchgefärbtes Feinsteinzeug R11 in hellen Tönen, verlegt auf Stelzlagern oder im Dickbett mit Bewegungsfugen alle drei Meter. Dunkle Fliesen erreichen mittags 65 °C und sind barfuß unbenutzbar.</li>
<li><strong>Geländer:</strong> Edelstahl 316 (nicht 304) oder pulverbeschichtetes Aluminium. Normaler Baustahl verliert hier in Meernähe innerhalb von zwei Jahren die Beschichtung.</li>
<li><strong>Beschattung:</strong> eine <em>palapa</em> aus Chit-Palme hält 8 bis 12 Jahre und kühlt spürbar besser als jedes Segel; Sonnensegel aus HDPE halten drei bis vier Jahre und müssen bei Hurrikanwarnung abgenommen werden.</li>
<li><strong>Möbel:</strong> Teak, Polypropylen-Geflecht oder pulverbeschichtetes Aluminium. Alles mit Eisenkern rostet durch, auch wenn es lackiert ist.</li>
<li><strong>Beleuchtung:</strong> ausschließlich IP65 aufwärts, 12 V, mit Trafo im Innenbereich. Warmes Licht unter 2.700 K, in Küstennähe wegen der Schildkrötensaison ohnehin Pflicht.</li>
</ul>
<p>Und das Wichtigste: Jede Durchdringung der Abdichtung — für Geländerpfosten, Pergola-Füße, Leitungen — ist eine potenzielle Leckstelle. Wir setzen Geländer deshalb wo immer möglich seitlich an die Attika statt durch die Fläche.</p>""")]

C['renovierung-roi-playa-del-carmen'] = [
("Welche Renovierungen sich beim Wiederverkauf nicht rechnen",
"""<p>Über den ROI einzelner Maßnahmen wird viel geschrieben — über die Maßnahmen, die Geld vernichten, fast nie. Nach rund hundert Renovierungen in Playa del Carmen und Umgebung ist unsere Liste ziemlich stabil:</p>
<ul>
<li><strong>Hochwertige Einbauküche im Mietobjekt:</strong> Eine Küche für 350.000 MXN erhöht in einer Airbnb-Wohnung weder die Nachtrate noch den Verkaufspreis messbar. Gäste bewerten Klimaanlage, Wasserdruck und WLAN — nicht die Arbeitsplatte.</li>
<li><strong>Whirlpool auf der Terrasse:</strong> hohe Anschaffung, hohe Wartung, und für Käufer oft ein Minus, weil sie die Folgekosten sehen.</li>
<li><strong>Sehr persönliche Gestaltung:</strong> farbige Zementfliesen, aufwendige Wandgestaltung, Mosaikbäder. Was Sie lieben, muss der nächste Käufer mit einkalkulieren, um es zu entfernen.</li>
<li><strong>Zusammenlegen von Schlafzimmern:</strong> Der Quadratmeterpreis steigt nicht, aber die Vermietbarkeit sinkt — drei Schlafzimmer vermieten sich in Playa deutlich besser als zwei große.</li>
</ul>
<p>Umgekehrt zahlen sich unspektakuläre Dinge am zuverlässigsten aus: eine funktionierende Dachabdichtung, Inverter-Klimageräte, ein Boiler mit ausreichender Leistung, eine saubere Elektrik mit FI-Schutzschalter und neue Fenster mit dichten Anschlägen. Diese Posten erhöhen zwar nicht den Angebotspreis, aber sie verhindern die Preisverhandlung von 8 bis 12 Prozent, die nach jeder Kaufprüfung kommt.</p>"""),
("Rechnen Sie in Netto-ROI, nicht in Bruttowertsteigerung",
"""<p>Die verbreitete ROI-Rechnung lautet: Renovierung 600.000 MXN, Wertsteigerung 900.000 MXN, also 50 Prozent Rendite. In Mexiko fehlen in dieser Rechnung mindestens vier Positionen.</p>
<p><strong>ISR beim Verkauf.</strong> Als Nicht-Resident zahlen Sie auf den Veräußerungsgewinn 25 Prozent auf den Bruttopreis oder 35 Prozent auf den Gewinn — je nachdem, was Sie wählen können. Renovierungskosten mindern den Gewinn nur, wenn Sie <em>facturas</em> mit Ihrer RFC und CFDI-Beleg haben. Bar bezahlte Handwerkerleistungen existieren steuerlich nicht.</p>
<p><strong>Maklerprovision.</strong> In der Riviera Maya sind 5 bis 7 Prozent plus IVA üblich, deutlich mehr als in Europa.</p>
<p><strong>Leerstand während der Bauzeit.</strong> Drei Monate Renovierung in einer Wohnung, die 35.000 MXN netto im Monat bringt, kosten 105.000 MXN entgangene Miete — ein Sechstel eines typischen Renovierungsbudgets.</p>
<p><strong>Kapitalbindung.</strong> Zwischen Baubeginn und Verkaufsabschluss liegen in der Praxis 9 bis 18 Monate.</p>
<p>Rechnen Sie deshalb so: Bruttowertsteigerung minus ISR, minus Provision, minus entgangene Miete, geteilt durch die tatsächliche Haltedauer. Aus den plakativen 50 Prozent werden dann meist 12 bis 18 Prozent jährlich — immer noch gut, aber eine andere Entscheidungsgrundlage. Wer nicht verkaufen, sondern vermieten will, rechnet ohnehin sinnvoller über die Steigerung der Nettomiete pro investiertem Peso.</p>""")]

C['gewerbebau-cancun-riviera-maya'] = [
("Betriebsgenehmigung und COFEPRIS: der Pfad neben dem Bauantrag",
"""<p>Beim Gewerbebau in Cancún laufen zwei Genehmigungsstränge parallel, und der zweite wird regelmäßig unterschätzt. Der erste ist die <em>licencia de construcción</em> beim Municipio — Statik, Brandschutz, Stellplätze, Nutzungsart. Der zweite ist alles, was Sie brauchen, um den fertigen Raum anschließend <em>betreiben</em> zu dürfen.</p>
<p>Für Gastronomie, Kliniken, Apotheken, Schönheitssalons und alles mit Lebensmittel- oder Körperkontakt ist das COFEPRIS-Verfahren maßgeblich, ergänzt durch die kommunale <em>licencia de funcionamiento</em>, das Brandschutzgutachten der <em>Protección Civil</em> und — bei Ableitung in die Kanalisation — eine Einleitgenehmigung von CONAGUA oder Aguakan. Jedes dieser Verfahren hat eigene bauliche Anforderungen:</p>
<ul>
<li>Fettabscheider mit definierter Dimensionierung vor dem Küchenanschluss;</li>
<li>abwaschbare Oberflächen bis 1,80 m Höhe, Hohlkehlsockel, kein offenes Holz in Zubereitungsbereichen;</li>
<li>getrennte Wege für Anlieferung und Abfall;</li>
<li>Fluchtwegbreiten und Panikbeschläge nach Personenzahl;</li>
<li>bei medizinischer Nutzung ein RPBI-Lagerraum für gefährliche Abfälle mit eigenem Zugang.</li>
</ul>
<p>Wer diese Punkte erst nach dem Innenausbau einplant, baut zweimal. Wir ziehen den Betreiber-Genehmigungspfad deshalb in die Entwurfsphase vor — spätestens wenn der Grundriss steht, nicht wenn die Fliesen liegen. Für ein mittleres Restaurant rechnen Sie mit drei bis fünf Monaten für den kompletten Genehmigungsblock, parallel zum Rohbau.</p>"""),
("Mietfläche im Einkaufszentrum: was der Vermieter stellt und was nicht",
"""<p>Ein großer Teil des Gewerbebaus in Cancún ist Innenausbau in bestehenden Zentren — La Isla, Las Américas, Malecón Américas, Plaza Hollywood und die Hotelzone. Dort entscheidet die Übergabeform über Ihr Budget, und die Begriffe werden oft unscharf verwendet:</p>
<ul>
<li><strong>Obra gris / shell:</strong> Rohbetonboden, keine Decke, ein Stromanschluss an der Grundstücksgrenze, kein Wasser im Laden. Innenausbau ab etwa 9.000 MXN/m².</li>
<li><strong>Obra blanca:</strong> Estrich, geputzte Wände, Elektro-Unterverteilung, Wasser und Abwasser im Raum, oft eine Grundbeleuchtung. Ausbau ab etwa 5.500 MXN/m².</li>
<li><strong>Llave en mano:</strong> nutzungsfertig, kommt im Einzelhandel praktisch nur bei Nachmietern vor.</li>
</ul>
<p>Drei Punkte, die vor der Unterschrift geklärt gehören: Wie viel <strong>Anschlussleistung in kW</strong> ist der Fläche zugeordnet? Ein Restaurant mit Kühlung und Klimaanlage braucht schnell 40 bis 60 kW; Nachrüstung über den Hausanschluss kostet sechsstellig. Gibt es eine <strong>Abluftführung bis übers Dach</strong>, und darf sie genutzt werden? Und wie lauten die <strong>Ausbauvorschriften</strong> des Centers zu Fassade, Beschilderung, Arbeitszeiten und Anlieferung — in vielen Zentren darf nur zwischen 23 und 7 Uhr gearbeitet werden, was die Bauzeit fast verdoppelt.</p>""")]

C['kleines-haus-tulum-budget'] = [
("Wo Sie beim kleinen Haus sparen dürfen — und wo nicht",
"""<p>Bei einem Budgethaus in Tulum entscheidet nicht die Quadratmeterzahl über die Gesamtkosten, sondern die Verteilung. Zwei Häuser mit je 90 m² können sich im Preis um 40 Prozent unterscheiden, ohne dass man den Unterschied auf dem Grundriss sieht.</p>
<p><strong>Sinnvoll gespart wird bei:</strong> der Anzahl der Bäder (jedes zusätzliche Bad kostet 90.000 bis 160.000 MXN allein an Installation), der Grundrissform (ein Rechteck braucht weniger Fundament und weniger Dachkante als ein L), der Deckenhöhe im Nebenraum, polierten Betonböden statt Fliesen, Fertigschränken statt Schreinerarbeit und einer Küche, die an einer einzigen Wand entlangläuft.</p>
<p><strong>Nicht gespart wird bei:</strong></p>
<ul>
<li><strong>Fundament und Baugrund.</strong> Der Karst in Tulum ist launisch; ein Hohlraum unter der Bodenplatte ist kein theoretisches Risiko. Eine Baugrunduntersuchung für 12.000 bis 25.000 MXN ist bei jedem Budget Pflicht.</li>
<li><strong>Dachabdichtung.</strong> Der günstigste Posten mit den teuersten Folgen.</li>
<li><strong>Abwasser.</strong> Ein ordentlicher Biodigestor mit Sickerfeld statt einer gemauerten Grube — in einer Karstregion über dem Trinkwasser ist das keine Komfortfrage.</li>
<li><strong>Fenster.</strong> Billige Aluminiumrahmen ohne echte Dichtung lassen Regen und Insekten durch und machen die Klimaanlage sinnlos.</li>
<li><strong>Elektrik.</strong> Kabelquerschnitte und Schutzleiter nach NOM-001-SEDE.</li>
</ul>
<p>Die Faustregel, die sich bei uns bewährt hat: Sparen Sie an dem, was Sie später mit überschaubarem Aufwand austauschen können. Alles, wofür man Beton aufstemmen müsste, wird beim ersten Mal richtig gemacht.</p>"""),
("Bauen in Etappen: der realistische Weg mit begrenztem Budget",
"""<p>Viele unserer Kunden in Tulum bauen nicht ein Haus, sondern die erste Hälfte davon. Das funktioniert gut, wenn die Erweiterung von Anfang an konstruktiv vorbereitet ist — und schlecht, wenn sie später improvisiert wird.</p>
<p>Was Sie in Etappe eins mitbauen sollten, auch wenn Sie es noch nicht nutzen:</p>
<ul>
<li><strong>Fundament und Stützen für den späteren Anbau.</strong> Nachträglich gegründete Anbauten setzen sich anders als der Bestand; der Riss in der Anschlussfuge ist dann vorprogrammiert.</li>
<li><strong>Bewehrungsanschlüsse aus der Decke</strong> (<em>bastones</em>), falls ein Obergeschoss kommen soll — inklusive Schutz gegen Korrosion, solange sie freiliegen.</li>
<li><strong>Leerrohre</strong> für Strom, Wasser, Abwasser und Datenleitungen bis zur Grenze der ersten Etappe.</li>
<li><strong>Zisterne und Hausanschluss</strong> in Endgröße. Eine zweite Zisterne kostet mehr als eine größere erste.</li>
<li><strong>Unterverteilung mit freien Plätzen</strong> und ausreichend dimensioniertem Hauptkabel.</li>
</ul>
<p>Der Mehraufwand für diese Vorbereitung liegt bei 6 bis 10 Prozent der Kosten von Etappe eins. Ohne sie kostet die zweite Etappe erfahrungsgemäß 25 bis 35 Prozent mehr, weil Bestand geöffnet, gestützt und wiederhergestellt werden muss — und weil man in einem bewohnten Haus baut, nicht auf einer freien Baustelle.</p>""")]

C['smart-home-tropen-riviera-maya'] = [
("Funkstandards, die im Stahlbetonhaus tatsächlich funktionieren",
"""<p>Mexikanische Häuser sind aus Betonhohlblock und Stahlbeton gebaut, häufig mit Bewehrungsmatten in Wänden und Decken. Das ist bauphysikalisch sinnvoll und funktechnisch eine Katastrophe: Eine 15 cm starke bewehrte Decke dämpft ein 2,4-GHz-Signal so stark, dass ein Repeater eine Etage tiefer praktisch nichts mehr empfängt. Wer ein Smart-Home-System nach europäischem Vorbild plant, wundert sich hier über Geräte, die „manchmal" reagieren.</p>
<p>Was in der Praxis funktioniert:</p>
<ul>
<li><strong>Zigbee oder Z-Wave mit Mesh:</strong> Jedes netzbetriebene Gerät — Schalter, Steckdose, Lampe — ist ein Repeater. Planen Sie mindestens ein netzbetriebenes Gerät pro Raum, dann trägt das Netz sich selbst.</li>
<li><strong>Ein Access Point pro Etage</strong>, per Kabel angebunden, nicht per WLAN-Repeater. Ein einziges Cat-6-Kabel im Rohbau löst mehr Probleme als jedes Mesh-System später.</li>
<li><strong>Kabelgebundene Bussysteme (KNX)</strong> lohnen sich in der Riviera Maya vor allem bei Villen über 400 m², wo Ausfallsicherheit wichtiger ist als die Anschaffung.</li>
<li><strong>Lokale Steuerung vor Cloud.</strong> Bei Internetausfall — in der Regenzeit keine Seltenheit — muss das Licht trotzdem angehen. Systeme mit lokalem Hub sind hier klar im Vorteil.</li>
</ul>
<p>Der billigste Zeitpunkt für all das ist die Rohbauphase. Leerrohre zu den Decken, zur Eingangstür, zum Tor und zum Poolbereich kosten während des Baus wenige Tausend Pesos; nachträglich bedeutet jede Leitung einen Schlitz in bewehrtem Beton.</p>"""),
("Was in der Salzluft ausfällt und wie man es verhindert",
"""<p>Küstennah ist nicht die Feuchtigkeit das Hauptproblem, sondern das Salz, das mit ihr transportiert wird. Es lagert sich auf Platinen ab, zieht Wasser an und bildet leitfähige Brücken. Typische Ausfallzeiten ungeschützter Elektronik in 300 m Entfernung zum Meer: Außenkameras 18 bis 30 Monate, Torantriebe 2 bis 4 Jahre, Außensteckdosen mit einfachem Klappdeckel unter einem Jahr.</p>
<p>Die Gegenmaßnahmen sind unspektakulär, aber wirksam:</p>
<ul>
<li><strong>Schutzart mindestens IP65</strong> für alles im Freien, IP66 in Sichtweite des Meeres — und zwar auch für die Verteilerdose, nicht nur für das Gerät.</li>
<li><strong>Gehäuse aus Polycarbonat oder Edelstahl 316</strong>, nie aus lackiertem Stahl oder Aluminium mit Eisenschrauben.</li>
<li><strong>Conformal Coating</strong> auf Platinen, die dauerhaft draußen bleiben — viele Hersteller bieten eine Marineausführung an, die den Aufpreis wert ist.</li>
<li><strong>Hub, Router und NVR im Innenraum</strong> mit Klimatisierung; nach draußen geht nur, was dort hin muss.</li>
<li><strong>Überspannungsschutz</strong> an der Hauptverteilung und am Datenschrank. Gewitter in der Regenzeit erledigen mehr Smart-Home-Technik als Salz und Feuchte zusammen.</li>
<li><strong>USV für Hub und Router</strong>, 30 bis 60 Minuten Überbrückung. Die kurzen CFE-Ausfälle sind zahlreicher als die langen.</li>
</ul>
<p>Und einmal jährlich: Außengehäuse mit Süßwasser abspülen, Dichtungen prüfen, Trockenmittelbeutel tauschen. Eine Stunde Wartung verlängert die Standzeit erfahrungsgemäß um Jahre.</p>""")]

C['bauunternehmen-waehlen-riviera-maya'] = [
("Welche Unterlagen ein seriöser Anbieter vor Vertragsschluss vorlegt",
"""<p>In Quintana Roo darf sich praktisch jeder Bauunternehmer nennen. Die Trennung zwischen seriösen Firmen und improvisierten Teams läuft deshalb nicht über die Website, sondern über Papiere, die vor der ersten Zahlung auf dem Tisch liegen sollten:</p>
<ul>
<li><strong>Constancia de Situación Fiscal</strong> mit aktueller RFC. Ohne sie gibt es keine <em>factura</em> — und ohne <em>facturas</em> können Sie Baukosten beim späteren Verkauf nicht gegen die Kapitalertragsteuer stellen.</li>
<li><strong>IMSS-Registrierung der Arbeiter.</strong> Bei einem Arbeitsunfall auf nicht versicherter Baustelle haftet in Mexiko der Grundstückseigentümer mit. Lassen Sie sich monatlich die <em>opinión de cumplimiento</em> zeigen.</li>
<li><strong>Der DRO mit Nummer.</strong> Der <em>Director Responsable de Obra</em> unterschreibt die Genehmigung persönlich. Fragen Sie nach Name und Registernummer, nicht nach „unser Architekt".</li>
<li><strong>Haftpflicht- und Bauleistungsversicherung</strong> mit Police und Deckungssumme, nicht als Zusage.</li>
<li><strong>Drei Referenzen der letzten zwei Jahre</strong> mit Adresse — und zwar fertiggestellte Projekte, keine Renderings.</li>
</ul>
<p>Ein Anbieter, der diese fünf Punkte innerhalb von 48 Stunden liefert, hat die Grundhygiene. Einer, der ausweicht oder um Vertrauen bittet, hat sie nicht — unabhängig davon, wie überzeugend die Referenzfotos aussehen.</p>"""),
("Die Vertragsstruktur, die Sie vor Nachträgen schützt",
"""<p>Die meisten Konflikte am Bau in der Riviera Maya entstehen nicht aus bösem Willen, sondern aus einem Angebot, das auf zwei Seiten passt. Ein belastbarer Vertrag enthält vier Elemente:</p>
<p><strong>1. Ein Leistungsverzeichnis nach Positionen</strong> (<em>catálogo de conceptos</em>) mit Mengen, Einheiten und Einheitspreisen — nicht eine Pauschale „Haus schlüsselfertig". Nur so lässt sich später prüfen, ob ein Nachtrag eine echte Änderung oder eine vergessene Position ist.</p>
<p><strong>2. Zahlungen gegen Baufortschritt</strong>, nicht gegen Kalender. Üblich und fair sind 20 bis 30 Prozent Anzahlung für Material und Baustelleneinrichtung, danach Abschläge gegen abgenommene Etappen: Fundament, Rohbau EG, Decke, Rohinstallation, Putz, Ausbau. Wer 50 Prozent im Voraus verlangt, verlagert sein Liquiditätsrisiko auf Sie.</p>
<p><strong>3. Ein Einbehalt von 5 bis 10 Prozent</strong> (<em>fondo de garantía</em>) für 6 bis 12 Monate nach Übergabe. Das ist der wirksamste Hebel, den Sie bei Mängeln haben — und der Punkt, bei dem sich Anbieter am schnellsten offenbaren.</p>
<p><strong>4. Eine definierte Änderungsprozedur:</strong> jede Abweichung schriftlich, mit Preis und Terminfolge, vor der Ausführung freigegeben. Ohne diese Klausel wird jede mündliche Idee auf der Baustelle später zur Rechnung.</p>
<p>Ergänzen Sie das um eine Liste der verwendeten Marken und Modelle bei Fenstern, Klimageräten, Sanitär und Fliesen. „Gleichwertig" ist in der Praxis das teuerste Wort im gesamten Vertrag.</p>""")]

C['individuelles-hausdesign-playa-del-carmen'] = [
("Klimagerecht entwerfen: Orientierung, Querlüftung, Dachüberstand",
"""<p>Ein individuell geplantes Haus in Playa del Carmen rechnet sich vor allem über den Betrieb. Zwei Häuser gleicher Größe unterscheiden sich in der Stromrechnung um den Faktor zwei, je nachdem, wie sie zur Sonne stehen. Die Entwurfsentscheidungen mit der größten Wirkung kosten im Bau fast nichts:</p>
<ul>
<li><strong>Orientierung:</strong> Die lange Fassade nach Norden und Süden, die kurzen Seiten nach Osten und Westen. Die Westfassade nimmt hier zwischen 15 und 18 Uhr die größte Last auf — je weniger Glas dort, desto kleiner die Klimaanlage.</li>
<li><strong>Dachüberstand:</strong> 80 bis 120 cm auf der Südseite halten die Mittagssonne aus dem Raum und lassen die flachere Wintersonne herein. Ein Überstand ist billiger als jede Verglasung mit Sonnenschutzbeschichtung.</li>
<li><strong>Querlüftung:</strong> Öffnungen auf gegenüberliegenden Seiten jedes Raums, mit der Hauptöffnung zur Ostbrise. Von November bis März braucht ein gut gelüftetes Haus an der Küste kaum Klimatisierung.</li>
<li><strong>Deckenhöhe:</strong> 2,90 bis 3,20 m in den Wohnräumen. Warme Luft sammelt sich oben; ein hoher Raum fühlt sich messbar kühler an.</li>
<li><strong>Helle Dachflächen:</strong> Ein weißer Elastomeranstrich senkt die Oberflächentemperatur der Decke um 20 bis 30 Grad.</li>
</ul>
<p>Verlangen Sie vom Planer eine Sonnenstandsstudie für 21. Juni und 21. Dezember, jeweils 9, 13 und 17 Uhr. Sie kostet einen halben Tag Arbeit und verändert erfahrungsgemäß mindestens eine Grundrissentscheidung.</p>"""),
("Vom Entwurf zur Genehmigung: welche Unterlagen Playa tatsächlich verlangt",
"""<p>Zwischen einem schönen Entwurf und einer Baugenehmigung in Solidaridad liegt ein Satz sehr konkreter Dokumente. Wer sie erst nach dem Entwurf zusammenstellt, plant häufig um. Was gebraucht wird:</p>
<ul>
<li><strong>Constancia de Uso de Suelo</strong> für das Grundstück, mit den zulässigen Werten für COS (bebaute Grundfläche), CUS (Geschossflächenzahl), Geschosszahl und Abstandsflächen. Diese Zahlen sind die eigentliche Vorgabe des Entwurfs.</li>
<li><strong>Alineamiento y número oficial</strong> — die verbindliche Grundstücksgrenze und Hausnummer.</li>
<li><strong>Vollständiges Planpaket:</strong> Architektur, Statik, Elektro, Sanitär, jeweils gestempelt vom <em>Director Responsable de Obra</em>.</li>
<li><strong>Baugrundgutachten</strong> — im Karstboden der Region faktisch immer erforderlich.</li>
<li><strong>Nachweis der Abwasserlösung:</strong> Anschluss an Aguakan oder genehmigte Kleinkläranlage.</li>
<li>In Küstennähe zusätzlich <strong>SEMARNAT/SEMA-Verfahren</strong> und gegebenenfalls eine ZOFEMAT-Konzession für den Bereich zwischen Bebauung und Meer.</li>
</ul>
<p>Realistisch dauert der Genehmigungsblock in Playa del Carmen 6 bis 12 Wochen, in Umweltverfahren deutlich länger. Planen Sie diese Zeit als eigene Projektphase ein — und nutzen Sie sie für Ausschreibung und Materialauswahl, statt sie am Ende auf die Bauzeit zu addieren.</p>""")]

C['hurrikansicheres-bauen-riviera-maya'] = [
("Die Schwachstellen in der Reihenfolge, in der sie versagen",
"""<p>Nach einem Sturm der Kategorie 3 sehen die Schäden in der Riviera Maya erstaunlich gleichförmig aus. Der tragende Stahlbetonrahmen hält fast immer; was versagt, ist die Hülle — und zwar in einer sehr vorhersagbaren Reihenfolge:</p>
<ol>
<li><strong>Ungesicherte Fenster und Türen.</strong> Bricht eine Öffnung, steigt der Innendruck schlagartig und arbeitet gegen das Dach von innen. Fast jeder abgedeckte Dachaufbau beginnt mit einem zerstörten Fenster.</li>
<li><strong>Leichte Vordächer, Carports und Pergolen.</strong> Sie werden angehoben und schlagen dann in Fassade und Verglasung.</li>
<li><strong>Palapas ohne Verankerung.</strong> Das Dach selbst ist erstaunlich robust, die Verbindung zum Fundament oft nicht.</li>
<li><strong>Außengeräte der Klimaanlage</strong> auf einfachen Konsolen.</li>
<li><strong>Dachabdichtung an Kehlen und Aufkantungen</strong>, wo Wasser bei horizontalem Regen von unten unter die Bahn gedrückt wird.</li>
</ol>
<p>Die Konsequenz für den Entwurf: Das Geld für Sturmsicherheit gehört in die Öffnungen, nicht in den Rohbau. Wer bei 150 km/h Fenster und Türen dicht hält, hat den größten Teil des Risikos abgeräumt — und zwar für einen Bruchteil dessen, was eine überdimensionierte Tragstruktur kosten würde.</p>"""),
("Wasser, Strom und Zufahrt: die Tage nach dem Sturm",
"""<p>Sturmsicheres Bauen endet nicht beim Wind. Die eigentliche Belastung beginnt danach: In der Riviera Maya sind nach einem stärkeren Hurrikan drei bis zehn Tage ohne Strom und Wasserdruck normal, in abgelegenen Lagen auch länger. Ein Haus, das darauf ausgelegt ist, kostet im Bau wenig mehr:</p>
<ul>
<li><strong>Zisterne mit mindestens 5.000 Litern</strong> und einem Handentnahmepunkt, der ohne Pumpe funktioniert.</li>
<li><strong>Einspeisepunkt für einen Generator</strong> mit Netzumschalter (<em>transfer switch</em>) in der Hauptverteilung — 12.000 bis 25.000 MXN im Neubau, ein Vielfaches davon als Nachrüstung.</li>
<li><strong>Ein Teil-Solarsystem mit Batterie</strong> für Kühlschrank, Licht, Router und Wasserpumpe. Kein Inselsystem für das ganze Haus, sondern ein definierter Notstromkreis.</li>
<li><strong>Höhenlage der Technik:</strong> Verteilung, Pumpe und Wechselrichter mindestens 60 cm über Bodenniveau. Überflutung kommt in der Region öfter vom Starkregen als vom Meer.</li>
<li><strong>Abflüsse mit Rückstauklappe</strong> und großzügig dimensionierte Dachabläufe, plus einen Notüberlauf an der Attika.</li>
<li><strong>Zufahrt und Bepflanzung:</strong> keine großen Bäume in Fallrichtung des Hauses, Palmen regelmäßig auslichten.</li>
</ul>
<p>Wir planen diese Punkte standardmäßig mit und dokumentieren sie in einer Übergabemappe: wo der Hauptschalter sitzt, wie die Sturmläden montiert werden, wo der Generator angeschlossen wird. Im Ernstfall ist diese Mappe mehr wert als jedes zusätzliche Detail an der Fassade.</p>""")]

C['luxusvilla-baukosten-tulum'] = [
("Wo das Geld in einer Luxusvilla wirklich hingeht",
"""<p>Die Preisspanne für Luxusvillen in Tulum reicht von 28.000 bis über 60.000 MXN pro Quadratmeter — und die Differenz liegt selten dort, wo Bauherren sie vermuten. Der Rohbau ist auch im oberen Segment relativ preisstabil; was den Preis verdoppelt, sind fünf Posten:</p>
<ul>
<li><strong>Geometrie.</strong> Gekrümmte Wände, auskragende Decken, Sichtbetonoberflächen und doppelgeschossige Räume vervielfachen den Schalungsaufwand. Sichtbeton in Ausführungsqualität kostet das Zwei- bis Dreifache von verputztem Beton, weil jede Naht und jedes Ankerloch geplant sein muss.</li>
<li><strong>Öffnungen.</strong> Großformatige Schiebeanlagen mit Einbaurahmen, thermischer Trennung und Edelstahlbeschlägen für Küstennähe kosten 18.000 bis 40.000 MXN pro Quadratmeter Öffnung — bei 60 m² Glas ist das ein eigenes Budgetkapitel.</li>
<li><strong>Wasserflächen.</strong> Ein Infinity-Pool mit Überlaufrinne, Ausgleichsbecken und Salzelektrolyse liegt beim Doppelten eines konventionellen Beckens gleicher Größe.</li>
<li><strong>Handwerkliche Oberflächen.</strong> Chukum, polierter Kalkstein, Terrazzo vor Ort gegossen, Vollholz-Schreinerei aus Tzalam oder Chechén — alles zeitintensive Handarbeit mit begrenzter Zahl fähiger Teams in der Region.</li>
<li><strong>Haustechnik.</strong> Wasseraufbereitung, Entfeuchtung, Wärmepumpe für den Pool, Notstrom, Gebäudeautomation: zusammen häufig 12 bis 18 Prozent der Bausumme.</li>
</ul>
<p>Wer das Budget steuern will, steuert diese fünf Positionen — nicht die Quadratmeterzahl.</p>"""),
("Grundstück, Umweltauflagen und Erschließung: die Kosten vor dem ersten Beton",
"""<p>In Tulum entscheidet das Grundstück über einen erheblichen Teil der Baukosten, und zwar bevor der erste Kubikmeter Beton geliefert wird. Drei Themen sollten vor dem Kauf geprüft sein:</p>
<p><strong>Umweltstatus.</strong> Liegt die Parzelle in einer Zone mit Mangrove, Cenote, Trockenwald mit Schutzstatus oder innerhalb des Einflussbereichs des Nationalparks, greift ein SEMARNAT-Verfahren (MIA). Das kostet je nach Umfang 150.000 bis 600.000 MXN und dauert 6 bis 14 Monate. Gutachten und Ausgleichsmaßnahmen kommen hinzu. Ein Grundstück ohne geklärten Umweltstatus ist kein günstiges Grundstück, sondern ein unbekanntes.</p>
<p><strong>Erschließung.</strong> Viele Premiumlagen — Region 15, La Veleta, Aldea Zamá-Randlagen, Sian Ka'an-Korridor — haben keinen Netzanschluss von CFE in Grundstücksnähe. Eine Leitungsverlängerung mit Trafostation liegt bei 250.000 bis 900.000 MXN. Ohne Kanalisation ist eine eigene Kläranlage Pflicht, ohne Wasserleitung eine Brunnenbohrung mit Aufbereitung.</p>
<p><strong>Rechtliche Form.</strong> In der Küstenzone (50 km von der Küste) erwerben Ausländer über einen <em>fideicomiso</em> — Einrichtung 25.000 bis 60.000 MXN, jährliche Gebühr 12.000 bis 25.000 MXN — oder über eine mexikanische Gesellschaft. Prüfen Sie zusätzlich, ob das Grundstück je <em>ejido</em>-Land war und ob die Umwandlung vollständig dokumentiert ist.</p>
<p>Diese drei Punkte summieren sich häufig auf 8 bis 15 Prozent des Gesamtprojekts. Sie gehören in die Kalkulation, nicht in die Überraschungen.</p>""")]

ANCHOR = re.compile(r'<h2[^>]*>\s*Häufig')
done = 0
for slug, secs in C.items():
    p = 'blog-de/%s.html' % slug
    h = open(p, encoding='utf-8').read()
    if '<!--deepened-->' in h:
        continue
    m = ANCHOR.search(h)
    if not m:
        print('NO ANCHOR', p); continue
    body = ''.join('<h2 class="mt-4">%s</h2>\n%s\n' % (t, b.strip()) for t, b in secs)
    open(p, 'w', encoding='utf-8').write(h[:m.start()] + '<!--deepened-->' + body + h[m.start():])
    done += 1
print('deepened:', done)
