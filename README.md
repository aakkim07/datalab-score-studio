# DataLab — Score Studio

Jednoduchá desktopová aplikácia v Pythone na generovanie a porovnávanie skóre. Rozhranie je v slovenčine a používa iba štandardnú knižnicu Tkinter.

## Funkcie

- Vygeneruje pole 50 náhodných hodnôt v rozsahu 10–100.
- Vypočíta minimum, maximum, priemer a medián; zobrazí aj vzostupne zoradené hodnoty.
- Umožňuje vybrať jeden z troch vzorcov a porovnať pôvodné a vypočítané hodnoty v grafe.
- Exportuje obe série a použitý vzorec do CSV.

## Spustenie v PyCharm

1. Otvorte projekt `PythonProject4` v PyCharm.
2. Ako interpreter vyberte existujúce prostredie `.venv` (Python 3.12).
3. Otvorte `main.py` a spustite ho cez zelené tlačidlo **Run**.

Projekt nepoužíva externé knižnice na beh aplikácie. Súbor `requirements.txt` obsahuje iba PyInstaller na vytvorenie EXE.

## Testy

V termináli PyCharm spustite:

```powershell
.venv\Scripts\python.exe -m unittest -v
```

## Vytvorenie EXE

Dvakrát kliknite na `build_exe.bat` alebo ho spustite z projektu. Skript nainštaluje PyInstaller do `.venv` a vytvorí samostatný spustiteľný súbor:

```text
dist\DataLab.exe
```

Na počítači, kde sa EXE spúšťa, nie je potrebné mať nainštalovaný Python. Samotné vytvorenie EXE sa vykonáva na Windows.
