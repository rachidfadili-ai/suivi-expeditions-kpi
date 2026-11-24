# Suivi des expeditions et KPI transport

Projet personnel de Rachid Fadili.

Outil Python simple pour suivre la performance du transport de marchandises:
ponctualite des livraisons (OTD), retard moyen, cout au km, expeditions perdues,
et classement des transporteurs avec alerte quand un transporteur passe sous 85% de ponctualite.

## Pourquoi
Dans la logistique de transport, on doit suivre chaque jour les delais, les couts
et la fiabilite des transporteurs. Ce projet montre comment calculer ces indicateurs
a partir d'un simple fichier CSV d'expeditions.

## Donnees
Toutes les donnees sont **fictives** (generees par `src/generate.py`, 500 expeditions,
5 transporteurs, 7 destinations). Aucune donnee d'entreprise.

## Utilisation
```
python src/generate.py          # cree data/expeditions_demo.csv
python src/report.py            # cree rapport.html (a ouvrir dans le navigateur)
python -m unittest discover tests
```
Python 3.9+, aucune dependance externe. Pour vos propres donnees, gardez les memes colonnes que le CSV de demo.

## Indicateurs
- **OTD %**: livraisons a l'heure (tolerance 1 h) sur livraisons effectuees.
- **Retard moyen**: moyenne des retards, en heures.
- **Cout / km**: cout total divise par les km parcourus.
- **Score transporteur /100**: 70% ponctualite, 20% pertes, 10% retard moyen.

## Contact
rachidfadili2002@outlook.com
