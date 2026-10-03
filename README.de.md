# Cybercrime in Deutschland, 2016 bis 2025

**Fallzahlen, Aufklärungsquote und Unterschiede zwischen den Bundesländern auf Grundlage der Polizeilichen Kriminalstatistik des Bundeskriminalamts (BKA)**

🇬🇧 [English version](README.md)

Dieses Projekt untersucht, wie sich die von der Polizei erfasste Cybercrime in Deutschland über zehn Jahre entwickelt hat. Grundlage ist die amtliche Polizeiliche Kriminalstatistik (PKS), die das BKA jedes Jahr veröffentlicht.

Die Analyse beantwortet drei Fragen. Wie haben sich die Fallzahlen entwickelt? Wie viele dieser Fälle klärt die Polizei auf, verglichen mit der Kriminalität insgesamt? Und wie stark unterscheiden sich die 16 Bundesländer?

Die vollständige Analyse steht im Notebook [`cybercrime_germany_pks.ipynb`](notebooks/cybercrime_germany_pks.ipynb), das auf Englisch geschrieben ist. Dazu gibt es ein interaktives [Dashboard](https://cybercrime-germany-pks.streamlit.app/) auf Deutsch und Englisch.

## Was hier als Cybercrime zählt

Welche Straftaten zu Cybercrime gehören, habe ich nicht selbst festgelegt. Das Projekt übernimmt die Abgrenzung des BKA, den Summenschlüssel 897000 „Cybercrime“, der sich aus vier Straftatenschlüsseln zusammensetzt:

| Schlüssel | Straftat | Strafgesetzbuch |
|---|---|---|
| 543000 | Fälschung beweiserheblicher Daten, Täuschung im Rechtsverkehr bei Datenverarbeitung | §§ 269, 270 StGB |
| 674200 | Datenveränderung, Computersabotage | §§ 303a, 303b StGB |
| 678000 | Ausspähen, Abfangen von Daten einschl. Vorbereitungshandlungen und Datenhehlerei | §§ 202a bis 202d StGB |
| 897100 | Computerbetrug | § 263a StGB |

In der Praxis ist das vor allem Computerbetrug, der 2025 gut 82 % der Fälle ausmachte.

Für den Vergleich über die Jahre war ein Detail wichtig. Bis 2020 zählte das BKA unter diesem Schlüssel auch die Softwarepiraterie mit, seit 2021 nicht mehr. Damit in jedem Jahr dieselben Straftaten verglichen werden, habe ich Cybercrime für den gesamten Zeitraum als Summe der vier Schlüssel berechnet und nicht die veröffentlichte Summe verwendet. Die so berechneten Werte für 2020 bis 2022 stimmen mit den Zahlen überein, die das BKA selbst im [Bundeslagebild Cybercrime 2022](https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/JahresberichteUndLagebilder/Cybercrime/cybercrimeBundeslagebild2022.pdf?__blob=publicationFile&v=4) nennt (Seite 5). Der Zeitraum beginnt 2016, weil der Schlüssel für Computerbetrug in diesem Jahr eingeführt wurde und das BKA die Zahlen von 2016 als nicht vergleichbar mit 2015 kennzeichnet.

## 1. Wie haben sich die Fallzahlen entwickelt?

Die Diagramme stammen aus dem englischen Notebook und sind deshalb englisch beschriftet. Im Dashboard gibt es sie auch auf Deutsch.

![Erfasste Fälle von Cybercrime, 2016 bis 2025](figures/01_cybercrime_cases.png)

Die erfasste Cybercrime stieg von 107.278 Fällen im Jahr 2016 auf den Höchstwert von 146.363 im Jahr 2021 und ist seitdem in jedem Jahr gesunken. 2025 erfasste die Polizei 126.034 Fälle. Das sind 14 % weniger als der Höchstwert, aber immer noch 17 % mehr als 2016. Im selben Zeitraum gingen die Straftaten insgesamt um 14 % zurück. Cybercrime hat also an Gewicht gewonnen: Ihr Anteil an allen erfassten Straftaten stieg von 1,7 % auf 2,3 %.

Die Statistik zeigt diese Entwicklung, aber nicht ihre Ursachen. Dazu äußert sich das BKA in seinen Lagebildern. Den Anstieg bis 2021 verbindet es mit der Digitalisierung, die durch die Corona-Pandemie noch beschleunigt wurde und neue Tatgelegenheiten geschaffen hat ([Pressemitteilung vom 9. Mai 2022](https://www.presseportal.de/blaulicht/pm/7/5217298)). Den Rückgang 2022 begründet es mit der Lockerung der Corona-Schutzmaßnahmen: Onlinehandel und mobiles Arbeiten hätten in den Vorjahren zusätzliche Angriffsmöglichkeiten geboten, 2022 habe sich ein Teil des Kriminalitätsgeschehens wieder in die analoge Welt verlagert ([Bundeslagebild Cybercrime 2022](https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/JahresberichteUndLagebilder/Cybercrime/cybercrimeBundeslagebild2022.pdf?__blob=publicationFile&v=4), Seite 7). Zum russischen Angriffskrieg gegen die Ukraine, der am 24. Februar 2022 begann, schreibt das BKA, er habe auch in Deutschland zu einer erhöhten Cyber-Bedrohungslage geführt (Seite 22). Die in der PKS erfassten Fälle gingen 2022 dennoch zurück.

Das BKA selbst nennt diesen Rückgang „scheinbar“. Die hier verwendete Statistik enthält nur Taten, die in Deutschland begangen wurden. Taten, bei denen der Schaden in Deutschland eintritt, der Täter aber im Ausland sitzt oder sein Aufenthaltsort unbekannt ist, werden seit 2020 getrennt erfasst. Diese Auslandstaten nahmen 2022 um über 8 % zu, während die Inlandstaten um 6,5 % zurückgingen (Bundeslagebild 2022, Seite 6).

## 2. Wie viele Fälle werden aufgeklärt?

![Aufklärungsquote von Cybercrime und Straftaten insgesamt](figures/02_clearance_rate.png)

Weniger als jeder dritte. Die Aufklärungsquote bei Cybercrime sank von 37,5 % im Jahr 2016 auf 31,4 % im Jahr 2025, während die Quote der Straftaten insgesamt in jedem Jahr zwischen 56 % und 59 % lag. Der Abstand zwischen beiden wuchs von 19 auf 27 Prozentpunkte.

Der Rückgang geschah in einem Schritt zwischen 2018 und 2019, seitdem liegt die Quote bei rund 30 %. Die Zahl der aufgeklärten Fälle hat sich in den zehn Jahren kaum verändert, sie lag jedes Jahr bei etwa 39.000 bis 43.000, während die Zahl der erfassten Fälle gestiegen ist.

## 3. Wie unterscheiden sich die Bundesländer?

![Cybercrime je 100.000 Einwohner nach Bundesland, 2016 und 2025](figures/03_federal_states.png)

Die Unterschiede sind sehr groß. 2025 erfasste Bremen 563 Fälle je 100.000 Einwohner, Mecklenburg-Vorpommern 39. Das ist der Faktor 14,5. Die drei Stadtstaaten Berlin, Bremen und Hamburg belegen 2016 und 2025 die ersten drei Plätze, ihr hohes Niveau ist also kein Ausreißer eines einzelnen Jahres. Dahinter ist die Rangfolge nicht stabil: In Bremen hat sich die Häufigkeitszahl etwa verdoppelt, in Mecklenburg-Vorpommern ist sie um drei Viertel gesunken.

Bremen fällt selbst unter den Stadtstaaten auf, und ich bin dem nachgegangen. Fast die Hälfte des Bremer Werts kommt aus einem einzigen Straftatenschlüssel, dem Computerbetrug mittels rechtswidrig erlangter sonstiger unbarer Zahlungsmittel (Schlüssel 516920). Bremen erfasste 2025 davon 257 Fälle je 100.000 Einwohner, das 17-Fache des Bundeswerts, während Berlin und Hamburg bei 11 liegen. Ohne diesen einen Schlüssel läge Bremen hinter beiden. Warum dieser Schlüssel gerade in Bremen so hoch ist, geht aus den veröffentlichten Tabellen nicht hervor. Der Anstieg ist allerdings nicht neu: Schon für 2022 berichtete der [Weser-Kurier](https://www.weser-kurier.de/bremen/politik/bremer-kriminalstatistik-immer-mehr-digitale-straftaten-doc7p7nodmh7tg1b8franvb) (6. März 2023), der Computerbetrug mit gestohlenen unbaren Zahlungsmitteln habe sich in Bremen binnen eines Jahres mehr als verdoppelt, von 968 auf 2.136 Fälle. Nach dem Bericht sieht das Bremer Landeskriminalamt diesen Anstieg begünstigt durch die zunehmende Verbreitung elektronischer Zahlungsmethoden wie Apple Pay und Google Pay.

Das gilt für den Ländervergleich insgesamt. Die Häufigkeitszahlen veränderten sich von 2016 bis 2025 zwischen −74 % und +103 %. Woher diese Unterschiede kommen, zeigen die Tabellen nicht, und die Hinweise des BKA zur PKS 2025 nennen für kein Land eine Besonderheit in diesem Bereich. Allgemein weist das BKA darauf hin, dass hohe Steigerungsraten zum Teil auf Ermittlungskomplexe mit zahlreichen Einzelfällen zurückgehen. Ob das für ein bestimmtes Land gilt, geht aus den Tabellen nicht hervor.

## Was die Daten nicht zeigen

Die Polizeiliche Kriminalstatistik zählt nur, was der Polizei bekannt wird. Das Dunkelfeld bei Cybercrime wird nach Angaben des BKA in Studien auf bis zu 91,5 % geschätzt. Das BKA schreibt deshalb, die PKS habe nur eine begrenzte Aussagekraft für die tatsächlich verübten Cyber-Straftaten und eigne sich vor allem für Aussagen zum Trend ([Bundeslagebild Cybercrime 2022](https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/JahresberichteUndLagebilder/Cybercrime/cybercrimeBundeslagebild2022.pdf?__blob=publicationFile&v=4), Seite 4).

Die Zahlen sind außerdem enger gefasst, als das Wort „Cybercrime“ vermuten lässt. Seit 2014 wird ein Fall nur gezählt, wenn konkrete Anhaltspunkte für eine Tathandlung in Deutschland vorliegen. Straftaten mit dem Tatmittel Internet weist das BKA in einer eigenen Tabelle aus, sie sind hier nicht enthalten.

Drei technische Punkte begrenzen die Genauigkeit. Die Aufklärungsquoten vor 2019 sind Näherungen, weil das BKA sie nur mit einer Nachkommastelle veröffentlicht hat und ich die aufgeklärten Fälle daraus zurückgerechnet habe. Die Häufigkeitszahlen beruhen für 2016 auf dem Zensus 2011 und für 2025 auf dem Zensus 2022, was das BKA als nur eingeschränkt vergleichbar bezeichnet. Und der Ländervergleich hat zwei Zeitpunkte, 2016 und 2025, nicht die Jahre dazwischen.

## Das Projekt ausführen

```
├── app.py                               Streamlit-Dashboard (Deutsch / Englisch)
├── requirements.txt
├── notebooks/
│   └── cybercrime_germany_pks.ipynb     Laden, Prüfen, Analyse, Diagramme
├── data/
│   ├── raw/                             Originaltabellen und Hinweise des BKA
│   └── clean/                           Ergebnistabellen für das Dashboard
└── figures/                             Die drei Diagramme als PNG
```

Das Notebook liest die drei Excel-Dateien in `data/raw`, prüft sie, berechnet die Ergebnisse und schreibt zwei kleine Tabellen nach `data/clean` sowie die Diagramme nach `figures`. Das Dashboard läuft online unter https://cybercrime-germany-pks.streamlit.app/ und liest diese beiden Tabellen. Lokal starten:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Quellen

Alle Daten stammen vom Bundeskriminalamt (BKA), Polizeiliche Kriminalstatistik (PKS). Das BKA erlaubt die Vervielfältigung nur mit Quellenangabe. Die Zahlen zu Cybercrime vor 2021, die Aufklärungsquoten vor 2021 und die Häufigkeitszahlen der Länder für 2016 sind eigene Berechnungen auf Grundlage dieser Tabellen.

| Verwendet für | Tabelle oder Dokument | Stand |
|---|---|---|
| Fälle und Aufklärungsquote, Bund | PKS 2025, Zeitreihen, T01 Grundtabelle – Fälle ab 1987 | V1.1, 08.04.2026 |
| Bundesländer 2025 | PKS 2025, T01 Grundtabelle – Fälle mit Häufigkeitszahl (HZ) – Länder | V1.0, 06.03.2026 |
| Bundesländer 2016 | PKS 2016, T01 Grundtabelle – Länder | 27.01.2017 |
| Hinweise des BKA zur Vergleichbarkeit und zu Steigerungsraten | PKS 2016, T01 Grundtabelle – Länder – Fallentwicklung | 01.02.2017 |
| Abgrenzung von Cybercrime | PKS 2025 – Übersicht Summenschlüssel, Seite 9 | V1.0 |
| Änderungen bei Erfassung und Schlüsseln | PKS 2025 – Hinweise zu den Zeitreihen, Seiten 19, 23 und 40 | V1.0 |
| Bevölkerungsbasis, Hinweise zu den Ländern | PKS 2025 – Wichtige Hinweise zur Interpretation der Daten, Seiten 4 bis 6 | V1.0 |

Die Tabellen stehen auf der Website des BKA: [PKS 2025, Tabellen und Interpretationshilfen](https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/PKS2025/pksTabellen_Interpretationshilfen/pksTabellen_Interpretationshilfen_node.html), [PKS 2025, Zeitreihen](https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/PKS2025/pksTabellen_Interpretationshilfen/Zeitreihen/zeitreihen_node.html) und [alle Berichtsjahre, auch 2016](https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/pks_node.html). Zur Einordnung, nicht für Berechnungen, dienen die im Text verlinkten Quellen: die Pressemitteilung des BKA zum Bundeslagebild Cybercrime 2021, das Bundeslagebild Cybercrime 2022 (Seiten 4 bis 7 und 22) und der Bericht des Weser-Kuriers vom 6. März 2023.

## Werkzeuge und KI-Nutzung

Python (pandas, matplotlib, Plotly), Jupyter und Streamlit. Das Projekt ist hauptsächlich mit Claude (Anthropic) bei Code und Text entstanden, für den finalen Check wurde zusätzlich ChatGPT (OpenAI) verwendet; Fragen, Entscheidungen und Prüfungen stammen von mir. Wie ich mit KI arbeite, beschreibe ich in meinem Repository [local-ai-workflow](https://github.com/Amirhouschang/local-ai-workflow).

---

© 2026 Amirhoushang Rahmannejad. Alle Rechte vorbehalten.
