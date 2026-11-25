import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

# Permet aussi de lancer ce fichier directement depuis le terminal ou VS Code.
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.main import Creation_Robot, Robot, deplacement_robot, main


class RobotTests(unittest.TestCase):
    # Cette méthode prépare un robot pour réutiliser les mêmes données de test.
    def make_robot(self, position=(1, 1), colonnes=3, lignes=3):
        grille = Robot.creation_grille(colonnes, lignes)
        return Robot("R2", [position], grille)

    # Le robot doit être enregistré sur sa case au moment de sa création.
    def test_initialisation_places_robot_on_grid(self):
        robot = self.make_robot()

        self.assertEqual(robot.nom, "R2")
        self.assertEqual(robot.emplacement, [(1, 1)])
        self.assertEqual(robot.grille[1][1], 1)

    # Un nom vide ne permet pas de créer un robot.
    def test_initialisation_rejects_empty_name(self):
        with self.assertRaises(ValueError):
            Robot(" ", [(0, 0)], [[0]])

    # La grille doit exister et la position doit rester dans ses limites.
    def test_initialisation_rejects_invalid_grid_and_position(self):
        with self.assertRaises(ValueError):
            Robot("R2", [(0, 0)], [])
        with self.assertRaises(ValueError):
            Robot("R2", [(2, 0)], [[0]])

    # Plusieurs positions valides sont marquées sur la grille.
    def test_deplacement_multidirectionelle_places_positions(self):
        robot = self.make_robot()

        result = robot.deplacement_multidirectionelle([(0, 2), (2, 0)])

        self.assertIs(result, robot.grille)
        self.assertEqual(robot.grille[0][2], 1)
        self.assertEqual(robot.grille[2][0], 1)
        self.assertEqual(robot.emplacement, [(0, 2), (2, 0)])

    # Une position hors grille ou avec un format incorrect est refusée.
    def test_deplacement_multidirectionelle_rejects_invalid_positions(self):
        robot = self.make_robot()

        for position in [[(3, 0)], [(1,)], [(1.5, 0)]]:
            with self.subTest(position=position):
                with self.assertRaises(ValueError):
                    robot.deplacement_multidirectionelle(position)

    # Un déplacement normal fonctionne, mais un déplacement au bord est bloqué.
    def test_private_move_moves_and_stays_inside_grid(self):
        robot = self.make_robot()

        robot._deplacer(0, 1)
        self.assertEqual(robot.emplacement, [(1, 2)])
        self.assertEqual(robot.grille[1], [0, 0, 1])

        with contextlib.redirect_stdout(io.StringIO()):
            robot._deplacer(0, 1)
        self.assertEqual(robot.emplacement, [(1, 2)])
        self.assertEqual(robot.grille[1], [0, 0, 1])

    # Une liste de positions vide ne doit pas provoquer d'erreur.
    def test_private_move_with_no_positions_is_safe(self):
        robot = Robot("R2", [], [[0]])

        self.assertEqual(robot._deplacer(1, 0), [[0]])

    # Chaque direction déplace le robot et une commande inconnue est refusée.
    def test_deplacer_supports_each_direction_and_rejects_unknown(self):
        robot = self.make_robot()

        for direction, position in (
            ("avant", [(0, 1)]),
            ("arriere", [(1, 1)]),
            ("gauche", [(1, 0)]),
            ("droite", [(1, 1)]),
        ):
            with self.subTest(direction=direction):
                self.assertTrue(robot.deplacer(direction))
                self.assertEqual(robot.emplacement, position)

        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(robot.deplacer("diagonale"))

    # La grille affichée contient le robot, les cases libres et son nom.
    def test_disposition_returns_a_readable_grid(self):
        robot = self.make_robot()

        with patch("src.main.os.system"):
            result = robot.disposition()

        self.assertIn("🚀", result)
        self.assertIn("🌌", result)
        self.assertIn("Position de R2", result)

    # La grille créée a le nombre de colonnes et de lignes demandé.
    def test_creation_grille_creates_requested_dimensions(self):
        self.assertEqual(
            Robot.creation_grille(2, 3),
            [[0, 0, 0], [0, 0, 0]],
        )

    # Une grille ne peut pas avoir de dimension nulle ou négative.
    def test_creation_grille_rejects_non_positive_dimensions(self):
        for colonnes, lignes in ((0, 3), (2, 0), (-1, 3), (2, -1)):
            with self.subTest(colonnes=colonnes, lignes=lignes):
                with self.assertRaises(ValueError):
                    Robot.creation_grille(colonnes, lignes)


class FunctionTests(unittest.TestCase):
    # La fonction de création renvoie un robot prêt à être utilisé.
    def test_creation_robot_returns_and_displays_robot(self):
        with patch("src.main.os.system"), contextlib.redirect_stdout(io.StringIO()):
            robot = Creation_Robot("R2", [(0, 1)], [[0, 0], [0, 0]], 2)

        self.assertIsInstance(robot, Robot)
        self.assertEqual(robot.emplacement, [(0, 1)])

    # Une position invalide affiche une erreur et ne crée pas de robot.
    def test_creation_robot_reports_invalid_data(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            robot = Creation_Robot("R2", [(5, 0)], [[0]], 1)

        self.assertIsNone(robot)
        self.assertIn("[ERREUR]", output.getvalue())

    # La boucle de déplacement signale si l'objet reçu n'est pas un robot.
    def test_deplacement_robot_rejects_non_robot(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            deplacement_robot(None)

        self.assertIn("robot valide", output.getvalue())

    # La commande saisie déplace le robot, puis "quitter" termine la boucle.
    def test_deplacement_robot_accepts_move_then_quits(self):
        robot = Robot("R2", [(1, 1)], Robot.creation_grille(3, 3))
        output = io.StringIO()
        with patch("builtins.input", side_effect=["droite", "quitter"]), \
                patch("src.main.os.system"), \
                contextlib.redirect_stdout(output):
            deplacement_robot(robot)

        self.assertEqual(robot.emplacement, [(1, 2)])
        self.assertIn("Fin du programme.", output.getvalue())

    # Le programme complet demande les dimensions, le nom et les commandes.
    def test_main_runs_interactive_program(self):
        output = io.StringIO()
        with patch(
            "builtins.input",
            side_effect=["3 3", "R2", "quitter"],
        ), patch("src.main.os.system"), contextlib.redirect_stdout(output):
            main()

        self.assertIn("Position de R2", output.getvalue())
        self.assertIn("Fin du programme.", output.getvalue())

    # Le programme signale des dimensions qui ne sont pas strictement positives.
    def test_main_reports_invalid_dimensions(self):
        output = io.StringIO()
        with patch("builtins.input", return_value="0 3"), \
                contextlib.redirect_stdout(output):
            main()

        self.assertIn("supérieurs à zéro", output.getvalue())


if __name__ == "__main__":
    unittest.main()
