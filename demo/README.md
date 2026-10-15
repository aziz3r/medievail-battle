# Démo — MedievAIl Battle

![Aperçu de la démo (GIF accéléré x3)](demo_apercu.gif)

> Aperçu accéléré x3. **[Vidéo complète : `demo.mp4`](demo.mp4)** (55 s, 1024×768, 30 images/s).

## Ce que montre la démo

Parcours complet du jeu, du menu à la victoire :

1. **Menu principal** → *Nouvelle bataille*.
2. **Configuration** : IA de l'équipe A = *General STRATEGUS*, IA de l'équipe B = *Major DAFT*, composition *Grande Bataille (105 unités par équipe)*, terrain *Colline Centrale*.
3. **Bataille** : 210 unités (piquiers, chevaliers, arbalétriers), zoom à la molette, déplacement de la caméra au glisser-déposer, minimap (`M`).
4. **Fin de partie** : *Victoire équipe B* (87 survivants contre 0), puis retour au menu avec `ÉCHAP`.

## Captures d'écran

| | |
| :-- | :-- |
| ![](screenshots/01_menu_principal.png)<br>**01** Menu principal | ![](screenshots/02_configuration_bataille.png)<br>**02** Configuration de la bataille |
| ![](screenshots/03_choix_de_l_ia.png)<br>**03** Choix de l'IA | ![](screenshots/04_configuration_complete.png)<br>**04** Configuration complète |
| ![](screenshots/05_bataille_debut.png)<br>**05** Début de bataille | ![](screenshots/06_vue_d_ensemble.png)<br>**06** Vue d'ensemble (dézoom) |
| ![](screenshots/07_melee.png)<br>**07** Les deux armées se rejoignent | ![](screenshots/08_zoom_melee.png)<br>**08** Zoom sur la mêlée |
| ![](screenshots/09_bataille_en_cours.png)<br>**09** Bataille en cours | ![](screenshots/10_victoire.png)<br>**10** Victoire |
| ![](screenshots/11_retour_menu.png)<br>**11** Retour au menu | |

## Comment la démo a été réalisée

[`capture_demo.py`](capture_demo.py) exécute **le vrai jeu** (`view/menu.py` en mode fenêtré, puis la bataille), sans modifier son code. Seuls la souris, le clavier et l'horloge sont pilotés par un scénario scripté, et l'affichage utilise le pilote SDL `dummy` (aucune fenêtre ne s'ouvre). Chaque image réellement dessinée par le jeu est enregistrée à 30 images/s en temps virtuel : la vidéo est donc fluide quelle que soit la machine, et le résultat est reproductible.

Pour régénérer la vidéo, le GIF et les captures (depuis la racine du dépôt) :

```bash
pip install pygame   # ffmpeg doit être installé et accessible dans le PATH
python demo/capture_demo.py
```
