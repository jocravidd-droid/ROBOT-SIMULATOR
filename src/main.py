import os


class Robot:
    def __init__(self, nom: str, emplacement: list, grille: list):
        try:
            if not isinstance(nom, str) or not nom.strip():
                raise ValueError("Le nom du robot ne peut pas être vide.")
            if not isinstance(grille, list) or not grille:
                raise ValueError("La grille doit être une liste non vide.")
            if not isinstance(emplacement, list):
                raise ValueError("Les positions du robot doivent être fournies sous forme de liste.")
            self.nom = nom
            self.emplacement = emplacement
            self.grille = grille
            self.deplacement_multidirectionelle(emplacement)
        except (TypeError, IndexError) as erreur:
            raise ValueError(
                "Impossible d'initialiser le robot : les données de position ou de grille sont invalides."
            ) from erreur

    def deplacement_multidirectionelle(self, position):
        try:
            for coordonnees in position:
                if not isinstance(coordonnees, tuple) or len(coordonnees) != 2:
                    raise ValueError(
                        "Chaque position doit contenir exactement deux coordonnées au format (x, y)."
                    )
                x, y = coordonnees
                if not isinstance(x, int) or not isinstance(y, int):
                    raise ValueError("Les coordonnées doivent être des nombres entiers.")
            colonnes = len(self.grille)
            lignes = len(self.grille[0]) if colonnes else 0
            if any(
                x < 0 or x >= colonnes or y < 0 or y >= lignes
                for x, y in position
            ):
                raise ValueError("La position du robot est située hors de la grille.")
            for x, y in position:
                self.grille[x][y] = 1
            self.emplacement = position
            return self.grille
        except (IndexError, TypeError) as erreur:
            raise ValueError(
                "Impossible de placer le robot : la grille ou les coordonnées sont invalides."
            ) from erreur

    def _deplacer(self, dx, dy):
        try:
            nouvelles_positions = [
                (x + dx, y + dy) for x, y in self.emplacement
            ]

            if not nouvelles_positions:
                return self.grille

            colonnes = len(self.grille)
            lignes = len(self.grille[0]) if colonnes else 0
            if any(
                x < 0 or x >= colonnes or y < 0 or y >= lignes
                for x, y in nouvelles_positions
            ):
                print(
                    "[AVERTISSEMENT] : Déplacement impossible, le robot sortirait de la grille."
                )
                return self.grille

            for x, y in self.emplacement:
                if 0 <= x < colonnes and 0 <= y < lignes:
                    self.grille[x][y] = 0
            return self.deplacement_multidirectionelle(nouvelles_positions)
        except (IndexError, TypeError, AttributeError):
            print(
                "[ERREUR] : Déplacement impossible, les positions ou la grille ne sont pas valides."
            )
            return self.grille

    def deplacer(self, direction):
        if direction == "avant":
            self._deplacer(-1, 0)
        elif direction == "arriere":
            self._deplacer(1, 0)
        elif direction == "gauche":
            self._deplacer(0, -1)
        elif direction == "droite":
            self._deplacer(0, 1)
        else:
            print(
                f"[AVERTISSEMENT] : Déplacement invalide '{direction}'. "
                "Veuillez saisir 'avant', 'arriere', 'gauche', 'droite' ou 'quitter'."
            )
            return False
        return True

    def disposition(self):
        os.system("cls" if os.name == "nt" else "clear")
        grille_visuelle = ""
        for colonne in self.grille:
            ligne = ""
            for position in colonne:
                ligne += "🚀" if position else "🌌"
            grille_visuelle += ligne + "\n"
        grille_visuelle += f"\nPosition de {self.nom} en ce moment"
        return grille_visuelle

    @staticmethod
    def creation_grille(colonnes, ligne):
        if colonnes <= 0 or ligne <= 0:
            raise ValueError(
                "Le nombre de colonnes et de lignes doit être supérieur à zéro."
            )
        return [[0 for _ in range(ligne)] for _ in range(colonnes)]


def Creation_Robot(
    nom_robot: str, coordonne_depart: list, grille_depart: list, n_ligne: int
):
    try:
        if not isinstance(nom_robot, str) or not nom_robot.strip():
            raise ValueError("Le nom du robot est obligatoire.")
        if not coordonne_depart or not isinstance(coordonne_depart[0], tuple):
            raise ValueError(
                "La position doit être une liste contenant une paire de coordonnées, "
                "par exemple [(2, 6)]."
            )
        if len(coordonne_depart) > 1:
            raise ValueError("Une seule position de départ est autorisée.")
        if len(coordonne_depart[0]) != 2:
            raise ValueError(
                "Chaque position doit contenir exactement deux coordonnées : une colonne et une ligne."
            )
        x, y = coordonne_depart[0]
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Les coordonnées de départ doivent être des nombres entiers.")
        if not isinstance(grille_depart, list) or not grille_depart:
            raise ValueError("La grille de départ est inexistante ou invalide.")
        if x < 0 or x >= len(grille_depart) or y < 0 or y >= n_ligne:
            raise ValueError("Les coordonnées de départ sont hors de la grille.")
        robot = Robot(
            nom=nom_robot,
            emplacement=coordonne_depart,
            grille=grille_depart,
        )
        print(robot.disposition())
        return robot
    except (ValueError, TypeError, IndexError) as erreur:
        print(f"[ERREUR] : {erreur}")
        return None


def deplacement_robot(robot_instance):
    try:
        if not isinstance(robot_instance, Robot):
            raise ValueError("L'instance fournie n'est pas un robot valide.")

        while True:
            deplacement = input(
                "\nDéplacement (avant, arriere, gauche, droite) "
                "ou 'quitter' pour arrêter : "
            ).strip().lower()
            if deplacement == "quitter":
                print("Fin du programme.")
                break
            deplacements_saisis = deplacement.split()
            if not all(robot_instance.deplacer(d) for d in deplacements_saisis): # all renvoie True si tous les éléments sont vrais, sinon False ( m'attraper pas la veste j'ai pas trouver mieux )
                continue
            print(robot_instance.disposition())
    except (ValueError, AttributeError) as erreur:
        print(f"[ERREUR] : {erreur}")


def main():
    try:
        dimensions = input(
            "\nNombre de colonnes et de lignes (séparés par des espaces) : "
        ).split()
        if len(dimensions) != 2:
            raise ValueError(
                "Saisissez exactement deux nombres : le nombre de colonnes puis le nombre de lignes."
            )
        try:
            new_colonne, new_ligne = map(int, dimensions) # convertie tout en entier
        except ValueError as erreur:
            raise ValueError(
                "Les dimensions doivent être saisies avec des nombres entiers."
            ) from erreur
        if new_colonne <= 0 or new_ligne <= 0:
            raise ValueError(
                "Le nombre de colonnes et le nombre de lignes doivent être supérieurs à zéro."
            )

        grille_original = Robot.creation_grille(
            colonnes=new_colonne, ligne=new_ligne
        )
        milieu_colonnes = len(grille_original) // 2
        milieu_lignes = len(grille_original[milieu_colonnes]) // 2
        coordonnee = [(milieu_colonnes, milieu_lignes)]

        robot_nom = input("Nom du robot : ").strip()
        if not robot_nom:
            raise ValueError("Le nom du robot ne peut pas être vide.")
        robot = Creation_Robot(
            robot_nom, coordonnee, grille_original, new_ligne
        )
        if robot is not None:
            deplacement_robot(robot)
    except (ValueError, EOFError, KeyboardInterrupt) as erreur:
        if isinstance(erreur, KeyboardInterrupt):
            print("\n[ERREUR] : La saisie a été interrompue par l'utilisateur.")
        elif isinstance(erreur, EOFError):
            print(
                "[ERREUR] : Aucune saisie n'a été reçue. Le programme ne peut pas continuer."
            )
        else:
            print(f"[ERREUR] : {erreur}")


if __name__ == "__main__":
    main()
