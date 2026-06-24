ReadME
# The Epic Games: Car RPG

Un jeu de rôle (RPG) au tour par tour développé en Python avec Pygame. Le joueur incarne un véhicule héroïque qui explore des cartes, combat des adversaires mécaniques (comme la Red Bull ou le Bulldozer Blindé) et récupère des pièces d'équipement pour améliorer ses statistiques.

---

## Fonctionnalités

- Exploration du Monde : Navigation à la grille sur une carte interactive avec gestion des collisions et zones de routes sinueuses déclenchant des combats aléatoires.
- Système de Combat : Affrontements tactiques au tour par tour incluant des mécaniques de calcul de dégâts basées sur l'attaque, la défense et un taux d'esquive (dodge).
- Équipements et Butin (Loot) : Système de butin automatique après chaque victoire. Il est possible d'équiper des moteurs (V8), turbos, pneus sport, carrosseries ou suspensions pour modifier les statistiques du véhicule.
- Gestion de l'Inventaire : Utilisation de potions de réparation en plein combat et navigation dans des menus d'inventaire dédiés.
- Sauvegarde et Chargement : Sauvegarde de la progression à tout moment depuis le monde ouvert pour ne pas perdre les équipements obtenus.

---

## Installation et Lancement

### Prérequis
Le jeu nécessite l'installation de Python 3.10 ou supérieur ainsi que le gestionnaire de paquets pip.

### 1. Cloner le dépôt
```bash
git clone [https://github.com/RainderAx/The-Epic-Games-.git](https://github.com/RainderAx/The-Epic-Games-.git)
cd The-Epic-Games-
```

### 2. Installer les dépendances
Installez la bibliothèque Pygame requise pour faire tourner le moteur du jeu :

```bash
pip install pygame
```
#### 3. Lancer le jeu

```bash
python main.py
```

Commandes du Jeu
Dans les Menus (Écran Titre / Inventaires)
Flèches Directionnelles : Naviguer entre les options.

Entrée : Valider un choix.

En Exploration (Monde Ouvert)
Flèches Directionnelles : Déplacer le véhicule.

I : Ouvrir / Fermer l'Inventaire des objets possédés.

E : Ouvrir / Fermer le menu d'Équipement (pour équiper les pièces de voiture).

B : Ouvrir / Fermer la Boutique (Station service).

S : Sauvegarder instantanément la partie actuelle.

En Combat
Flèches Gauche / Droite : Choisir entre Attaquer, Potion ou Fuite.

Entrée : Confirmer l'action du tour.

### Générer un Build Exécutable (.exe)
Il est possible de compiler le jeu pour y jouer sans installer Python ou pour le partager sous forme de fichier exécutable grâce à PyInstaller.

### 1. Installez PyInstaller :
```Bash 
pip install pyinstaller
```

### 2. Créez le build :
```Bash
pyinstaller --noconsole --onefile main.py
```

### 3. Intégration des Assets :

dist/
├── main.exe
├── assets/       <-- À copier/coller ici
└── data/         <-- À copier/coller ici


**Structure du Projet**

The-Epic-Games-/
├── assets/             # Sprites des véhicules (PNG), UI et arrière-plans
├── battle/             # Logique des combats, calculs de dégâts et loots
├── data/               # Base de données du jeu (cars.json, equipments.json, maps/)
├── entities/           # Modèles de données (Player, Ennemy, Stats)
├── equipment/          # Gestion et instanciation des pièces de rechange
├── save/               # Gestionnaire du système de sauvegarde JSON
├── ui/                 # Interfaces graphiques (BattleUI, Menu, ShopMenu...)
├── world/              # Moteur de la carte, des herbes et des collisions
├── main.py             # Point d'entrée principal du jeu
└── README.md           # Documentation du projet


**Licence**
Ce projet est réalisé dans un but pédagogique et de divertissement. Les assets et codes sources restent modifiables et utilisables librement.