from django.test import TestCase

from .factories import ClueFactory, EntryFactory, PuzzleFactory


class TestXWordModels(TestCase):

    def test_clue(self):
        clue = ClueFactory()
        string_repr = str(clue)
        # I changed this test to look for pk instead of entry_text because
        # I would not want to reference values from the foreign Entry model
        # in the str represtation method of the Clue model.
        # The reason for that is in case we only query for Clue without using select_related
        # for Entry then every call to __str__ would cause another query for the related Entry object.
        self.assertTrue(str(clue.entry.id) in string_repr)
        self.assertTrue(clue.clue_text in string_repr)

    def test_entry(self):
        entry = EntryFactory()
        string_repr = str(entry)
        self.assertTrue(entry.entry_text in string_repr)

    def test_puzzle(self):
        puzzle = PuzzleFactory()
        string_repr = str(puzzle)
        self.assertTrue(puzzle.publisher in string_repr)
        self.assertTrue(str(puzzle.publication_date) in string_repr)
