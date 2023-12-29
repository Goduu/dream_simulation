import unittest
from unittest.mock import MagicMock
from board import Board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_set_players(self):
        players = [MagicMock(), MagicMock()]
        self.board.set_players(players)
        self.assertEqual(self.board.players, players)

    def test_find_hex_by_coordinates(self):
        hex1 = MagicMock(coordinates=(1, 2))
        hex2 = MagicMock(coordinates=(3, 4))
        self.board.hexs = [hex1, hex2]
        result = self.board.find_hex_by_coordinates((3, 4))
        self.assertEqual(result, hex2)

    def test_get_hex_color(self):
        player1 = MagicMock(color="red")
        player2 = MagicMock(color="blue")
        hex1 = MagicMock()
        hex2 = MagicMock()
        hex3 = MagicMock()
        self.board.hexs = [hex1, hex2, hex3]
        result1 = self.board.get_hex_color(hex1)
        result2 = self.board.get_hex_color(hex2)
        result3 = self.board.get_hex_color(hex3)
        self.assertEqual(result1, "red")
        self.assertEqual(result2, "blue")
        self.assertIsNone(result3)

    def test_remove_penguin(self):
        player = MagicMock(penguins=[MagicMock(), MagicMock()])
        self.board.players = [player]
        self.board.remove_penguin(player)
        self.assertEqual(len(self.board.players), 0)

    def test_get_all_penguins(self):
        player1 = MagicMock(penguins=[MagicMock(), MagicMock()])
        player2 = MagicMock(penguins=[MagicMock(), MagicMock()])
        self.board.players = [player1, player2]
        result = self.board.get_all_penguins()
        self.assertEqual(len(result), 4)
        self.assertIn(player1.penguins[0], result)
        self.assertIn(player1.penguins[1], result)
        self.assertIn(player2.penguins[0], result)
        self.assertIn(player2.penguins[1], result)

    def test_get_all_hexs(self):
        hex1 = MagicMock()
        hex2 = MagicMock()
        hex3 = MagicMock()
        self.board.hexs = [hex1, hex2, hex3]
        result = self.board.get_all_hexs()
        self.assertEqual(len(result), 3)
        self.assertIn(hex1, result)
        self.assertIn(hex2, result)
        self.assertIn(hex3, result)

if __name__ == '__main__':
    unittest.main()
    class TestBoard(unittest.TestCase):

        def setUp(self):
            self.board = Board()

        def test_set_players(self):
            players = [MagicMock(), MagicMock()]
            self.board.set_players(players)
            self.assertEqual(self.board.players, players)

    def test_find_hex_by_coordinates(self):
        hex1 = MagicMock(coordinates=(1, 2))
        hex2 = MagicMock(coordinates=(3, 4))
        self.board.hexs = [hex1, hex2]
        result = self.board.find_hex_by_coordinates((3, 4))
        self.assertEqual(result, hex2)

    def test_find_penguin_hex_occupation(self):
        player1 = MagicMock(penguins=[MagicMock(position=MagicMock()), MagicMock(position=None)])
        player2 = MagicMock(penguins=[MagicMock(position=None), MagicMock(position=MagicMock())])
        self.board.players = [player1, player2]
        hex1 = MagicMock()
        hex2 = MagicMock()
        result1 = self.board.find_penguin_hex_occupation(hex1)
        result2 = self.board.find_penguin_hex_occupation(hex2)
        self.assertEqual(result1, player1)
        self.assertEqual(result2, player2)

    def test_find_penguins_player(self):
        player1 = MagicMock(penguins=[MagicMock(), MagicMock()])
        player2 = MagicMock(penguins=[MagicMock(), MagicMock()])
        self.board.players = [player1, player2]
        penguin1 = MagicMock()
        penguin2 = MagicMock()
        result1 = self.board.find_penguins_player(penguin1)
        result2 = self.board.find_penguins_player(penguin2)
        self.assertEqual(result1, player1)
        self.assertEqual(result2, player2)

    def test_add_hex(self):
        hex1 = MagicMock()
        hex2 = MagicMock()
        self.board.add_hex(hex1)
        self.board.add_hex(hex2)
        self.assertEqual(self.board.hexs, [hex1, hex2])

    def test_add_penguin(self):
        player = MagicMock(start_point=MagicMock(), cubes=3)
        self.board.add_penguin(player)
        self.assertEqual(len(self.board.players), 1)
        self.assertEqual(self.board.players[0], player)

    def test_hex_exists(self):
        hex1 = MagicMock(coordinates=(1, 2))
        hex2 = MagicMock(coordinates=(3, 4))
        self.board.hexs = [hex1, hex2]
        result1 = self.board.hex_exists((1, 2))
        result2 = self.board.hex_exists((5, 6))
        self.assertTrue(result1)
        self.assertFalse(result2)

    def test_new_round(self):
        hex1 = MagicMock(occupation_number=2, player_occupation=MagicMock())
        hex2 = MagicMock(occupation_number=3, player_occupation=MagicMock())
        self.board.hexs = [hex1, hex2]
        self.board.new_round()
        self.assertEqual(hex1.occupation_number, 0)
        self.assertIsNone(hex1.player_occupation)
        self.assertEqual(hex2.occupation_number, 0)
        self.assertIsNone(hex2.player_occupation)

    def test_get_hex_color(self):
        player1 = MagicMock(color="red")
        player2 = MagicMock(color="blue")
        hex1 = MagicMock()
        hex2 = MagicMock()
        self.board.players = [player1, player2]
        self.board.find_penguin_hex_occupation = MagicMock(side_effect=[player1, player2])
        result1 = self.board.get_hex_color(hex1)
        result2 = self.board.get_hex_color(hex2)
        self.assertEqual(result1, "red")
        self.assertEqual(result2, "blue")

    def test_get_hex_player_name(self):
        player1 = MagicMock(name="Alice")
        player2 = MagicMock(name="Bob")
        hex1 = MagicMock()
        hex2 = MagicMock()
        self.board.players = [player1, player2]
        self.board.find_penguin_hex_occupation = MagicMock(side_effect=[player1, player2])
        result1 = self.board.get_hex_player_name(hex1)
        result2 = self.board.get_hex_player_name(hex2)
        self.assertEqual(result1, "Alice")
        self.assertEqual(result2, "Bob")