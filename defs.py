from thefuzz import fuzz
import textdistance
import pandas as pd

#fourth_match: Gegeben einer Textdatei bspw. 'test.txt' wird eine Datei mit ICD-10-GM Zuweisungen erstellt
#stepsize: Die Textdatei wird in "Batches" verarbeitet, die stepsize gibt an wie viele Krankheiten auf einmal
#verarbeitet werden.
#return: result: Zurückgegeben wird eine Liste mit Krankheit, gefundene Übereinstimmung und Übereinstimmungsscore
def fourth_match(start):
    print("Starting batch: " + str(start))
    # Load Data
    data = pd.read_csv('test.txt', sep="                               ", names=["Krankheit"], skip_blank_lines=True, engine="python")
    data = data.values.tolist()
    data_flattened = [element for sublist in data for element in sublist]

    # Load ICD-10
    names_kapitel = ["Kapitelnummer", "Kapiteltitel"]
    names_codes = ["Klassifikationsebene", "Ort der Schlüsselnummer im Klassifikationsbaum, 1 Zeichen",
                   "Art der Vier- und Fünfsteller", "Kapitelnummer, max. 2 Zeichen",
                   "erster Dreisteller der Gruppe, 3 Zeichen",
                   "Schlüsselnummer ohne eventuelles Kreuz, bis zu 7 Zeichen",
                   "Schlüsselnummer ohne Strich, Stern und Ausrufezeichen, bis zu 6 Zeichen",
                   "Schlüsselnummer ohne Punkt, Strich, Stern und Ausrufezeichen, bis zu 5 Zeichen",
                   "Klassentitel, zusammengesetzt aus Bestandteilen der Titel der dreistelligen, vierstelligen und fünfstelligen Kodes, falls vorhanden, bis zu 255 Zeichen",
                   "Titel des dreistelligen Kodes, bis zu 255 Zeichen",
                   "Titel des vierstelligen Kodes, falls vorhanden, bis zu 255 Zeichen",
                   "Titel des fünfstelligen Kodes, falls vorhanden, bis zu 255 Zeichen",
                   "Verwendung der Schlüsselnummer nach Paragraph 295",
                   "Verwendung der Schlüsselnummer nach Paragraph 301", "Bezug zur Mortalitätsliste 1",
                   "Bezug zur Mortalitätsliste 2",
                   "Bezug zur Mortalitätsliste 3", "Bezug zur Mortalitätsliste 4", "Bezug zur Morbiditätsliste",
                   "Geschlechtsbezug der Schlüsselnummer",
                   "Art des Fehlers bei Geschlechtsbezug", "untere Altersgrenze für eine Schlüsselnummer",
                   "obere Altersgrenze für eine Schlüsselnummer",
                   "Art des Fehlers bei Altersbezug", "Krankheit in Mitteleuropa sehr selten?",
                   "Schlüsselnummer mit Inhalt belegt?",
                   "IfSG-Meldung, kennzeichnet, dass bei Diagnosen, die mit dieser Schlüsselnummer kodiert sind, besonders auf die Arzt-Meldepflicht nach dem Infektionsschutzgesetz (IfSG) hinzuweisen ist",
                   "IfSG-Labor, kennzeichnet, dass bei Laboruntersuchungen zu diesen Diagnosen die Laborausschlussziffer des EBM (32006) gewählt werden kann"]

    kapitel = pd.read_csv("icd10gm2022syst-meta/Klassifikationsdateien/icd10gm2022syst_kapitel.txt", delimiter=";",
                          names=names_kapitel)
    codes = pd.read_csv("icd10gm2022syst-meta/Klassifikationsdateien/icd10gm2022syst_kodes.txt", delimiter=";",
                        names=names_codes)
    kapitel.columns = kapitel.columns.str.replace('Kapitelnummer', 'Code')
    kapitel.columns = kapitel.columns.str.replace('Kapiteltitel', 'Krankheit')

    codes.columns = codes.columns.str.replace('Schlüsselnummer ohne eventuelles Kreuz, bis zu 7 Zeichen', 'Code')
    codes.columns = codes.columns.str.replace(
        'Klassentitel, zusammengesetzt aus Bestandteilen der Titel der dreistelligen, vierstelligen und fünfstelligen Kodes, falls vorhanden, bis zu 255 Zeichen',
        'Krankheit')

    frames = [kapitel, codes[["Code", "Krankheit"]]]
    krankheiten = pd.concat(frames)
    krankheiten = krankheiten.values.tolist()

    # Lade Synonyme
    names_synonyme = ["Code",
                      "Krankheit"]
    synonyme = pd.read_csv("synonyme.csv", encoding="ISO-8859-1", on_bad_lines='skip', delimiter=",", index_col=False,
                           header=2, names=names_synonyme)

    # Lade alphabetisches Verzeichnis von ICD-10-GM
    # Alpha-ID(-SE)
    names_alpha = ["Gültigkeit", "Alpha-Identifikationsnummer", "Primärschlüsselnummer 1", "Sternschlüsselnummer",
                   "Zusatzschlüsselnummer",
                   "Primärschlüsselnummer 2", "Orpha-Kennnummer", "zugehöriger Text, ohne eventuelle Verweise"]
    alpha = pd.read_csv("alphaidse2022_20220114\icd10gm2022_alphaidse_edvtxt_20211001_20220114.txt", delimiter="|",
                        names=names_alpha)
    alpha = alpha[["Primärschlüsselnummer 1", "zugehöriger Text, ohne eventuelle Verweise"]].dropna()
    alpha = alpha.values.tolist()
    synonyme = synonyme.values.tolist()
    krankheiten.extend(alpha)
    krankheiten.extend(synonyme)

    result = []
    for element1 in data_flattened[start:start+100]:
        fuzz_score = 0
        fuzz_match = ""
        soren_score = 0
        soren_match = ""
        for ls in krankheiten:
            if (fuzz_score < fuzz.token_set_ratio(element1, ls[1])):
                fuzz_score = fuzz.token_set_ratio(element1, ls[1])
                fuzz_match = ls
            if (soren_score < textdistance.sorensen.normalized_similarity(element1, str(ls[1]))):
                soren_score = textdistance.sorensen.normalized_similarity(element1, str(ls[1]))
                soren_match = ls
        if (soren_score * 100 > fuzz_score + 5):
            fuzz_score = soren_score * 100
            fuzz_match = soren_match
        result.append([element1, fuzz_match, fuzz_score])
    print("Done with batch: " + str(start))
    return result

