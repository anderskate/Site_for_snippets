from django.db import models
from django.shortcuts import reverse
import uuid
import re


class Snippet(models.Model):
    id = models.UUIDField('уникальный id', primary_key=True, default=uuid.uuid4)
    title = models.CharField('название сниппета', max_length=200)
    date_pub = models.DateTimeField('дата создания', auto_now_add=True)

    PRIVATE_STATUS = (
        ('y', 'Да'),
        ('n', 'Нет'),
    )
    status = models.CharField(
        'является ли приватным', 
        max_length=1, 
        choices=PRIVATE_STATUS, 
        default='n',
    )

    class Meta:
        ordering = ['-date_pub']

    def get_absolute_url(self):
        return reverse('snippet_datail_url', args=[str(self.id)])


    def get_number_of_files(self):
        return len(self.pieceofcode_set.all())

    def get_code_preview(self):
        first_part_code = self.pieceofcode_set.first().code
        line_feed_character_indices = [m.start() for m in re.finditer('\n', first_part_code)]
        if len(line_feed_character_indices) < 10:
            return first_part_code
        else:
            index = line_feed_character_indices[9]
            return first_part_code[:index]

    def __str__(self):
        return self.title


class PieceOfCode(models.Model):
    snippet = models.ForeignKey(Snippet, verbose_name='сниппет', on_delete=models.CASCADE)
    LANGUAGES = (
        (None, '------'),
        ('py', 'Python'),
        ('js', 'Javascript'),
        ('php', 'PHP'),
        ('java', 'Java'),
        ('swift', 'Swift'),
        )
    language = models.CharField(
        'язык программирования', 
        max_length=5, 
        choices=LANGUAGES, 
        blank=True,
    )
    code = models.TextField('код')

    def __str__(self):
        return '{code_id} код сниппета {snippet}'.format(
            code_id = self.id,
            snippet = self.snippet.title
            )
