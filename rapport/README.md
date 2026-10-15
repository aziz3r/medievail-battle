# Rapport technique

[`rapport.pdf`](rapport.pdf) — 8 pages : contexte du projet, architecture MVP, modèle de combat
(unités, formule de dégâts, boucle de simulation, terrains), les cinq IA, les interfaces,
expériences (tournoi de 500 matchs entre les IA, vérification de la loi carrée de Lanchester,
coût de calcul), démonstration, limites repérées et pistes d'amélioration.

Source LaTeX : `rapport.tex`. Les figures du dossier `figures/` sont des captures de la
démonstration (`../demo/`) et le graphe `loi_carree_knight_crossbowman.png` du dépôt, réencodés en JPEG
pour alléger le PDF.

## Recompiler

```bash
brew install tectonic          # moteur LaTeX autonome, sans privilèges
cd rapport
tectonic -X compile rapport.tex
```
