from django.db import models


class Puzzle(models.Model):
    title = models.CharField(max_length=255, null=True)
    # Changed field to publication_date because 'date' shadows common object name from datetime module
    publication_date = models.DateField()
    byline = models.CharField(max_length=255)
    publisher = models.CharField(max_length=12)

    def __str__(self):
        return '{}/{}/{}/{}'.format(self.title, str(self.publication_date), self.byline, self.publisher)


class Entry(models.Model):
    entry_text = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.entry_text


class Clue(models.Model):
    entry = models.ForeignKey(Entry, models.PROTECT)
    puzzle = models.ForeignKey(Puzzle, models.PROTECT)
    clue_text = models.CharField(max_length=512)
    theme = models.BooleanField(default=False)

    def __str__(self):
        return '{}/{}/{}/{}'.format(self.entry_id, self.puzzle_id, self.clue_text, self.theme)

