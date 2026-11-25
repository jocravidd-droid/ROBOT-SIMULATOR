# Exemples d'utilisation

Lancer le programme avec `python -m src.main`, puis saisir les réponses aux
questions dans l'ordre.

## Créer une grille et quitter

**Entrées**

```text
Nombre de colonnes et de lignes (séparés par des espaces) : 4 3
Nom du robot : R2
Déplacement ... : quitter
```

Le robot est placé au centre de la grille (colonne 2, ligne 1). La grille est affichée avec `🚀` pour le robot et `🌌` pour une case vide.

> Vous pouvez changer de perssonnage en allant dans le programme puis dans `class Robot` et descendre jusqu'a atteindre la methode `disposition`

## Déplacer le robot

**Entrées**

```text
Nombre de colonnes et de lignes (séparés par des espaces) : 4 3
Nom du robot : R2
Déplacement ... : droite
Déplacement ... : avant
Déplacement ... : quitter
```

`droite` déplace le robot d'une case vers la droite. `avant` le déplace d'une case vers le haut. Après chaque déplacement, la grille actualisée est affichée.

## Déplacement qui sortirait de la grille

Si le robot est déjà au bord de la grille et que le prochain déplacement le ferait sortir, le programme affiche un avertissement et le garde à sa place.

## Entrée de dimensions incorrecte

```text
Nombre de colonnes et de lignes (séparés par des espaces) : grand petit
```

Le programme affiche une erreur indiquant que les dimensions doivent être des nombres entiers.
