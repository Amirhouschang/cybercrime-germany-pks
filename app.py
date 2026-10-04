"""Cybercrime in Germany - interactive dashboard (English / German).

Run locally with:  streamlit run app.py
Data: data/clean/cybercrime_federal.csv and data/clean/cybercrime_states.csv,
both created by the notebook from the Police Crime Statistics (PKS) of the BKA.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA_CLEAN = Path(__file__).parent / "data" / "clean"
FIRST_YEAR, LAST_YEAR = 2016, 2025

# English names of the federal states (states missing here have the same name in both languages)
STATE_NAMES_EN = {
    "Bayern": "Bavaria", "Hessen": "Hesse", "Mecklenburg-Vorpommern": "Mecklenburg-Western Pomerania",
    "Niedersachsen": "Lower Saxony", "Nordrhein-Westfalen": "North Rhine-Westphalia",
    "Rheinland-Pfalz": "Rhineland-Palatinate", "Sachsen": "Saxony", "Sachsen-Anhalt": "Saxony-Anhalt",
    "Thüringen": "Thuringia",
}
STATE_NAMES_DE = {english: german for german, english in STATE_NAMES_EN.items()}

st.set_page_config(page_title="Cybercrime in Germany", page_icon="📊", layout="wide")


# ----------------------------------------------------------------------------
# Texts in both languages
# ----------------------------------------------------------------------------
TEXT = {
    "en": {
        "title": "Cybercrime in Germany",
        "subtitle": "Recorded cases, clearance rate and differences between the federal states, 2016 to 2025",
        "intro": ("Based on the Police Crime Statistics (PKS) of the Federal Criminal Police Office (BKA). "
                  "Cybercrime follows the BKA definition: aggregate key 897000, calculated as the sum of the "
                  "offence keys 543000, 674200, 678000 and 897100. The figures cover only cases that were "
                  "reported to the police and committed in Germany."),
        "language": "Language",
        "kpi_cases": "Recorded cases {year}",
        "kpi_cases_delta": "{value} since {year}",
        "kpi_clearance": "Clearance rate {year}",
        "kpi_clearance_delta": "{value} points vs. all crime",
        "kpi_share": "Share of all recorded crime",
        "kpi_share_delta": "{value} points since {year}",
        "kpi_spread": "Highest vs. lowest state",
        "kpi_spread_value": "Factor {value}",
        "kpi_spread_delta": "{high} vs. {low}",
        "tab_cases": "Cases",
        "tab_clearance": "Clearance rate",
        "tab_states": "Federal states",
        "tab_sources": "Method and sources",
        "years": "Years",
        "cases_title": "Recorded cybercrime cases",
        "cases_axis": "Recorded cases",
        "share_title": "Cybercrime as a share of all recorded crime",
        "share_axis": "Share in %",
        "cases_finding": ("Recorded cybercrime rose from **{first}** cases in 2016 to a peak of **{peak}** in "
                          "{peak_year} and has fallen in every year since. In 2025 the police recorded **{last}** "
                          "cases: **{vs_peak} %** against the peak and **+{vs_first} %** against 2016. All recorded "
                          "crime fell by {all_change} % in the same period."),
        "clearance_title": "Clearance rate: cybercrime and all recorded crime",
        "clearance_axis": "Clearance rate in %",
        "series_cyber": "Cybercrime",
        "series_all": "All recorded crime",
        "clearance_finding": ("The police cleared **{c_first} %** of the cybercrime cases in 2016 and **{c_last} %** "
                              "in 2025. The rate of all recorded crime stayed between {a_min} % and {a_max} %. "
                              "The gap grew from **{gap_first}** to **{gap_last}** percentage points."),
        "clearance_note": ("Clearance rates before 2021 are calculated from the rates of the four offence keys. "
                           "Until 2018 the BKA publishes them with one decimal place, so these values are rounded."),
        "cleared_title": "Recorded and cleared cybercrime cases",
        "cleared_axis": "Cases",
        "series_recorded": "Recorded cases",
        "series_cleared": "Cleared cases",
        "measure": "Measure",
        "m_rate": "Cases per 100,000 inhabitants",
        "m_cases": "Recorded cases",
        "m_clearance": "Clearance rate in %",
        "view": "View",
        "v_compare": "2016 and 2025",
        "v_2025": "Ranking 2025",
        "v_2016": "Ranking 2016",
        "highlight": "Highlight states",
        "placeholder": "All states",
        "states_title": "{measure} by federal state",
        "states_finding": ("In 2025 **{high}** recorded **{high_value}** cybercrime cases per 100,000 inhabitants and "
                           "**{low}** **{low_value}**, a factor of **{factor}**. Berlin, Bremen and Hamburg hold "
                           "ranks 1 to 3 in both 2016 and 2025. The rate rose in {up} states and fell in {down}.\n\n"
                           "The three states with the highest rates have the three lowest clearance rates in 2025: "
                           "{low_clear}. The rate is highest in {top_clear_state} at {top_clear} %."),
        "states_warning": ("The tables do not show why the states differ this much, and the BKA notes on the PKS 2025 "
                           "list no special circumstance for any state in this field. In general the BKA points "
                           "out that high rates of increase are partly due to investigation complexes with "
                           "numerous individual cases. The 2016 rates use the "
                           "census of 2011, the 2025 rates the census of 2022."),
        "table": "Table",
        "col_state": "Federal state",
        "col_change": "Change of rate in %",
        "col_rank": "Rank {year}",
        "definition_h": "Definition of cybercrime",
        "definition": ("Which offences count as cybercrime is not defined in this project. The BKA definition is "
                       "used: aggregate key **897000 Cybercrime** (PKS 2025, overview of aggregate keys, page 9)."),
        "def_key": "Key", "def_offence": "Offence", "def_law": "German Criminal Code",
        "def_rows": [("543000", "Forgery of data intended to provide proof, deception in legal commerce through data processing", "§§ 269, 270 StGB"),
                     ("674200", "Data tampering, computer sabotage", "§§ 303a, 303b StGB"),
                     ("678000", "Data espionage and interception of data including preparatory acts, handling of stolen data", "§§ 202a to 202d StGB"),
                     ("897100", "Computer fraud", "§ 263a StGB")],
        "method_h": "Method",
        "method": ("- **Same definition in all years.** Until 2020 the published key 897000 also contained software "
                   "piracy (keys 715100 and 715200). Cybercrime is therefore calculated as the sum of the four "
                   "offence keys in every year.\n"
                   "- **Start in 2016.** The key for computer fraud (897100) was introduced in 2016. The BKA marks "
                   "the cybercrime figures of 2016 as not comparable with 2015.\n"
                   "- **Federal states.** 2025: key 897000 as published. 2016: sum of the four keys per state; the "
                   "rate per 100,000 inhabitants is recalculated with the population of 2016, derived from the "
                   "BKA table."),
        "limits_h": "Limitations",
        "limits": ("- **Recorded crime only.** The PKS counts cases known to the police. According to the BKA, "
                   "studies estimate the unreported share of cybercrime at up to 91.5 %. The BKA writes that the "
                   "PKS therefore has only limited informative value for the offences actually committed and is "
                   "suited mainly for statements on the trend ([Bundeslagebild Cybercrime 2022](https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/JahresberichteUndLagebilder/Cybercrime/cybercrimeBundeslagebild2022.pdf?__blob=publicationFile&v=4), page 4).\n"
                   "- **Offences committed in Germany only.** Since 2014 a cybercrime case is counted only when "
                   "there are concrete indications that the act was carried out in Germany. Offences committed "
                   "from abroad are recorded separately and are not included.\n"
                   "- **Narrow definition.** More than 80 % of the cases are computer fraud. Offences committed "
                   "with the internet as a tool are published by the BKA in a separate table, which is not "
                   "analysed here.\n"
                   "- **Population basis.** Rates for 2016 are based on the census of 2011, rates for 2025 on the "
                   "census of 2022. According to the BKA they are comparable only to a limited extent.\n"
                   "- **Two points in time for the states.** The comparison shows 2016 and 2025, not the years "
                   "in between."),
        "sources_h": "Data sources",
        "sources_intro": ("All data: Federal Criminal Police Office (Bundeskriminalamt, BKA), Police Crime "
                          "Statistics (Polizeiliche Kriminalstatistik, PKS). Figures on cybercrime before 2021, "
                          "clearance rates before 2021 and the state rates for 2016 are own calculations based "
                          "on these tables."),
        "src_used": "Used for", "src_table": "Table or document", "src_version": "Version",
        "src_rows": [("Cases and clearance rate, federal level", "PKS 2025, time series, T01 Grundtabelle – Fälle ab 1987", "V1.1, 8 April 2026"),
                     ("Federal states 2025", "PKS 2025, T01 Grundtabelle – Fälle mit Häufigkeitszahl (HZ) – Länder", "V1.0, 6 March 2026"),
                     ("Federal states 2016", "PKS 2016, T01 Grundtabelle – Länder", "27 January 2017"),
                     ("BKA notes on comparability and rates of increase", "PKS 2016, T01 Grundtabelle – Länder – Fallentwicklung", "1 February 2017"),
                     ("Definition of cybercrime", "PKS 2025 – Übersicht Summenschlüssel, page 9", "V1.0"),
                     ("Changes of recording and keys", "PKS 2025 – Hinweise zu den Zeitreihen, pages 19, 23 and 40", "V1.0"),
                     ("Population basis, notes on the states", "PKS 2025 – Wichtige Hinweise zur Interpretation der Daten, pages 4 to 6", "V1.0")],
        "context_h": "What the BKA says about the development",
        "context": ("The statistics show the development, not its causes. The BKA comments on them in its "
                    "situation reports:\n"
                    "- **Rise until 2021.** The BKA links it to the further accelerated digitalisation, driven "
                    "among other things by the COVID-19 pandemic, which creates many new opportunities for "
                    "cybercriminals ([BKA press release, 9 May 2022](https://www.presseportal.de/blaulicht/pm/7/5217298)).\n"
                    "- **Decline in 2022.** The BKA explains it with the easing of the pandemic measures: online "
                    "shopping and remote work had offered additional opportunities for attacks in the years "
                    "before, and in 2022 part of the crime moved back into the analogue world "
                    "([Bundeslagebild Cybercrime 2022](https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/JahresberichteUndLagebilder/Cybercrime/cybercrimeBundeslagebild2022.pdf?__blob=publicationFile&v=4), page 7).\n"
                    "- **Russia's war against Ukraine.** The war began on 24 February 2022. The BKA writes that "
                    "it led to a heightened cyber threat situation in Germany as well (page 22). The cases "
                    "recorded in the PKS nevertheless fell in 2022.\n"
                    "- **Offences committed from abroad.** The BKA calls the decline in 2022 an apparent one. "
                    "Offences with damage in Germany and an offender abroad or at an unknown location rose by "
                    "more than 8 % in 2022, while the cases recorded in Germany fell by 6.5 % (page 6). Those "
                    "offences are not part of these figures."),
        "groups_title": "Cybercrime per 100,000 inhabitants by offence group, {year}",
        "groups_axis": "Recorded cases per 100,000 inhabitants",
        "groups_year": "Year",
        "groups_note": ("The differences between the states come mainly from fraud with means of payment and goods "
                        "ordered on credit. The three cybercrime offences outside computer fraud range from 9 to 47 "
                        "cases per 100,000 inhabitants in 2025, payment card data from 3.5 to 145 and other non-cash "
                        "means of payment from 1 to 257. The breakdown shows where the differences are, not why "
                        "they exist."),
        "groups": {"Goods credit fraud": "Goods credit fraud", "Payment cards with PIN": "Payment cards with PIN",
                   "Payment card data": "Payment card data",
                   "Other non-cash means of payment": "Other non-cash means of payment",
                   "Other computer fraud": "Other computer fraud",
                   "Other cybercrime offences": "Other cybercrime offences"},
        "bremen_h": "Why is Bremen so high?",
        "bremen": ("Bremen stands out even among the three city states. Almost half of its value comes from one "
                   "offence key: computer fraud with unlawfully obtained other non-cash means of payment "
                   "(key 516920). In 2025 Bremen recorded **1,809** such cases or **257** per 100,000 "
                   "inhabitants, **17 times** the national rate of 15. Berlin and Hamburg are at 11. Without "
                   "this key Bremen would be at about **306** per 100,000, below Hamburg and Berlin.\n\n"
                   "Why this key is so high in Bremen in particular does not follow from the PKS tables. The rise "
                   "is not new: for 2022 the Weser-Kurier reported that computer fraud with stolen non-cash means "
                   "of payment in Bremen had more than doubled within one year, from 968 to 2,136 cases. According "
                   "to the report, the Bremen State Criminal Police Office sees this rise favoured by the growing "
                   "use of electronic payment methods such as Apple Pay and Google Pay "
                   "([Weser-Kurier, 6 March 2023](https://www.weser-kurier.de/bremen/politik/bremer-kriminalstatistik-immer-mehr-digitale-straftaten-doc7p7nodmh7tg1b8franvb)). " "The calculation is in Section 9 of the notebook."),
        "context_sources_h": "Further sources for context",
        "context_sources": ("- [BKA, press release on the Bundeslagebild Cybercrime 2021, 9 May 2022](https://www.presseportal.de/blaulicht/pm/7/5217298)\n"
                            "- [BKA, Bundeslagebild Cybercrime 2022, pages 4 to 7 and 22](https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/JahresberichteUndLagebilder/Cybercrime/cybercrimeBundeslagebild2022.pdf?__blob=publicationFile&v=4)\n"
                            "- [Weser-Kurier, report on the Bremen crime statistics 2022, 6 March 2023](https://www.weser-kurier.de/bremen/politik/bremer-kriminalstatistik-immer-mehr-digitale-straftaten-doc7p7nodmh7tg1b8franvb)"),
        "download_h": "Download the data",
        "download_federal": "Federal table (CSV)",
        "download_states": "State table (CSV)",
        "chart_source": "Source: BKA, Police Crime Statistics. Own calculation.",
        "missing": "Data files not found in `data/clean`. Run the notebook first.",
        "footer": ("© 2026 Amirhoushang Rahmannejad. All rights reserved. "
                   "Data: Federal Criminal Police Office (BKA), Police Crime Statistics."),
    },
    "de": {
        "title": "Cybercrime in Deutschland",
        "subtitle": "Erfasste Fälle, Aufklärungsquote und Unterschiede zwischen den Bundesländern, 2016 bis 2025",
        "intro": ("Grundlage ist die Polizeiliche Kriminalstatistik (PKS) des Bundeskriminalamts (BKA). "
                  "Cybercrime folgt der Abgrenzung des BKA: Summenschlüssel 897000, berechnet als Summe der "
                  "Straftatenschlüssel 543000, 674200, 678000 und 897100. Die Zahlen enthalten nur Fälle, die "
                  "der Polizei angezeigt und in Deutschland begangen wurden."),
        "language": "Sprache",
        "kpi_cases": "Erfasste Fälle {year}",
        "kpi_cases_delta": "{value} seit {year}",
        "kpi_clearance": "Aufklärungsquote {year}",
        "kpi_clearance_delta": "{value} Punkte ggü. insgesamt",
        "kpi_share": "Anteil an allen Straftaten",
        "kpi_share_delta": "{value} Punkte seit {year}",
        "kpi_spread": "Höchstes ggü. niedrigstem Land",
        "kpi_spread_value": "Faktor {value}",
        "kpi_spread_delta": "{high} ggü. {low}",
        "tab_cases": "Fallzahlen",
        "tab_clearance": "Aufklärungsquote",
        "tab_states": "Bundesländer",
        "tab_sources": "Methode und Quellen",
        "years": "Jahre",
        "cases_title": "Erfasste Fälle von Cybercrime",
        "cases_axis": "Erfasste Fälle",
        "share_title": "Anteil von Cybercrime an allen erfassten Straftaten",
        "share_axis": "Anteil in %",
        "cases_finding": ("Die erfassten Fälle stiegen von **{first}** im Jahr 2016 auf den Höchstwert von "
                          "**{peak}** im Jahr {peak_year} und sind seitdem in jedem Jahr gesunken. 2025 erfasste "
                          "die Polizei **{last}** Fälle: **{vs_peak} %** gegenüber dem Höchstwert und "
                          "**+{vs_first} %** gegenüber 2016. Die Straftaten insgesamt gingen im selben Zeitraum "
                          "um {all_change} % zurück."),
        "clearance_title": "Aufklärungsquote: Cybercrime und Straftaten insgesamt",
        "clearance_axis": "Aufklärungsquote in %",
        "series_cyber": "Cybercrime",
        "series_all": "Straftaten insgesamt",
        "clearance_finding": ("Die Polizei klärte 2016 **{c_first} %** der Cybercrime-Fälle auf, 2025 **{c_last} %**. "
                              "Die Quote der Straftaten insgesamt lag durchgehend zwischen {a_min} % und {a_max} %. "
                              "Der Abstand wuchs von **{gap_first}** auf **{gap_last}** Prozentpunkte."),
        "clearance_note": ("Die Aufklärungsquoten vor 2021 sind aus den Quoten der vier Straftatenschlüssel "
                           "berechnet. Bis 2018 veröffentlicht das BKA sie mit einer Nachkommastelle, diese Werte "
                           "sind daher gerundet."),
        "cleared_title": "Erfasste und aufgeklärte Fälle von Cybercrime",
        "cleared_axis": "Fälle",
        "series_recorded": "Erfasste Fälle",
        "series_cleared": "Aufgeklärte Fälle",
        "measure": "Kennzahl",
        "m_rate": "Fälle je 100.000 Einwohner",
        "m_cases": "Erfasste Fälle",
        "m_clearance": "Aufklärungsquote in %",
        "view": "Ansicht",
        "v_compare": "2016 und 2025",
        "v_2025": "Rangliste 2025",
        "v_2016": "Rangliste 2016",
        "highlight": "Länder hervorheben",
        "placeholder": "Alle Länder",
        "states_title": "{measure} nach Bundesland",
        "states_finding": ("2025 erfasste **{high}** **{high_value}** Cybercrime-Fälle je 100.000 Einwohner, "
                           "**{low}** **{low_value}**. Das ist der Faktor **{factor}**. Berlin, Bremen und Hamburg "
                           "belegen 2016 und 2025 die Plätze 1 bis 3. Die Häufigkeitszahl stieg in {up} Ländern "
                           "und sank in {down}.\n\n"
                           "Die drei Länder mit den höchsten Häufigkeitszahlen haben 2025 die drei niedrigsten "
                           "Aufklärungsquoten: {low_clear}. Am höchsten ist die Quote in {top_clear_state} mit "
                           "{top_clear} %."),
        "states_warning": ("Die Tabellen zeigen nicht, warum sich die Länder so stark unterscheiden, und die Hinweise "
                           "des BKA zur PKS 2025 nennen für kein Land eine Besonderheit in diesem Bereich. "
                           "Allgemein weist das BKA darauf hin, dass hohe Steigerungsraten zum Teil auf "
                           "Ermittlungskomplexe mit zahlreichen Einzelfällen zurückgehen. Die "
                           "Werte für 2016 beruhen auf dem Zensus 2011, die Werte für 2025 auf dem Zensus 2022."),
        "table": "Tabelle",
        "col_state": "Bundesland",
        "col_change": "Veränderung der Häufigkeitszahl in %",
        "col_rank": "Rang {year}",
        "definition_h": "Abgrenzung von Cybercrime",
        "definition": ("Welche Straftaten zu Cybercrime zählen, legt dieses Projekt nicht selbst fest. Es gilt die "
                       "Abgrenzung des BKA: Summenschlüssel **897000 Cybercrime** (PKS 2025, Übersicht "
                       "Summenschlüssel, Seite 9)."),
        "def_key": "Schlüssel", "def_offence": "Straftat", "def_law": "Strafgesetzbuch",
        "def_rows": [("543000", "Fälschung beweiserheblicher Daten, Täuschung im Rechtsverkehr bei Datenverarbeitung", "§§ 269, 270 StGB"),
                     ("674200", "Datenveränderung, Computersabotage", "§§ 303a, 303b StGB"),
                     ("678000", "Ausspähen, Abfangen von Daten einschl. Vorbereitungshandlungen und Datenhehlerei", "§§ 202a bis 202d StGB"),
                     ("897100", "Computerbetrug", "§ 263a StGB")],
        "method_h": "Methode",
        "method": ("- **Gleiche Abgrenzung in allen Jahren.** Bis 2020 enthielt der veröffentlichte Schlüssel "
                   "897000 zusätzlich die Softwarepiraterie (Schlüssel 715100 und 715200). Cybercrime wird "
                   "deshalb in jedem Jahr als Summe der vier Straftatenschlüssel berechnet.\n"
                   "- **Beginn 2016.** Der Schlüssel für Computerbetrug (897100) wurde 2016 eingeführt. Das BKA "
                   "kennzeichnet die Cybercrime-Zahlen von 2016 als nicht vergleichbar mit 2015.\n"
                   "- **Bundesländer.** 2025: Schlüssel 897000 wie veröffentlicht. 2016: Summe der vier Schlüssel "
                   "je Land; die Häufigkeitszahl ist mit der Einwohnerzahl von 2016 neu berechnet, abgeleitet "
                   "aus der BKA-Tabelle."),
        "limits_h": "Grenzen der Daten",
        "limits": ("- **Nur das Hellfeld.** Die PKS zählt Fälle, die der Polizei bekannt wurden. Das Dunkelfeld "
                   "bei Cybercrime wird nach Angaben des BKA in Studien auf bis zu 91,5 % geschätzt. Das BKA "
                   "schreibt, die PKS habe deshalb nur eine begrenzte Aussagekraft für die tatsächlich verübten "
                   "Straftaten und eigne sich vor allem für Aussagen zum Trend "
                   "([Bundeslagebild Cybercrime 2022](https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/JahresberichteUndLagebilder/Cybercrime/cybercrimeBundeslagebild2022.pdf?__blob=publicationFile&v=4), Seite 4).\n"
                   "- **Nur Taten in Deutschland.** Seit 2014 wird ein Cybercrime-Fall nur gezählt, wenn konkrete "
                   "Anhaltspunkte für eine Tathandlung in Deutschland vorliegen. Auslandstaten werden getrennt "
                   "erfasst und sind hier nicht enthalten.\n"
                   "- **Enge Abgrenzung.** Mehr als 80 % der Fälle sind Computerbetrug. Straftaten mit dem "
                   "Tatmittel Internet weist das BKA in einer eigenen Tabelle aus, die hier nicht "
                   "ausgewertet wird.\n"
                   "- **Bevölkerungsbasis.** Die Häufigkeitszahlen für 2016 beruhen auf dem Zensus 2011, die für "
                   "2025 auf dem Zensus 2022. Laut BKA sind sie nur eingeschränkt vergleichbar.\n"
                   "- **Zwei Zeitpunkte bei den Ländern.** Der Vergleich zeigt 2016 und 2025, nicht die Jahre "
                   "dazwischen."),
        "sources_h": "Datenquellen",
        "sources_intro": ("Alle Daten: Bundeskriminalamt (BKA), Polizeiliche Kriminalstatistik (PKS). Die Zahlen "
                          "zu Cybercrime vor 2021, die Aufklärungsquoten vor 2021 und die Häufigkeitszahlen der "
                          "Länder für 2016 sind eigene Berechnungen auf Grundlage dieser Tabellen."),
        "src_used": "Verwendet für", "src_table": "Tabelle oder Dokument", "src_version": "Stand",
        "src_rows": [("Fälle und Aufklärungsquote, Bund", "PKS 2025, Zeitreihen, T01 Grundtabelle – Fälle ab 1987", "V1.1, 08.04.2026"),
                     ("Bundesländer 2025", "PKS 2025, T01 Grundtabelle – Fälle mit Häufigkeitszahl (HZ) – Länder", "V1.0, 06.03.2026"),
                     ("Bundesländer 2016", "PKS 2016, T01 Grundtabelle – Länder", "27.01.2017"),
                     ("Hinweise des BKA zur Vergleichbarkeit und zu Steigerungsraten", "PKS 2016, T01 Grundtabelle – Länder – Fallentwicklung", "01.02.2017"),
                     ("Abgrenzung von Cybercrime", "PKS 2025 – Übersicht Summenschlüssel, Seite 9", "V1.0"),
                     ("Änderungen bei Erfassung und Schlüsseln", "PKS 2025 – Hinweise zu den Zeitreihen, Seiten 19, 23 und 40", "V1.0"),
                     ("Bevölkerungsbasis, Hinweise zu den Ländern", "PKS 2025 – Wichtige Hinweise zur Interpretation der Daten, Seiten 4 bis 6", "V1.0")],
        "context_h": "Was das BKA zur Entwicklung sagt",
        "context": ("Die Statistik zeigt die Entwicklung, nicht ihre Ursachen. Dazu äußert sich das BKA in seinen "
                    "Lagebildern:\n"
                    "- **Anstieg bis 2021.** Das BKA verbindet ihn mit der weiter beschleunigten Digitalisierung, "
                    "unter anderem durch die Corona-Pandemie, die viele neue Tatgelegenheiten für Cyberkriminelle "
                    "schaffe ([Pressemitteilung des BKA, 9. Mai 2022](https://www.presseportal.de/blaulicht/pm/7/5217298)).\n"
                    "- **Rückgang 2022.** Das BKA begründet ihn mit der Lockerung der Corona-Schutzmaßnahmen: "
                    "Onlinehandel und mobiles Arbeiten hätten in den Vorjahren zusätzliche Angriffsmöglichkeiten "
                    "geboten, 2022 habe sich ein Teil des Kriminalitätsgeschehens wieder in die analoge Welt "
                    "verlagert ([Bundeslagebild Cybercrime 2022](https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/JahresberichteUndLagebilder/Cybercrime/cybercrimeBundeslagebild2022.pdf?__blob=publicationFile&v=4), Seite 7).\n"
                    "- **Russlands Krieg gegen die Ukraine.** Der Krieg begann am 24. Februar 2022. Das BKA "
                    "schreibt, er habe auch in Deutschland zu einer erhöhten Cyber-Bedrohungslage geführt "
                    "(Seite 22). Die in der PKS erfassten Fälle gingen 2022 dennoch zurück.\n"
                    "- **Auslandstaten.** Das BKA nennt den Rückgang 2022 „scheinbar“. Taten mit Schaden in "
                    "Deutschland und Täter im Ausland oder an unbekanntem Ort nahmen 2022 um über 8 % zu, während "
                    "die in Deutschland erfassten Fälle um 6,5 % sanken (Seite 6). Diese Taten sind in den Zahlen "
                    "hier nicht enthalten."),
        "groups_title": "Cybercrime je 100.000 Einwohner nach Deliktgruppe, {year}",
        "groups_axis": "Erfasste Fälle je 100.000 Einwohner",
        "groups_year": "Jahr",
        "groups_note": ("Die Unterschiede zwischen den Ländern kommen vor allem aus dem Betrug mit Zahlungsmitteln "
                        "und mit Waren auf Kredit. Die drei Cybercrime-Delikte außerhalb des Computerbetrugs liegen "
                        "2025 zwischen 9 und 47 Fällen je 100.000 Einwohner, die Fälle mit Kartendaten zwischen 3,5 "
                        "und 145 und die mit sonstigen unbaren Zahlungsmitteln zwischen 1 und 257. Die "
                        "Aufschlüsselung zeigt, wo die Unterschiede liegen, nicht warum es sie gibt."),
        "groups": {"Goods credit fraud": "Warenkreditbetrug", "Payment cards with PIN": "Zahlungskarten mit PIN",
                   "Payment card data": "Daten von Zahlungskarten",
                   "Other non-cash means of payment": "Sonstige unbare Zahlungsmittel",
                   "Other computer fraud": "Sonstiger Computerbetrug",
                   "Other cybercrime offences": "Übrige Cybercrime-Delikte"},
        "bremen_h": "Warum liegt Bremen so hoch?",
        "bremen": ("Bremen fällt selbst unter den drei Stadtstaaten auf. Fast die Hälfte des Bremer Werts kommt "
                   "aus einem einzigen Straftatenschlüssel: Computerbetrug mittels rechtswidrig erlangter "
                   "sonstiger unbarer Zahlungsmittel (Schlüssel 516920). 2025 erfasste Bremen **1.809** solcher "
                   "Fälle, das sind **257** je 100.000 Einwohner und das **17-Fache** des Bundeswerts von 15. "
                   "Berlin und Hamburg liegen bei 11. Ohne diesen Schlüssel läge Bremen bei rund **306** je "
                   "100.000, unter Hamburg und Berlin.\n\n"
                   "Warum dieser Schlüssel gerade in Bremen so hoch ist, geht aus den PKS-Tabellen nicht hervor. "
                   "Der Anstieg ist nicht neu: Schon für 2022 berichtete der Weser-Kurier, der Computerbetrug mit "
                   "gestohlenen unbaren Zahlungsmitteln habe sich in Bremen binnen eines Jahres mehr als "
                   "verdoppelt, von 968 auf 2.136 Fälle. Nach dem Bericht sieht das Bremer Landeskriminalamt "
                   "diesen Anstieg begünstigt durch die zunehmende Verbreitung elektronischer Zahlungsmethoden "
                   "wie Apple Pay und Google Pay ([Weser-Kurier, 6. März 2023](https://www.weser-kurier.de/bremen/politik/bremer-kriminalstatistik-immer-mehr-digitale-straftaten-doc7p7nodmh7tg1b8franvb)). "
                   "Die Rechnung steht in Abschnitt 9 des Notebooks."),
        "context_sources_h": "Weitere Quellen zur Einordnung",
        "context_sources": ("- [BKA, Pressemitteilung zum Bundeslagebild Cybercrime 2021, 9. Mai 2022](https://www.presseportal.de/blaulicht/pm/7/5217298)\n"
                            "- [BKA, Bundeslagebild Cybercrime 2022, Seiten 4 bis 7 und 22](https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/JahresberichteUndLagebilder/Cybercrime/cybercrimeBundeslagebild2022.pdf?__blob=publicationFile&v=4)\n"
                            "- [Weser-Kurier, Bericht zur Bremer Kriminalstatistik 2022, 6. März 2023](https://www.weser-kurier.de/bremen/politik/bremer-kriminalstatistik-immer-mehr-digitale-straftaten-doc7p7nodmh7tg1b8franvb)"),
        "download_h": "Daten herunterladen",
        "download_federal": "Tabelle Bund (CSV)",
        "download_states": "Tabelle Länder (CSV)",
        "chart_source": "Quelle: BKA, Polizeiliche Kriminalstatistik. Eigene Berechnung.",
        "missing": "Datendateien in `data/clean` nicht gefunden. Bitte zuerst das Notebook ausführen.",
        "footer": ("© 2026 Amirhoushang Rahmannejad. Alle Rechte vorbehalten. "
                   "Daten: Bundeskriminalamt (BKA), Polizeiliche Kriminalstatistik."),
    },
}


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    federal = pd.read_csv(DATA_CLEAN / "cybercrime_federal.csv", index_col="year")
    states = pd.read_csv(DATA_CLEAN / "cybercrime_states.csv", index_col="state")
    return federal, states


def fmt(value, decimals=0, signed=False):
    """Format a number in the style of the selected language (1,234.5 or 1.234,5)."""
    text = f"{value:+,.{decimals}f}" if signed else f"{value:,.{decimals}f}"
    if LANG == "de":
        text = text.replace(",", "§").replace(".", ",").replace("§", ".")
    return text


def base_layout(fig, title, y_title=None, x_title=None, height=420):
    """Shared chart layout: left-aligned title, quiet grid, legend on top."""
    fig.update_layout(
        title=dict(text=title, x=0, xanchor="left", font=dict(size=17)),
        height=height, margin=dict(l=10, r=20, t=70, b=40),
        separators=",." if LANG == "de" else ".,",
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0),
        hoverlabel=dict(font_size=13),
        yaxis_title=y_title, xaxis_title=x_title,
    )
    return fig


def show(fig):
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.caption(T["chart_source"])


# ----------------------------------------------------------------------------
# Language, colours and data
# ----------------------------------------------------------------------------
with st.sidebar:
    choice = st.radio("Language / Sprache", ["English", "Deutsch"], horizontal=True)
LANG = "de" if choice == "Deutsch" else "en"
T = TEXT[LANG]

# Series colours for the light and the dark theme (checked for colour-blind safety)
try:
    DARK = st.context.theme.type == "dark"
except Exception:
    DARK = False
BLUE = "#3987e5" if DARK else "#2a78d6"        # cybercrime, 2025
ORANGE = "#d95926" if DARK else "#eb6834"      # all recorded crime
BLUE_SOFT = "#1f4f8a" if DARK else "#a9c9f0"   # 2016, lighter shade of the same hue
GREY = "#6b6b68" if DARK else "#c9c8c2"        # states that are not highlighted
# Six offence groups, fixed order (light and dark theme)
GROUP_COLORS = (["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#9085e9"] if DARK
                else ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#4a3aa7"])

if not (DATA_CLEAN / "cybercrime_federal.csv").exists():
    st.error(T["missing"])
    st.stop()
federal, states = load_data()
# Show the state names in the selected language (the CSV may hold German or English names)
states = states.rename(index=STATE_NAMES_DE)
if LANG == "en":
    states = states.rename(index=STATE_NAMES_EN)

# ----------------------------------------------------------------------------
# Header and key figures
# ----------------------------------------------------------------------------
st.title(T["title"])
st.markdown(f"**{T['subtitle']}**")
st.markdown(T["intro"])

first, last = federal.loc[FIRST_YEAR], federal.loc[LAST_YEAR]
top_state, bottom_state = states["rate_2025"].idxmax(), states["rate_2025"].idxmin()

k1, k2, k3, k4 = st.columns(4)
k1.metric(T["kpi_cases"].format(year=LAST_YEAR), fmt(last["cases"]),
          T["kpi_cases_delta"].format(value=fmt(100 * (last["cases"] / first["cases"] - 1), 1, True) + " %",
                                      year=FIRST_YEAR), delta_color="off", delta_arrow="off")
k2.metric(T["kpi_clearance"].format(year=LAST_YEAR), fmt(last["clearance_rate"], 1) + " %",
          T["kpi_clearance_delta"].format(
              value=fmt(last["clearance_rate"] - last["clearance_rate_all_crime"], 1, True)), delta_color="off", delta_arrow="off")
k3.metric(T["kpi_share"], fmt(last["share_of_all_crime_pct"], 1) + " %",
          T["kpi_share_delta"].format(
              value=fmt(last["share_of_all_crime_pct"] - first["share_of_all_crime_pct"], 1, True),
              year=FIRST_YEAR), delta_color="off", delta_arrow="off")
k4.metric(T["kpi_spread"],
          T["kpi_spread_value"].format(value=fmt(states["rate_2025"].max() / states["rate_2025"].min(), 1)),
          help=T["kpi_spread_delta"].format(high=top_state, low=bottom_state))

tab_cases, tab_clearance, tab_states, tab_sources = st.tabs(
    [T["tab_cases"], T["tab_clearance"], T["tab_states"], T["tab_sources"]])

# ----------------------------------------------------------------------------
# Tab 1: cases
# ----------------------------------------------------------------------------
with tab_cases:
    year_from, year_to = st.slider(T["years"], FIRST_YEAR, LAST_YEAR, (FIRST_YEAR, LAST_YEAR), key="years_cases")
    data = federal.loc[year_from:year_to]

    fig = go.Figure(go.Bar(
        x=data.index, y=data["cases"], marker_color=BLUE, name=T["series_cyber"],
        text=[fmt(v) for v in data["cases"]], textposition="outside", cliponaxis=False,
        hovertemplate="%{x}: %{y:,.0f}<extra></extra>"))
    base_layout(fig, T["cases_title"], T["cases_axis"])
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(tickformat=",.0f", rangemode="tozero")
    show(fig)

    peak_year = federal["cases"].idxmax()
    st.markdown(T["cases_finding"].format(
        first=fmt(first["cases"]), peak=fmt(federal["cases"].max()), peak_year=peak_year, last=fmt(last["cases"]),
        vs_peak=fmt(100 * (last["cases"] / federal["cases"].max() - 1), 1),
        vs_first=fmt(100 * (last["cases"] / first["cases"] - 1), 1),
        all_change=fmt(abs(100 * (last["cases_all_crime"] / first["cases_all_crime"] - 1)), 1)))
    with st.expander(T["context_h"]):
        st.markdown(T["context"])

    fig = go.Figure(go.Scatter(
        x=data.index, y=data["share_of_all_crime_pct"], mode="lines+markers", name=T["series_cyber"],
        line=dict(color=BLUE, width=2), marker=dict(size=8),
        hovertemplate="%{x}: %{y:.2f} %<extra></extra>"))
    base_layout(fig, T["share_title"], T["share_axis"], height=320)
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(rangemode="tozero", ticksuffix=" %")
    show(fig)

# ----------------------------------------------------------------------------
# Tab 2: clearance rate
# ----------------------------------------------------------------------------
with tab_clearance:
    year_from, year_to = st.slider(T["years"], FIRST_YEAR, LAST_YEAR, (FIRST_YEAR, LAST_YEAR), key="years_clear")
    data = federal.loc[year_from:year_to]

    fig = go.Figure()
    for column, name, color in [("clearance_rate_all_crime", T["series_all"], ORANGE),
                                ("clearance_rate", T["series_cyber"], BLUE)]:
        fig.add_trace(go.Scatter(
            x=data.index, y=data[column], mode="lines+markers", name=name,
            line=dict(color=color, width=2), marker=dict(size=8),
            hovertemplate=name + " %{x}: %{y:.1f} %<extra></extra>"))
    base_layout(fig, T["clearance_title"], T["clearance_axis"])
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(range=[0, 70], ticksuffix=" %")
    fig.update_layout(hovermode="x unified")
    show(fig)

    gap = federal["clearance_rate_all_crime"] - federal["clearance_rate"]
    st.markdown(T["clearance_finding"].format(
        c_first=fmt(first["clearance_rate"], 1), c_last=fmt(last["clearance_rate"], 1),
        a_min=fmt(federal["clearance_rate_all_crime"].min(), 1), a_max=fmt(federal["clearance_rate_all_crime"].max(), 1),
        gap_first=fmt(gap[FIRST_YEAR], 1), gap_last=fmt(gap[LAST_YEAR], 1)))

    # Recorded vs. cleared cases: shows that the rate fell because recorded cases grew
    fig = go.Figure()
    for column, name, color in [("cases", T["series_recorded"], BLUE_SOFT), ("cleared", T["series_cleared"], BLUE)]:
        fig.add_trace(go.Bar(x=data.index, y=data[column], name=name, marker_color=color,
                             hovertemplate=name + " %{x}: %{y:,.0f}<extra></extra>"))
    base_layout(fig, T["cleared_title"], T["cleared_axis"], height=340)
    fig.update_layout(barmode="group", bargap=0.25)
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(tickformat=",.0f")
    show(fig)
    st.caption(T["clearance_note"])

# ----------------------------------------------------------------------------
# Tab 3: federal states
# ----------------------------------------------------------------------------
with tab_states:
    measures = {T["m_rate"]: ("rate", 0), T["m_cases"]: ("cases", 0), T["m_clearance"]: ("clearance_rate", 1)}
    c1, c2, c3 = st.columns([2, 2, 3])
    measure_label = c1.selectbox(T["measure"], list(measures))
    view = c2.radio(T["view"], [T["v_compare"], T["v_2025"], T["v_2016"]], horizontal=True)
    highlight = c3.multiselect(T["highlight"], sorted(states.index), placeholder=T["placeholder"])
    column, decimals = measures[measure_label]
    col_2016, col_2025 = f"{column}_2016", f"{column}_2025"

    sort_col = col_2016 if view == T["v_2016"] else col_2025
    data = states.sort_values(sort_col)                       # smallest value at the bottom
    # Colour follows the state: highlighted states keep the series colour, the others turn grey
    colors = [BLUE if (not highlight or s in highlight) else GREY for s in data.index]
    suffix = " %" if column == "clearance_rate" else ""

    fig = go.Figure()
    if view == T["v_compare"]:
        # One connecting line per state from the 2016 value to the 2025 value
        for state, row in data.iterrows():
            fig.add_shape(type="line", x0=row[col_2016], x1=row[col_2025], y0=state, y1=state,
                          line=dict(color=GREY, width=2), layer="below")
        fig.add_trace(go.Scatter(
            x=data[col_2016], y=data.index, mode="markers", name="2016",
            marker=dict(color=BLUE_SOFT, size=11, line=dict(color=BLUE, width=1)),
            hovertemplate="%{y} 2016: %{x:,." + str(decimals) + "f}" + suffix + "<extra></extra>"))
        fig.add_trace(go.Scatter(
            x=data[col_2025], y=data.index, mode="markers", name="2025",
            marker=dict(color=colors, size=13),
            hovertemplate="%{y} 2025: %{x:,." + str(decimals) + "f}" + suffix + "<extra></extra>"))
    else:
        fig.add_trace(go.Bar(
            x=data[sort_col], y=data.index, orientation="h", marker_color=colors, name=sort_col[-4:],
            text=[fmt(v, decimals) + suffix for v in data[sort_col]], textposition="outside", cliponaxis=False,
            hovertemplate="%{y}: %{x:,." + str(decimals) + "f}" + suffix + "<extra></extra>"))
    base_layout(fig, T["states_title"].format(measure=measure_label), x_title=measure_label, height=560)
    fig.update_xaxes(rangemode="tozero", tickformat=",.0f", ticksuffix=suffix)
    fig.update_layout(showlegend=view == T["v_compare"])
    show(fig)

    st.markdown(T["states_finding"].format(
        high=top_state, high_value=fmt(states.loc[top_state, "rate_2025"]),
        low=bottom_state, low_value=fmt(states.loc[bottom_state, "rate_2025"]),
        factor=fmt(states["rate_2025"].max() / states["rate_2025"].min(), 1),
        up=int((states["rate_change_pct"] > 0).sum()), down=int((states["rate_change_pct"] < 0).sum()),
        low_clear=", ".join(f"{name} {fmt(value, 1)} %" for name, value in
                            states["clearance_rate_2025"].nsmallest(3).items()),
        top_clear_state=states["clearance_rate_2025"].idxmax(),
        top_clear=fmt(states["clearance_rate_2025"].max(), 1)))
    st.warning(T["states_warning"])

    # Offence groups: stacked bars per state, one colour per group (file is optional)
    offences_file = DATA_CLEAN / "cybercrime_states_offences.csv"
    if offences_file.exists():
        offences = pd.read_csv(offences_file)
        year = st.radio(T["groups_year"], [2025, 2016], horizontal=True, key="groups_year")
        wide = (offences[(offences["year"] == year) & (offences["state"] != "Germany")]
                .pivot(index="state", columns="group", values="rate"))
        wide = wide.rename(index=STATE_NAMES_DE)
        if LANG == "en":
            wide = wide.rename(index=STATE_NAMES_EN)
        wide = wide.loc[wide.sum(axis=1).sort_values().index]        # smallest total at the bottom
        fig = go.Figure()
        for group, color in zip(T["groups"], GROUP_COLORS):
            fig.add_trace(go.Bar(
                x=wide[group], y=wide.index, orientation="h", name=T["groups"][group],
                marker=dict(color=color, line=dict(color="rgba(255,255,255,0.9)", width=1)),
                hovertemplate="%{x:,.1f}"))
        base_layout(fig, T["groups_title"].format(year=year), x_title=T["groups_axis"], height=600)
        # Two legend rows need more room above the plot than the other charts
        # One hover box per state that lists all six groups
        fig.update_layout(barmode="stack", legend=dict(traceorder="normal"), margin=dict(t=120),
                          hovermode="y unified", yaxis=dict(showspikes=False),
                          title=dict(y=0.97, yanchor="top"))
        show(fig)
        st.markdown(T["groups_note"])

    with st.expander(T["bremen_h"]):
        st.markdown(T["bremen"])

    with st.expander(T["table"]):
        table = states.loc[highlight] if highlight else states
        table = table[["cases_2016", "cases_2025", "rate_2016", "rate_2025", "rate_change_pct",
                       "clearance_rate_2016", "clearance_rate_2025", "rank_2016", "rank_2025"]].round(1)
        table.columns = [f"{T['m_cases']} 2016", f"{T['m_cases']} 2025", f"{T['m_rate']} 2016",
                         f"{T['m_rate']} 2025", T["col_change"], f"{T['m_clearance']} 2016",
                         f"{T['m_clearance']} 2025", T["col_rank"].format(year=2016), T["col_rank"].format(year=2025)]
        table.index.name = T["col_state"]
        st.dataframe(table, width="stretch")

# ----------------------------------------------------------------------------
# Tab 4: method and sources
# ----------------------------------------------------------------------------
with tab_sources:
    st.subheader(T["definition_h"])
    st.markdown(T["definition"])
    st.table(pd.DataFrame(T["def_rows"], columns=[T["def_key"], T["def_offence"], T["def_law"]]).set_index(T["def_key"]))

    st.subheader(T["method_h"])
    st.markdown(T["method"])

    st.subheader(T["limits_h"])
    st.markdown(T["limits"])

    st.subheader(T["sources_h"])
    st.markdown(T["sources_intro"])
    st.table(pd.DataFrame(T["src_rows"], columns=[T["src_used"], T["src_table"], T["src_version"]]).set_index(T["src_used"]))
    st.markdown("[BKA: Polizeiliche Kriminalstatistik](https://www.bka.de/DE/AktuelleInformationen/"
                "StatistikenLagebilder/PolizeilicheKriminalstatistik/pks_node.html)")

    st.subheader(T["context_sources_h"])
    st.markdown(T["context_sources"])

    st.subheader(T["download_h"])
    d1, d2 = st.columns(2)
    d1.download_button(T["download_federal"], federal.to_csv().encode("utf-8"), "cybercrime_federal.csv", "text/csv")
    d2.download_button(T["download_states"], states.to_csv().encode("utf-8"), "cybercrime_states.csv", "text/csv")

# Footer below all tabs: copyright and data attribution
st.divider()
st.caption(T["footer"])
