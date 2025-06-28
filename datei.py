import sys 

try:
    d = open("praxislager.db", "w")
except:
    print("Datei nicht geöffnet")
    sys.exit(0)

li = [[('Latexhandschuhe', 60, 10, 'Packung', 'Labor', '17.06.2025', 'MS'),
            ('Mullbinde 6cm', 18, 8, 'Packung', 'Labor', '17.06.2025', 'AB'),
            ('Desinfektionsmittel', 25, 5, 'Liter', 'Lager A', '17.06.2025', 'TK'),
            ('Einmalspritzen 5ml', 120, 20, 'Packung', 'Labor', '17.06.2025', 'MS'),
            ('Gelbe Kanüle', 6, 5, 'Stück', 'Labor', '17.06.2025', 'EG'),
            ('Urbason 1000mg', 3, 2, 'Stück', 'Medikamentenschrank', '17.06.2025', 'EG'),
            ('Mullkompresse 10x10', 2, 3, 'Packung', 'Labor', '17.06.2025', 'EG'),
            ('Optiskin', 2, 1, 'Stück', 'Labor', '17.06.2025', 'EG'),
            ('Leukase Puder', 1, 1, 'Stück', 'Medikamentenschrank', '17.06.2025', 'EG'),
            ('Skalpell 15 REF', 3, 2, 'Stück', 'Labor', '17.06.2025', 'EG')]]
