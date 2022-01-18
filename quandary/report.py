# Copyright (C) 2022, Steven Cooper
#
# This file is part of Quandary.
#
# Quandary is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Quandary is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Quandary.  If not, see <https://www.gnu.org/licenses/>.

"""Quandary report production."""

from .data import Quandary, Results, DEFAULT_DECIMAL_PLACES


def produce_report(quandary: Quandary,
                   results: Results,
                   decimal_places: int = DEFAULT_DECIMAL_PLACES,
                   confidence: float = None,
                   details: bool = False,
                   ):
    """
    Load quandary file and display evaluation report.

    :param quandary: quandary definition
    :param results: analysis results
    :param decimal_places: number of decimal places
    :param confidence: optional confidence rating
    :param details: display extra details if True
    """
    rating_format = f'%{decimal_places + 2}.{decimal_places}f'
    row_format = f'%4d  %6.{decimal_places}f  %s'
    print(f'''
::: {quandary.description} :::
''')
    print(f'''\
RANK  RATING  CHOICE\
''')
    for idx, choice_ranking in enumerate(results.choice_rankings):
        row = row_format % (idx + 1, choice_ranking.rating, choice_ranking.label)
        print(f'''\
{row}\
''')
    if confidence is not None:
        print(f'''
Confidence: {confidence * 100:.0f}%

Confidence is the highest random stress percentage with stable rankings.
''')
    if details:
        print('''\
::: Choices :::
''')
        for choice_letter in sorted(quandary.choices.keys()):
            print(f'''\
[{choice_letter}] {quandary.choices[choice_letter]}\
''')
        print('''
::: Criteria with choices ordered by rating (adjusted rating) :::\
''')
        for criterion_letter in sorted(quandary.criteria.keys()):
            criterion = quandary.criteria[criterion_letter]
            priority = quandary.priority_ratings[criterion_letter]
            print(f'''
[{criterion_letter}] {criterion.label}\
''')
            sorted_choices = sorted(criterion.choice_ratings.items(),
                                    key=lambda pair: pair[1], reverse=True)
            for choice_letter, choice_rating in sorted_choices:
                rating_string = rating_format % choice_rating
                adj_rating_string = rating_format % (choice_rating * priority)
                print(f'''\
   {rating_string} ({adj_rating_string}) [{choice_letter}] {quandary.choices[choice_letter]}\
''')
        print('''
::: Priorities with criteria ordered by rating :::
''')
        sorted_criteria = sorted(quandary.priority_ratings.items(),
                                 key=lambda pair: pair[1], reverse=True)
        for criterion_letter, criterion_rating in sorted_criteria:
            criterion = quandary.criteria[criterion_letter]
            rating_string = rating_format % criterion_rating
            print(f'''\
{rating_string} [{criterion_letter}] {criterion.label}\
            ''')
        print('')
