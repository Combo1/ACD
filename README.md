# AKK
Automatische Klassifikation von Krankheiten. Dieses Programm ermöglicht es dem Benutzer Krankheiten im Textformat in das ICD-10-GM-Format zu klassifizieren.


# Wie wird dieses Programm verwendet?
Um Ihre Krankheiten zu klassifizieren, führen Sie die Datei "classify.py" aus. Allerdings müssen Sie das Verzeichnis in Zeile 2: "data = pd.read_csv('INSERT-YOUR-PATH', sep=" ", names = ["Krankheit"], skip_blank_lines=True)" in Ihr eigenes Verzeichnis ändern. Die Datei muss nur die Diagnose gefolgt von einem Zeilenumbruch/Enter enthalten. Eine Beispieldatei wird als "sample.txt" bereitgestellt.

# Wie funktioniert es?
Um unsere Krankheiten automatisch zu klassifizieren werden sämtliche Krankheiten mit ICD-10-GM Beschreibungen verglichen (siehe: https://www.bfarm.de/SharedDocs/Downloads/DE/Kodiersysteme/klassifikationen/icd-10-gm/version2022/icd10gm2022syst-meta_zip.html?nn=841246&cms_dlConfirm=true&cms_calledFromDoc=841246). Dieser Vergleich läuft mithilfe von "Approximate String Matching" ab. Approximate String Matching ist dazu fähig ähnliche aber nicht komplett gleiche Text/Sequenzen einander zuzuordnen. Approximate String Matching beinhaltet eine Vielzahl an Methoden, wir verwenden aber nur die "Token Set Ratio" (siehe https://github.com/seatgeek/thefuzz).

Zusätzlich zu den ICD-10-GM Beschreibungen haben wir sämtliche ICD-10-GM Codes in Altmeyers Enzyklopädie gesucht und alle Krankheiten die darunter fallen in "synonyme.csv" geschrieben, sodass wir jede Krankheit mit diesen expliziten Krankheitsbezeichnungen vergleichen. Des Weiteren verwenden wir auch noch das alphabetische Verzeichnis aus ICD-10-GM, welches Krankheitsbezeichnungen aus dem stationären und ambulanten Alltagsgebrauch beinhaltet, um unsere Krankheiten zu vergleichen.

Abschließend verwenden wir noch den "Sorensen Dice Coefficient" in einer Hybrid-Version mit der Token Set Ratio, um unsere Texte zu vergleichen. Diese Hybrid-Lösung benötigt viel Rechenleistung auf ihrer Maschine, sodass wir Multiprocessing verwenden, um sämtliche Texte miteinander zu vergleichen.
