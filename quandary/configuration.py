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

"""Quandary configuration loading, parsing, and checking."""

import yaml
from typing import Iterable, Any, Optional, Tuple, List

from .data import ChoicesMap, CriteriaMap, GenericRatings, PriorityRatings, \
    Quandary, Criterion, MINIMUM_RATINGS_BAR_WIDTH
from .utility import critical_error


def _load(config_path: str) -> dict:
    try:
        with open(config_path, encoding='utf-8') as stream:
            raw_data = yaml.safe_load(stream)
            if not isinstance(raw_data, dict):
                critical_error('Configuration is not a YAML dictionary.')
            return raw_data
    except (IOError, OSError) as exc:
        critical_error(f'Failed to load configuration file: {config_path}: {exc}')


def _parse_ratings(label: str,
                   raw_ratings_data: Any,
                   valid_label: str,
                   valid_letters: Iterable[str],
                   ) -> GenericRatings:
    if not isinstance(raw_ratings_data, str):
        critical_error(f'{label}: ratings bar is not a string.')
    ratings_bar = raw_ratings_data
    if len(ratings_bar) < MINIMUM_RATINGS_BAR_WIDTH:
        critical_error(f'{label}: ratings bar is not at least'
                       f' {MINIMUM_RATINGS_BAR_WIDTH} characters wide.')
    divisor = len(ratings_bar) - 1
    ratings = {
        letter.upper(): pos / divisor
        for pos, letter in enumerate(ratings_bar)
        if letter.isalpha()
    }
    _check_letters(label, ratings.keys(), valid_label, valid_letters)
    return ratings


def _check_letters(label: str,
                   input_letters: Iterable[str],
                   valid_label: str,
                   valid_letters: Iterable[str],
                   ):
    input_letter_set = set(input_letters)
    valid_letter_set = set(valid_letters)
    letter_errors: List[str] = []
    extra_letters = sorted(input_letter_set.difference(valid_letter_set))
    if extra_letters:
        letter_errors.append(f'unknown {valid_label} letter(s):'
                             f' {", ".join(extra_letters)}')
    missing_letters = ', '.join(
        sorted(valid_letter_set.difference(input_letter_set)))
    if missing_letters:
        letter_errors.append(f'missing {valid_label} letter(s):'
                             f' {", ".join(missing_letters)}')
    if letter_errors:
        critical_error(f'{label}: {", ".join(letter_errors)}')


class _ConfigurationLoader:

    def __init__(self, config_path: str):
        self.raw_data = _load(config_path)
        self._configuration: Optional[Quandary] = None

    @property
    def configuration(self) -> Quandary:
        if self._configuration is None:
            description = self._parse_description()
            choices = self._parse_choices()
            criteria = self._parse_criteria(choices)
            priorities = self._parse_priorities(criteria)
            self._configuration = Quandary(description, choices, criteria, priorities)
        return self._configuration

    def _parse_description(self) -> str:
        label, quandary_data = self._get_block('quandary')
        if 'description' not in quandary_data:
            critical_error(f'{label} has no "description" element.')
        return str(quandary_data['description'])

    def _parse_choices(self) -> ChoicesMap:
        choices_map: ChoicesMap = {}
        label, choices_data = self._get_block('choices')
        for choice_letter, choice_data in choices_data.items():
            choice_letter = choice_letter.upper()
            if not isinstance(choice_data, dict):
                critical_error(f'Choice "{choice_letter}" is not a dictionary.')
            if 'name' not in choice_data:
                critical_error(f'Choice "{choice_letter}" has no "name" element.')
            choices_map[choice_letter] = str(choice_data['name'])
        return choices_map

    def _parse_criteria(self, choices: ChoicesMap) -> CriteriaMap:
        criteria_map: CriteriaMap = {}
        label, criteria_data = self._get_block('criteria')
        for criterion_letter, criterion_data in criteria_data.items():
            criterion_letter = criterion_letter.upper()
            criterion_label = f'criterion.{criterion_letter}'
            ratings_label = f'{criterion_label}.ratings'
            if not isinstance(criterion_data, dict):
                critical_error(f'{criterion_label} is not a dictionary.')
            if 'name' not in criterion_data:
                critical_error(f'{criterion_label} has no "name" element.')
            if 'ratings' not in criterion_data:
                critical_error(f'{ratings_label} is missing.')
            choice_ratings = _parse_ratings(ratings_label,
                                            criterion_data['ratings'],
                                            'choice',
                                            choices.keys())
            name = str(criterion_data['name'])
            criteria_map[criterion_letter] = Criterion(name, choice_ratings)
        return criteria_map

    def _parse_priorities(self, criteria: CriteriaMap) -> PriorityRatings:
        label, priorities_data = self._get_block('priorities')
        ratings_label = f'{label}.ratings'
        if 'ratings' not in priorities_data:
            critical_error(f'{ratings_label}: missing ratings bar.')
        return _parse_ratings(ratings_label,
                              priorities_data['ratings'],
                              'criterion',
                              criteria.keys())

    def _get_block(self, name: str) -> Tuple[str, dict]:
        label = f'configuration.{name}'
        if name not in self.raw_data:
            critical_error(f'{label}: missing block.')
        block_data = self.raw_data[name]
        if not isinstance(block_data, dict):
            critical_error(f'{label}: block is not a dictionary.')
        return label, block_data


def parse_configuration_file(path: str) -> Quandary:
    """
    Parse YAML configuration file.

    :param path: configuration file path
    :return: parsed quandary data
    """
    return _ConfigurationLoader(path).configuration
