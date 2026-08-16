#!/usr/bin/env python3
"""Fourth depth pass, batch 3a of 3: the German tail, 29 pages (2026-08-15)."""
import os, re

OPEN, CLOSE = '<div data-depth="2026-08">', '</div><!--/depth-->'


def sec(h, p):
    return '<h2 class="mt-4">%s</h2>\n<p>%s</p>\n' % (h, p)


def tbl(head, rows):
    return ('<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr>'
            + ''.join('<th>%s</th>' % h for h in head) + '</tr></thead><tbody>\n'
            + '\n'.join('<tr>' + ''.join('<td>%s</td>' % c for c in r) + '</tr>' for r in rows)
            + '\n</tbody></table></div>\n')


B = {

'architekten-playa-del-carmen/index.html':
 sec('Was ein vollständiges Projekt enthält',
     'Vorentwurf mit Grundrissen und Volumetrie; Architekturprojekt mit Schnitten, Ansichten und Details; '
     'Ausführungsplanung mit Statik, Sanitär, Elektro und Sonderanlagen; sowie die vom DRO unterzeichneten Unterlagen '
     'für die Genehmigung. Wer die Ausführungsplanung überspringt, zahlt sie später als Nachtrag: Was nicht gezeichnet '
     'ist, wird auf der Baustelle entschieden, und dort ist es teurer.')
 + sec('Für dieses Klima entwerfen, nicht für den Katalog',
     'Ausrichtung und Querlüftung, Sonnenschutz an West- und Südfassaden, großzügige Dachüberstände für Starkregen, '
     'salzbeständige Materialien, sowie Zisterne, Pumpe und Abwasserbehandlung von Anfang an eingeplant. Ein schöner '
     'Plan, der das ignoriert, ergibt ein Haus, das im Betrieb teuer ist.')
 + sec('Honorar und Dauer',
     'In der Riviera Maya üblicherweise 4% bis 8% der Bausumme, je nach Komplexität. Sechs bis zehn Wochen für ein '
     'Einfamilienhaus vom Vorentwurf bis zum unterschriebenen Satz. Wenn dasselbe Unternehmen plant und baut, wird '
     'dieser Anteil meist in den Bauvertrag integriert.'),

'baugenehmigungen-lizenzen-riviera-maya/index.html':
 sec('Die richtige Reihenfolge der Unterlagen',
     'Zuerst die Nutzungsbescheinigung: Lässt das Grundstück Ihr Vorhaben nicht zu, hilft kein Entwurf. Danach '
     'Fluchtlinie und Hausnummer, Erschließungsbestätigung, das vom DRO unterzeichnete Projekt und damit die '
     'Baugenehmigung. Parallel, wo einschlägig, das Umweltverfahren — das in Tulum, Puerto Morelos und nahe '
     'Schutzgebieten den eigentlichen Zeitplan bestimmt.')
 + sec('Warum Anträge zurückkommen',
     'Selten wegen langsamer Behörden, meist weil die Unterlagen unvollständig sind: Pläne, die nicht zur '
     'Nutzungsbescheinigung passen, Dichte oder Höhe über dem Zulässigen, ungelöste Abwasserfrage, DRO-Unterlagen, die '
     'nach allem anderen eintreffen, oder eine deklarierte Fläche, die nicht zur Vermessung passt. Jede Rückgabe setzt '
     'die Uhr zurück.')
 + tbl(['Vorgang', 'Wofür', 'Kosten und Dauer'],
       [['Nutzungsbescheinigung', 'Nutzung, Dichte, GRZ, GFZ, Höhe', '$1,500 – $6,000 MXN · 1–3 Wochen'],
        ['Fluchtlinie und Hausnummer', 'Grenzen und Straßenfront', '$800 – $3,500 MXN · 1–2 Wochen'],
        ['Baugenehmigung mit DRO', 'Genehmigt die Arbeiten', 'Nach Fläche · 3–10 Wochen'],
        ['Umweltverfahren', 'Wo einschlägig', 'Je Projekt · Monate']]),

'bauunternehmen-cancun/index.html':
 sec('Cancún ist nicht ein Markt, sondern drei',
     'In der Hotelzone bestimmen enge Anlieferfenster, strenge Lärmregeln und häufige Bauverbote in der Hochsaison den '
     'Ablauf: Der Terminplan richtet sich nach dem Gebäude, nicht nach den Gewerken. In Puerto Cancún und den neueren '
     'Anlagen prüfen Gestaltungsbeiräte alles, was von außen sichtbar ist. In Cumbres und im Westen findet der meiste '
     'Wohnungsneubau statt, dort sind Verkehr und Zufahrt die Einschränkung.')
 + sec('Die Anlagenordnung schlägt meist die Kommune',
     'Größere Abstände, geringere Höhen, vorgeschriebene Materialien und Farben, Bauzeiten, Kaution und maximale '
     'Bauzeit. Das alles gilt Ihnen gegenüber unabhängig davon, was Benito Juárez erlaubt, und gehört vor den Entwurf '
     'gelesen — nicht nach der kommunalen Genehmigung.')
 + tbl(['Niveau', 'Was es bedeutet', 'Kosten pro m²'],
       [['Einfach', 'Basisausstattung, ohne Pool', '$12,000 – $16,000 MXN'],
        ['Mittel', 'Gute Ausstattung, kleiner Pool', '$17,000 – $24,000 MXN'],
        ['Premium', 'Importmaterialien, großer Pool', '$25,000 – $35,000 MXN']]),

'bauunternehmen-tulum/index.html':
 sec('In Tulum bestimmt das Umweltverfahren den Kalender',
     'Nicht die kommunale Genehmigung entscheidet, wann gebaut wird, sondern das Umweltdossier. Karstboden, '
     'Cenotensysteme und Schutzgebiete verlangen eine detaillierte Begründung für Regenwasserführung, '
     'Abwasserbehandlung und Rückhaltung. Ein vollständiges Dossier läuft; ein unvollständiges wird zurückgegeben und '
     'die Frist beginnt neu.')
 + sec('Der Untergrund und was er im Budget bewirkt',
     'Zerklüfteter Kalkstein, Hohlräume und ein oberflächennaher Grundwasserspiegel. Deshalb können zwei Nachbar'
     'grundstücke sehr unterschiedliche Gründungskosten haben, und deshalb ist das Baugrundgutachten hier kein '
     'Papierkram, sondern das, was verhindert, auf einem Hohlraum zu gründen.')
 + tbl(['Niveau', 'Was es bedeutet', 'Kosten pro m²'],
       [['Mittel', 'Gute Ausstattung, kleiner Pool', '$18,000 – $26,000 MXN'],
        ['Premium', 'Importmaterialien, großer Pool', '$27,000 – $38,000 MXN'],
        ['Designvilla', 'Sonderanfertigungen durchgehend', 'Ab $38,000 MXN']]),

'hausrenovierung-playa-del-carmen/index.html':
 sec('Was fast jede Sanierung hier zutage fördert',
     'Eine Abdichtung am Ende ihrer Lebensdauer, eine Elektroinstallation ohne funktionierende Erdung, und Feuchtigkeit, '
     'die überstrichen statt diagnostiziert wurde. Eine Sanierung, die nur Oberflächen anfasst, lässt alle drei drin und '
     'sieht etwa achtzehn Monate hervorragend aus.')
 + sec('Die richtige Reihenfolge',
     'Aufmaß und Diagnose; Rückbau mit Schutz des Bestands; statische und Abdichtungskorrekturen; Erneuerung der '
     'Haustechnik bei offenen Wänden; danach Oberflächen; dann Einbauten; zuletzt die Mängelliste. Diese Reihenfolge zu '
     'ändern, um schneller ein sichtbares Ergebnis zu bekommen, ist der häufigste Grund für doppelte Arbeit.')
 + tbl(['Umfang', 'Enthält', 'Kosten pro m²'],
       [['Auffrischung', 'Anstrich, Böden, Armaturen', '$4,000 – $8,000 MXN'],
        ['Küche und Bäder', 'Möbel, Fliesen, Sanitär', '$9,000 – $18,000 MXN'],
        ['Komplettsanierung', 'Haustechnik erneuert, alle Oberflächen', '$12,000 – $22,000 MXN']]),

'services/gewerbebau.html':
 sec('Beim Gewerbebau ist der Eröffnungstermin das Budget',
     'Jede Woche Verzug kostet den Betreiber Umsatz, den er genau beziffern kann. Das ändert die Planung: Bestellungen '
     'mit langer Lieferzeit vor dem Rückbau, Gewerke dort überlappt, wo es sicher möglich ist, und Vermieter oder '
     'Centermanagement eingebunden, bevor die erste Kolonne anrückt.')
 + sec('Was wir bauen',
     'Ladenflächen und Mieterausbau, Büros, Restaurants und Küchen mit Abluft, Gas und Fettabscheider, Praxen und '
     'Kliniken, leichte Lagerhallen sowie Markenauftritte in Einkaufszentren. Dazu Komplettumbauten bei laufendem '
     'Betrieb, was in Playa del Carmen und Cancún die Hälfte unserer Anfragen ausmacht.')
 + tbl(['Typ', 'Umfang', 'Kosten pro m²'],
       [['Mieterausbau', 'Oberflächen, Technik, Markenauftritt', '$7,000 – $14,000 MXN'],
        ['Büro', 'Trennwände, Netzwerk, Klima, Akustik', '$10,000 – $20,000 MXN'],
        ['Restaurant', 'Sonderanlagen, Abluft', '$15,000 – $30,000 MXN']]),

'services/metallbau.html':
 sec('Was zuerst korrodiert — nie der sichtbare Stahl',
     'An dieser Küste beginnt der Schaden an Verbindungen und Befestigungen: eine gewöhnlich verzinkte Schraube in '
     'einer Edelstahlkonstruktion, eine nicht gereinigte Schweißnaht, eine Beschichtung über Walzhaut. Das Salz findet '
     'diese Punkte, und der Rost wandert von dort nach außen, während die Oberfläche noch intakt aussieht.')
 + sec('Beschichtungen, die hier halten',
     'Feuerverzinkung mit anschließender Pulverbeschichtung für Außen- und Tragkonstruktionen. Seewasserbeständiger '
     'Edelstahl für Geländer in Strandnähe und alles im Spritzwasserbereich. Pulverbeschichtetes Aluminium für leichtere '
     'Bauteile. Normaler Anstrich auf unbehandeltem Stahl ist eine Zwei-Saisons-Lösung zum Preis einer Einjahreslösung.')
 + tbl(['Position', 'Ausführung', 'Kosten 2026'],
       [['Geländer, pulverbeschichtet', 'Verzinkt und beschichtet', '$1,800 – $3,500 MXN/m'],
        ['Geländer, Marine-Edelstahl', 'Strandlage', '$4,500 – $9,000 MXN/m'],
        ['Schiebetorkonstruktion', 'Bis 4 m, ohne Antrieb', '$25,000 – $60,000 MXN']]),

'blog-de/airbnb-investment-tulum.html':
 sec('Rechnen Sie mit den echten Betriebskosten',
     'Zwischen Bruttobuchungen und dem, was ankommt, liegt mehr, als die meisten Prognosen zeigen. Verwaltung nimmt 15% '
     'bis 30% vom Brutto, Reinigung fällt je Aufenthalt an, Plattformgebühren werden vor der Auszahlung abgezogen, die '
     'Klimaanlage läuft während des Aufenthalts fast durchgehend, dazu Pool, Garten, Nachschub, Versicherung und eine '
     'Instandhaltungsrücklage, die dieses Klima unverzichtbar macht.')
 + sec('Wo das Angebot der Nachfrage vorausgeeilt ist',
     'Kleine Eigentumswohnungen, die über eine Renditeprognose verkauft werden, bilden das am dichtesten besetzte '
     'Segment. Wenn viele nahezu identische Einheiten um denselben Gast konkurrieren, zeigt sich die Anpassung zuerst '
     'in sinkender Auslastung und Rabatten, nicht in fallenden Preisen. Fragen Sie stets, welche Auslastung eine '
     'Prognose unterstellt, und vergleichen Sie mit vergleichbaren Inseraten.')
 + sec('Für die Vermietung bauen, nicht für sich selbst',
     'Warmwasser bei voller Belegung, Klimaanlage nach realer Gästezahl ausgelegt, Oberflächen, die den Wechsel '
     'aushalten, genügend Sitzplätze für die beworbene Kapazität, Stauraum für Wäsche. Das gehört ins Raumprogramm, '
     'nicht in die Auswertung der ersten Bewertungen.'),

'blog-de/auswandern-playa-del-carmen-leitfaden.html':
 sec('Erst mieten, und zwar in der unangenehmen Jahreszeit',
     'Verbringen Sie einige Monate hier, bevor Sie Kapital binden, und legen Sie einen Teil davon in die schwüle '
     'Spätsommerhitze statt nur in den angenehmen trockenen Winter. Viertel, die sich an einem Februarnachmittag gleich '
     'anfühlen, verhalten sich im September sehr unterschiedlich — Lärm, Überflutung, Mücken, und ob die Straße '
     'ganzjährig lebt.')
 + sec('Die praktische Liste, die Ihnen niemand gibt',
     'Aufenthaltsstatus und was er erlaubt. Ein mexikanisches Bankkonto, das meist Aufenthalt voraussetzt. Eine RFC, '
     'wenn Mieteinnahmen anfallen. Krankenversicherung, entschieden bevor Sie sie brauchen. Eine lokale Mobilnummer, '
     'weil hier alles über WhatsApp läuft. Und eine realistische Sicht auf Mobilität: außerhalb des fußläufigen '
     'Zentrums ist ein Auto praktisch notwendig.')
 + sec('Was unterschätzt wird',
     'Wie sehr die Luftfeuchtigkeit Besitz und Gebäude beansprucht. Was Klimatisierung im Betrieb kostet. Wie lange '
     'Verwaltungsvorgänge dauern und wie viel glatter sie mit vorbereiteten Unterlagen laufen. Und wie viel leichter '
     'der Alltag mit funktionalem Spanisch wird.'),

'blog-de/badezimmer-renovierung-kosten-playa-del-carmen.html':
 sec('Wohin das Budget wirklich fließt',
     'Nicht in die Fliesen, sondern in das, was dahinter liegt: Abdichtung, Gefälle zum Ablauf, teils Jahrzehnte alte '
     'Leitungen, Lüftung und Elektroarbeiten im Feuchtbereich. Eine Sanierung, die Oberflächen über eine versagende '
     'Abdichtung legt, sieht hervorragend aus und tropft binnen zwei Jahren in den Raum darunter — hier der häufigste '
     'Badschaden.')
 + sec('Wofür es sich zu zahlen lohnt',
     'Fachgerechte Abdichtung mit Hochzügen und Überlappungen statt eines Anstrichs. Gefälle, das tatsächlich '
     'entwässert, vor dem Fliesen mit Wasser geprüft. Lüftung, mechanisch wenn kein Fenster vorhanden ist. Edelstahl '
     'oder hochwertig beschichtete Armaturen, weil gewöhnliches Chrom hier binnen weniger Jahre pittet.')
 + tbl(['Umfang', 'Enthält', 'Kosten 2026'],
       [['Auffrischung', 'Armaturen, Anstrich, kleine Fliesenarbeiten', '$25,000 – $60,000 MXN'],
        ['Komplettsanierung, Standard', 'Rückbau bis fertig, Mittelklasse', '$80,000 – $160,000 MXN'],
        ['Komplettsanierung, gehoben', 'Sonderanfertigung, Naturstein', '$160,000 – $350,000 MXN']]),

'blog-de/bauen-am-cenote-riviera-maya.html':
 sec('Der Abstand ist nicht die ganze Frage',
     'Alle fragen zuerst nach dem Abstand zur Cenote, und das ist erst der Anfang. Die Behörde prüft, ob überhaupt '
     'etwas von Ihrem Grundstück das Wasser erreichen kann: Regenwasserabfluss, Abwasser, Leckagen und Bausedimente. '
     'Ein weit entferntes Haus mit unbehandelter Einleitung ist der schlechtere Antrag als ein näheres, das alles '
     'behandelt und zurückhält. Das Wasser wird vor dem Haus geplant.')
 + sec('Was in der Praxis verlangt wird',
     'Abwasserbehandlung auf dem Grundstück — Biodigester oder Kompaktanlage, niemals Versickerung ohne Behandlung. '
     'Regenwasser gefasst und geführt. Rückhaltung dort, wo Fahrzeuge oder Geräte arbeiten. Sedimentkontrolle während '
     'der Bauzeit, jene Phase, die den meisten Schaden anrichtet und die geringste Aufmerksamkeit erhält.')
 + sec('Daneben wohnen, ehrlich betrachtet',
     'Eine Cenote auf oder neben dem Grundstück ist ein echter Wert und eine echte Verantwortung. Sie begrenzt, wo Sie '
     'bauen, was Sie einleiten, wie Sie nachts beleuchten und was Sie pflanzen dürfen.'),

'blog-de/bauen-oder-kaufen-riviera-maya.html':
 sec('Der Kostenvergleich ohne Verkaufsargument',
     'Bauen kostet pro fertigem Quadratmeter meist weniger als der Kauf vergleichbarer fertiger Immobilien, und der '
     'Abstand wächst im oberen Segment. Aber Bauen bringt Posten mit, die ein Kauf nicht hat: Grundstück, Planung, '
     'Genehmigungen, Anschlüsse — und Ihre Zeit über zwölf bis vierundzwanzig Monate.')
 + sec('Was Bauen Ihnen gibt',
     'Eine Spezifikation für dieses Klima statt für einen Prospekt: echte Abdichtung, Edelstahlbefestigungen, '
     'ausreichend dimensionierte Elektrik für Klimatisierung, behandeltes Abwasser, eine Ausrichtung, die das Haus kühl '
     'hält. Und keine geerbten Mängel — was hier zählt, wo ein fünf Jahre altes, schlecht gebautes Haus das deutlich '
     'zeigt.')
 + sec('Was Kaufen Ihnen gibt',
     'Sicherheit und Tempo. Sie sehen das fertige Objekt, kennen die Zahl, ziehen ein. Das Risiko verschiebt sich vom '
     'Ausführungsrisiko zum Zustandsrisiko — und eine technische Prüfung vor dem Kauf ist günstig und wird fast nie '
     'gemacht.'),

'blog-de/baugenehmigungen-playa-del-carmen.html':
 sec('Was der Antrag enthalten muss',
     'Nutzungsbescheinigung, Fluchtlinie und Hausnummer, Architektur- und Statikprojekt mit gültiger DRO-Unterschrift, '
     'Berechnungen, Erschließungsbestätigung sowie je nach Fall Verkehrsgutachten, Zivilschutzfreigabe und '
     'Umweltgenehmigung. Fehlt ein Punkt, wird der Antrag nicht langsamer — er steht.')
 + sec('Solidaridad im Detail',
     'Die kommunale Prüfung bleibt regelmäßig an zwei Punkten hängen: Verkehrserschließung an Straßen mit Mittelstreifen, '
     'und Regenwasserableitung in einer Stadt, die bei Starkregen schnell überflutet. Beides gehört in den Vorentwurf, '
     'weil beides Anträge zurückgehen lässt.')
 + tbl(['Schritt', 'Dauer', 'Hinweis'],
       [['Nutzungsbescheinigung', '1–3 Wochen', 'Vor jedem Entwurf'],
        ['Fluchtlinie und Hausnummer', '1–2 Wochen', ''],
        ['Baugenehmigung mit DRO', '3–10 Wochen', 'Gültige Registrierung nötig'],
        ['Bauabnahme', 'Zum Abschluss', 'Für die Nutzung erforderlich']]),

'blog-de/beste-gebiete-bauen-playa-del-carmen.html':
 sec('Was die Viertel tatsächlich unterscheidet',
     'Fußweg zur Quinta und zum Strand, nächtlicher Lärm, Überflutungsneigung bei Starkregen, Reife der '
     'Infrastruktur, und ob dort ganzjährig Menschen wohnen oder nur saisonal. Zwei Viertel, die an einem '
     'Februarnachmittag gleich wirken, verhalten sich im September sehr verschieden.')
 + sec('Geschlossene Anlage oder offenes Viertel',
     'Die Anlage bringt Sicherheit, gepflegte Gemeinschaftsflächen und ein geschütztes Umfeld — zum Preis einer '
     'Ordnung, die Ihr Projekt einschränkt: Abstände, Höhen, Materialien, Bauzeiten, Fristen. Das offene Viertel lässt '
     'mehr Gestaltungsfreiheit und überträgt Ihnen die Pflege dessen, was Ihnen gehört.')
 + sec('Was vor dem Kauf zu prüfen ist',
     'Nutzung und Dichte, GRZ und GFZ, Höhe, und ob ein Teil des Grundstücks Schutzgebiet oder Bundeszone berührt. '
     'Danach Vermessung und Baugrundgutachten. Diese Prüfungen kosten einen Bruchteil dessen, was ein falsches '
     'Grundstück kostet.'),

'blog-de/betonarten-bau-riviera-maya.html':
 sec('Was den Beton hier beansprucht',
     'Salzhaltige Luft, hohe Luftfeuchtigkeit und Starkregen. Der Feind ist nicht die Druckfestigkeit, sondern das '
     'Eindringen von Chloriden bis zur Bewehrung. Deshalb entscheiden Betondeckung, Verdichtung und Nachbehandlung hier '
     'mehr über die Lebensdauer als die Festigkeitsklasse auf dem Lieferschein.')
 + sec('Betondeckung und Nachbehandlung',
     'Zu geringe Deckung ist der häufigste Baufehler an dieser Küste und zeigt sich Jahre später als abplatzender Beton '
     'mit rostender Bewehrung. Ebenso wichtig: Nachbehandlung in der ersten Woche. Bei dieser Hitze trocknet '
     'ungeschützter Beton zu schnell aus, verliert Festigkeit und reißt.')
 + sec('Wo Ortbeton, wo Fertigteil, wo Spritzbeton',
     'Ortbeton für Fundamente, Stützen, Unterzüge und Decken. Fertigteile, wo Wiederholung und Termindruck es '
     'rechtfertigen. Spritzbeton für Pools und Stützwände mit freier Geometrie — im zerklüfteten Kalkstein häufig die '
     'praktikabelste Lösung.'),

'blog-de/boutique-hotel-bauen-tulum.html':
 sec('Das Genehmigungspaket ist der Projektplan',
     'Ein Boutiquehotel in Tulum ist ein Gewerbeprojekt unter Umweltprüfung: Nicht die kommunale Lizenz, sondern das '
     'Bundesdossier bestimmt den Baubeginn. Rechnen Sie mit Monaten und misstrauen Sie jedem Terminplan, der diese '
     'Phase nicht benennt. Das Gebäude selbst ist der einfachere Teil.')
 + sec('Was es von einem großen Haus unterscheidet',
     'Abwasser in Hotelmenge verlangt eine Kompaktanlage, keinen Haus-Biodigester. Die elektrische Last erfordert einen '
     'eigenen Transformator. Wasserspeicher und Pumpen werden auf Spitzenbelegung ausgelegt. Brandschutz, Fluchtwege '
     'und Zivilschutzfreigabe kommen hinzu. Und der Back-of-House-Bereich — Wäscherei, Lager, Personalräume — ist für '
     'Gäste unsichtbar und für unerfahrene Budgets ebenso.')
 + tbl(['Segment', 'Was es bedeutet', 'Kosten pro m²'],
       [['Boutique, einfach', 'Moderate Ausstattung', '$22,000 – $32,000 MXN'],
        ['Boutique, gestaltet', 'Sonderanfertigungen', '$32,000 – $48,000 MXN'],
        ['Gehoben', 'Importspezifikation', 'Ab $48,000 MXN']]),

'blog-de/fernverwaltung-bau-mexiko.html':
 sec('Die fünf Momente, die sich nicht nachholen lassen',
     'Absteckung und Höhen vor dem Aushub. Fundamentbewehrung vor dem Guss. Deckenbewehrung, eingelegte Leitungen und '
     'Druckprüfung vor dem Guss. Abdichtung vor dem Überdecken. Elektro und Sanitär vor dem Schließen der Wände. Jeder '
     'dauert Stunden und bestimmt das Haus. Alles andere lässt sich später prüfen, diese nicht — außer man schlägt '
     'etwas auf.')
 + sec('Was der Bericht enthalten muss',
     'Wöchentlich, schriftlich, mit datierten Fotos jeder Etappe vor dem Verschließen, Fortschritt gegen Terminplan, '
     'Laborergebnisse, Mängelliste mit Verantwortlichem und Frist, und ein Nachtragsregister. Lose Fotos per '
     'Messenger ohne Datum sind kein Bericht, sondern Beruhigung — und genau die produziert ein Projekt in '
     'Schwierigkeiten am meisten.')
 + sec('Zahlungen als Schutzmechanismus',
     'An überprüfbare Bautenstände koppeln statt an Kalenderdaten, Anzahlung anteilig verrechnen statt bis zum Ende '
     'offen lassen, und Einbehalt bis zur Abarbeitung der Mängelliste. Diese eine Struktur schützt einen abwesenden '
     'Bauherrn mehr als jede Überwachung.'),

'blog-de/fundamenttypen-riviera-maya.html':
 sec('Warum die Gründung hier nicht aus dem Katalog kommt',
     'Zerklüfteter Kalkstein mit Hohlräumen, Sascab und altem Auffüllmaterial. Zwei Nachbargrundstücke können '
     'unterschiedliche Gründungen brauchen, weil eines in drei Metern Tiefe einen Hohlraum hat und das andere nicht. '
     'Deshalb steht am Anfang das Baugrundgutachten und nicht ein Standarddetail.')
 + sec('Die üblichen Lösungen',
     'Einzel- und Streifenfundamente auf tragfähigem Fels, die häufigste Lösung. Plattengründung, wenn die Lasten '
     'verteilt werden sollen oder der Untergrund uneinheitlich ist. Tiefergründung oder Verfüllung von Hohlräumen, wo '
     'die Erkundung sie nachweist. Und immer: Aushub im Fels, der Zeit und Gerät kostet und in jedem Angebot als '
     'eigene Position stehen sollte.')
 + sec('Die teuerste Überraschung der Region',
     'Ein Hohlraum, der nach dem Rohbau entdeckt wird. Die Sanierung kostet ein Vielfaches des Gutachtens, das ihn '
     'gefunden hätte — und sie kommt zum denkbar schlechtesten Zeitpunkt.'),

'blog-de/gelaendevorbereitung-stuetzmauern-riviera-maya.html':
 sec('Stützmauern versagen an der Entwässerung, nicht an der Mauer',
     'Ohne Entwässerung staut sich hinter der Mauer Wasserdruck, und sie reißt oder kippt. Was vorhanden sein muss: '
     'Kiesfilter, Geotextil gegen Verschlämmung, perforiertes Rohr am Fuß und Entwässerungsöffnungen. Das kostet einen '
     'Bruchteil der Mauer und entscheidet zwischen zwanzig Jahren und zwei Regenzeiten.')
 + sec('Geländevorbereitung, die später Geld spart',
     'Rodung mit Erhalt dessen, was erhalten werden soll, Aushub im Fels mit realistischer Kalkulation, Verfüllung in '
     'dünnen, verdichteten Lagen mit Kontrolle, und eine Höhenplanung, die das Regenwasser vom Haus wegführt. Schlecht '
     'verdichtete Auffüllung ist der Grund für einen großen Teil der Setzungsrisse in dieser Region.')
 + tbl(['Mauertyp', 'Übliche Höhe', 'Kosten je m² Ansichtsfläche'],
       [['Schwergewichtsmauer, Mauerwerk', 'bis 2,0 m', '$2,500 – $4,500 MXN'],
        ['Stahlbeton, auskragend', '2,0 – 4,0 m', '$3,500 – $6,500 MXN'],
        ['Gabionen', '1,5 – 4,0 m', '$1,800 – $3,200 MXN']]),

'blog-de/haus-unterhaltskosten-mexiko.html':
 sec('Was dieses Klima mit einem leeren Haus macht',
     'Feuchtigkeit findet jeden geschlossenen, unbelüfteten Raum und macht Schimmel daraus. Monatelang abgeschaltete '
     'Klimaanlagen lassen das zu; unbeaufsichtigt laufende überschwemmen bei verstopftem Kondensatablauf eine Decke. '
     'Die Poolchemie kippt binnen Tagen. Salz greift Beschläge dauerhaft an. Im ersten Monat unspektakulär, im sechsten '
     'teuer.')
 + tbl(['Posten', 'Monatlich', 'Hinweis'],
       [['Strom', '$2,500 – $10,000 MXN', 'Tarifstufen bestrafen hohen Klimabedarf'],
        ['Wasser', '$200 – $800 MXN', ''],
        ['Gas', '$500 – $1,500 MXN', 'LP-Tank'],
        ['Pool', '$1,500 – $4,000 MXN', 'Wöchentlicher Service'],
        ['Garten', '$2,000 – $6,000 MXN', 'Wachstum überrascht Zugezogene']])
 + sec('Der Wartungskalender',
     'Wöchentlich Pool, Garten und ein Rundgang mit Fotos. Monatlich alle Hähne laufen lassen und Spülungen betätigen, '
     'Kondensatabläufe prüfen. Vierteljährlich Klimafilter und Beschläge. Jährlich Abdichtung vor der Regenzeit, '
     'Abläufe, Elektroprüfung, Pumpenwartung.'),

'blog-de/klaeranlage-abwasser-riviera-maya.html':
 sec('Warum die klassische Sickergrube hier falsch ist',
     'Die Halbinsel besteht aus zerklüftetem Kalkstein: Was versickert, erreicht rasch den Grundwasserleiter, und '
     'dieser entwässert in Cenoten und aufs Riff. Deshalb bedingen oder verweigern Umweltbehörden Projekte mit '
     'unbehandelter Einleitung — und deshalb ist eine einfache Sickergrube für Schwarzwasser nicht nur rechtlich, '
     'sondern sachlich ein Problem.')
 + sec('Biodigester oder Kompaktanlage',
     'Selbstreinigender Biodigester für das Einfamilienhaus, ausgelegt nach Nutzerzahl und Tagesmenge. Kompaktanlage, '
     'wenn die Menge es verlangt: kleines Hotel, Restaurant, mehrere Wohneinheiten. Behandeltes Abwasser darf gemäß '
     'Genehmigung zur Bewässerung genutzt oder versickert werden — was etwas anderes ist als unbehandelte Versickerung.')
 + tbl(['Lösung', 'Anwendungsfall', 'Kosten'],
       [['Biodigester', 'Haus, 5–10 Nutzer', '$25,000 – $60,000 MXN'],
        ['Kompaktanlage', 'Hotel, Restaurant, mehrere Einheiten', '$180,000 – $600,000 MXN'],
        ['Fettabscheider', 'Küchen', '$8,000 – $25,000 MXN']]),

'blog-de/nachhaltiges-bauen-tulum.html':
 sec('Nachhaltig heißt hier zuerst: weniger Kühlbedarf',
     'Der größte ökologische und finanzielle Hebel ist nicht die Photovoltaik, sondern das Haus davor: Ausrichtung, '
     'Querlüftung, Verschattung nach Westen, Dämmung, Sonnenschutzglas und thermische Masse. Erst danach lohnt es sich, '
     'die verbleibende Last mit Solar zu decken. Umgekehrt wird es teuer.')
 + sec('Wasser ist hier das eigentliche Thema',
     'Regenwassernutzung mit ausreichendem Speicher, sparsame Armaturen, Behandlung des Abwassers statt Versickerung, '
     'und Wiederverwendung des behandelten Abflusses zur Bewässerung, soweit genehmigt. In einer Karstlandschaft mit '
     'Cenoten ist das der wirksamste Beitrag, den ein Haus leisten kann.')
 + sec('Materialien mit kurzem Weg',
     'Regionale Harthölzer, lokaler Kalkstein, Chukum statt importierter Beschichtungen. Das reduziert Transport, passt '
     'zum Klima und altert besser als vieles, was hierher verschifft wird.'),

'blog-de/palapa-bau-leitfaden.html':
 sec('Wie lange eine Palapa wirklich hält',
     'Gut verlegtes Huano hält meist 8 bis 15 Jahre bis zur Erneuerung. Die Spanne ist so groß wegen der Umgebung: '
     'Dauerschatten und nie trocknende Feuchte verkürzen sie deutlich, Belüftung von unten verlängert sie, ebenso ein '
     'steiles Dach und korrekte Überlappung. Die Hartholzkonstruktion überdauert mehrere Deckungszyklen — deshalb '
     'kostet das Neudecken einen Bruchteil.')
 + sec('Brandschutz, Versicherung, Genehmigung',
     'Huano lässt sich mit Flammschutzmittel behandeln, und bei Miet- oder Gewerbeobjekten ist das meist Pflicht: viele '
     'Versicherer verlangen es, manche Kommunen ebenfalls. Während des Baus aufgetragen kostet es weit weniger als '
     'nachträglich.')
 + tbl(['Position', 'Detail', 'Kosten je m²'],
       [['Neue Palapa', 'Hartholz und Huano', '$4,000 – $9,000 MXN'],
        ['Premium-Konstruktion', 'Chicozapote, sichtbare Verbindungen', '$7,000 – $12,000 MXN'],
        ['Neudeckung', 'Konstruktion bleibt', '$1,500 – $3,500 MXN']]),

'blog-de/restaurant-bar-bau-riviera-maya.html':
 sec('Die Haustechnik macht das Projekt',
     'Abluft nach der realen Küche ausgelegt, normgerechter Fettabscheider, Gasversorgung mit Sicherheitseinrichtungen, '
     'elektrische Leistung und Verteilung passend zu den Geräten, ausreichend Warmwasser, und eine Entwässerung, die '
     'die regional geforderte Abwasserbehandlung einhält. Die Oberflächen sieht man; ob pünktlich eröffnet wird, '
     'entscheidet die Technik.')
 + sec('Der Eröffnungstermin ist das Budget',
     'Jede Woche Verzug kostet Umsatz. Deshalb: lange Lieferzeiten vor dem Rückbau bestellen, Gewerke überlappen, wo es '
     'sicher geht, und Vermieter oder Centermanagement früh einbinden.')
 + sec('Genehmigungen und Zivilschutz',
     'Nutzung passend zum Betrieb, Bau- oder Umbaugenehmigung, Zivilschutzfreigabe und die gastronomiespezifischen '
     'Hygieneanforderungen. In Einkaufszentren zusätzlich die Zustimmung der Verwaltung, die Pläne, Versicherungen und '
     'Arbeitszeiten vorab sehen will.'),

'blog-de/steuervorteile-bau-mexiko.html':
 sec('Was Sie hier realistisch erwarten können',
     'Bauleistungen mit ordnungsgemäßer Rechnung (factura) sind bei vermieteten Objekten grundsätzlich als Aufwand oder '
     'über Abschreibung relevant, und bei einem späteren Verkauf können nachgewiesene, korrekt fakturierte Investitionen '
     'die Bemessungsgrundlage beeinflussen. Beides setzt eine RFC und lückenlose Belege voraus — ohne Rechnung existiert '
     'die Investition steuerlich nicht.')
 + sec('Warum "ohne Rechnung billiger" teuer wird',
     'Der Nachlass ist einmalig, der Nachteil dauerhaft: keine steuerliche Anerkennung, kein Nachweis der Investition '
     'beim Verkauf, keine Gewährleistungsgrundlage und kein Beleg im Streitfall. Wir fakturieren jede Leistung, und '
     'das ist ausdrücklich Teil dessen, wofür Sie zahlen.')
 + sec('Wer das entscheidet, sind nicht wir',
     'Wir sind Bauunternehmer. Wir sagen Ihnen, dass die Pflichten und die Möglichkeiten bestehen, und verweisen Sie an '
     'einen mexikanischen Contador, der es zeichnet. Wer im Bauwesen Steuerberatung anbietet, überschreitet seine '
     'Kompetenz.'),

'blog-de/strandhaus-bauen-riviera-maya.html':
 sec('Was direkt am Meer anders ist',
     'Salz greift zuerst Beschläge, dann Aluminiumprofile, dann ungeschützte Elektroinstallationen an. Die Antwort ist '
     'unspektakulär und wirksam: Edelstahlbefestigungen, hochwertig eloxierte oder pulverbeschichtete Profile, dichte '
     'Harthölzer oder Komposit außen, Betondeckung mit Reserve und Elektroverteilungen mit echtem Schutzgrad.')
 + sec('Bundeszone und was sie bedeutet',
     'Die Bundeszone am Strand (ZOFEMAT) ist niemals Teil Ihres Titels, unabhängig davon, was ein Verkäufer sagt. Ihre '
     'Nutzung erfordert eine eigene Konzession mit eigenem Verfahren und jährlicher Zahlung. Das gehört vor den Kauf '
     'geprüft.')
 + sec('Sturmschutz von Anfang an',
     'Schlagregendichte Öffnungen mit Verbundsicherheitsglas oder Läden, verankertes Dach, Entwässerung mit Reserve, '
     'und ein Grundriss, der bei geschlossenen Öffnungen bewohnbar bleibt. Nachträglich kostet all das ein Vielfaches.'),

'blog-de/tropische-gartengestaltung-riviera-maya.html':
 sec('Arten, die Salz, Trockenzeit und Starkregen aushalten',
     'Sechs trockene und sechs sehr feuchte Monate, dazu Salz an der Küste. Bewährt haben sich heimische und angepasste '
     'Arten: lokale Palmen, Meertraube in erster Reihe, Bougainvillea, Plumbago, Kroton, Agaven und Sukkulenten in der '
     'Sonne, Farne und Philodendren im Schatten. Was scheitert, ist die aus einem gemäßigten Projekt kopierte '
     'Pflanzenpalette.')
 + sec('Boden und Bewässerung',
     'Über Kalkstein ist das Substrat meist dünn, ernsthafte Gärten brauchen hier Bodenaufbau. Automatische '
     'Sektorbewässerung ist das, was jährliches Nachpflanzen verhindert, und frühmorgens gießen reduziert die '
     'Verdunstung erheblich.')
 + sec('Bäume und Sturmsaison',
     'Erziehungsschnitt von jung an, Pflanzabstand nach der Endgröße, und jährliche Kontrolle von Ästen über Dach und '
     'Leitungen. Ein großer Teil der Sturmschäden an gut gebauten Häusern stammt von falsch platzierter Vegetation.'),

'blog-de/wertsteigerung-immobilien-riviera-maya-2026.html':
 sec('Was den Wert hier tatsächlich treibt',
     'Reale Infrastruktur — Zufahrt, Flughafen, Versorgung, Sicherheit — und die Knappheit an differenziertem Produkt. '
     'Nicht das Versprechen eines künftigen Projekts und nicht die Renditeprognose eines Prospekts. Wenn viele nahezu '
     'identische Einheiten um denselben Gast konkurrieren, zeigt sich die Anpassung zuerst in der Auslastung.')
 + sec('Wo der Markt dünner ist',
     'Private Villen mit echtem Außenraum, Privatsphäre und Pool konkurrieren in einem deutlich weniger besetzten '
     'Segment als kleine, über Rendite verkaufte Wohnungen. Sie sind schwerer zu bauen und kaum in Serie zu '
     'reproduzieren — und genau diese Hürde schützt den Wert des Bestehenden.')
 + sec('Nüchtern rechnen',
     'Gegen die tatsächlich erzielte Auslastung vergleichbarer Inserate rechnen, nicht gegen die Prognose. Vollständige '
     'Betriebskosten abziehen: Verwaltung 15% bis 30% vom Brutto, Reinigung, Strom mit Klimatisierung, Pool, Garten, '
     'Versicherung und 1% bis 2% des Werts pro Jahr als Instandhaltungsrücklage.'),

'blog-de/zisternen-wasserversorgung-riviera-maya.html':
 sec('Warum hier jedes Haus speichert',
     'Das kommunale Netz liefert nicht überall durchgehend und nicht mit konstantem Druck. Deshalb speichert das Haus: '
     'Zisterne ebenerdig oder erdverlegt, Pumpe für den Hausdruck, häufig mit Druckkessel oder drehzahlgeregelter Pumpe, '
     'damit der Druck nicht bei jedem geöffneten Hahn schwankt.')
 + sec('Volumen richtig bemessen',
     'Nach Personenzahl, Nutzung und gewünschter Autonomie bei Versorgungsausfall. Ein Familienhaus kommt meist mit '
     'einigen tausend Litern aus; eine Ferienvilla mit hoher Belegung braucht deutlich mehr, und ein Pool wird separat '
     'gerechnet. Zu knapp bemessen fällt in der ersten Hochsaisonwoche auf.')
 + sec('Ausführung und Reinigung',
     'Innenabdichtung, dichter Deckel gegen Insekten und Licht, echter Zugang zur Reinigung, Belüftung. Mindestens '
     'jährliche Reinigung ist Pflicht, nicht Kür. Wird Regenwasser eingeleitet, gehört ein Erstspülabscheider davor.'),
}


def insert(path, block):
    s = open(path, encoding='utf-8').read()
    s = re.sub(re.escape(OPEN) + r'.*?' + re.escape(CLOSE), '', s, flags=re.S)
    payload = OPEN + '\n' + block + CLOSE + '\n'
    m = (re.search(r'\n[ \t]*<h2[^>]*>\s*(Häufige Fragen|FAQ)', s)
         or re.search(r'\n[ \t]*<div class="cta-section', s)
         or re.search(r'\n[ \t]*<section data-cluster=', s))
    at = (s.rfind('\n', 0, m.start() + 1) + 1) if m else s.rfind('<footer')
    s = s[:at] + payload + s[at:]
    open(path, 'w', encoding='utf-8').write(s)
    return s


def wc(html):
    return len(re.sub(r'<[^>]+>', ' ', html[html.index('<h1'):html.index('<footer')]).split())


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    n = 0
    for path, block in B.items():
        if not os.path.exists(path):
            print('  missing:', path); continue
        before = wc(open(path, encoding='utf-8').read())
        after = wc(insert(path, block))
        n += 1
        print('%-58s %4d -> %4d' % (path, before, after))
    print('deepened:', n)
