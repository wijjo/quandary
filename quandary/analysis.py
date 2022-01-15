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

"""Quandary analysis."""

import random
from typing import List, Set, Iterable, Optional

from .data import Quandary, Results, GenericLetter, CriteriaMap, Criterion, \
    ChoiceRatings, ChoiceResult, GenericRatings, PriorityRatings, \
    DEFAULT_RANDOM_STEPS, DEFAULT_RANDOM_TRIALS, DEFAULT_STABILITY_PERCENTAGE
from .utility import error


class _QuandaryRandomizer:
    """Can perform multiple random perturbations of a given quandary."""

    def __init__(self, quandary: Quandary):
        self.quandary = quandary

    @classmethod
    def _randomize_rating(cls, rating: float, perturbation: float) -> float:
        return max(min(rating + random.choice([perturbation, -perturbation]), 1), 0)

    @classmethod
    def _randomize_generic_ratings(cls, ratings: GenericRatings, factor: float) -> GenericRatings:
        return {
            letter: cls._randomize_rating(rating, factor)
            for letter, rating in ratings.items()
        }

    def _randomize_criteria(self, perturbation: float) -> CriteriaMap:
        criteria: CriteriaMap = {}
        for criterion_letter, criterion in self.quandary.criteria.items():
            choice_ratings = self._randomize_generic_ratings(criterion.choice_ratings,
                                                             perturbation)
            criteria[criterion_letter] = Criterion(criterion.label, choice_ratings)
        return criteria

    def _randomize_priorities(self, perturbation: float) -> PriorityRatings:
        return self._randomize_generic_ratings(self.quandary.priority_ratings, perturbation)

    def randomize(self, perturbation: float) -> Quandary:
        return Quandary(f'{self.quandary.description} [randomization={perturbation:.2f}%]',
                        dict(self.quandary.choices),
                        self._randomize_criteria(perturbation),
                        self._randomize_priorities(perturbation))


def _report_unknown_letters(letters: Iterable[GenericLetter], label: str, section: str):
    sorted_letters = sorted(letters)
    if letters:
        error(f'Ignored unknown {label} {"letters" if len(sorted_letters) > 1 else "letter"}'
              f' "{" ".join(sorted_letters)}" in quandary "{section}"')


def analyze_stability(quandary: Quandary,
                      results: Results,
                      random_steps: int = DEFAULT_RANDOM_STEPS,
                      random_trials: int = DEFAULT_RANDOM_TRIALS,
                      stability_percentage: int = DEFAULT_STABILITY_PERCENTAGE,
                      ) -> Optional[float]:
    """
    Calculate stability (see README.md for more information).

    :param quandary: quandary definition
    :param results: results data
    :param random_steps: number of random steps (increments)
    :param random_trials: number of random trials
    :param stability_percentage: percent limit for considering stable
    :return: stability value (between 0 and 1) or None if stability % is 0
    """
    if stability_percentage == 0:
        return None
    ranked_labels = [ranking.label for ranking in results.choice_rankings]
    quandary_randomizer = _QuandaryRandomizer(quandary)
    volatility_threshold = (100 - stability_percentage) / 100
    stability = 0
    for random_step in range(1, random_steps + 1):
        perturbation = random_step / random_steps
        changed_count = 0
        for _trial in range(1, random_trials + 1):
            randomized_quandary = quandary_randomizer.randomize(perturbation)
            results = resolve_quandary(randomized_quandary)
            trial_ranked_labels = [ranking.label for ranking in results.choice_rankings]
            if trial_ranked_labels != ranked_labels:
                changed_count += 1
        if changed_count / random_trials >= volatility_threshold:
            break
        stability = perturbation
    return stability


def resolve_quandary(quandary: Quandary) -> Results:
    """
    Analyze quandary and provide results.

    :param quandary: quandary definition
    :return: evaluation results
    """
    total_choice_ratings: ChoiceRatings = {letter: 0 for letter in quandary.choices.keys()}
    bad_ratings_criteria: Set[str] = set()
    bad_ratings_choices: Set[str] = set()
    missing_priority_factors: Set[str] = set()
    missing_choice_ratings: Set[str] = set()
    for criterion_letter, criterion in quandary.criteria.items():
        if criterion_letter not in quandary.criteria:
            bad_ratings_criteria.add(criterion_letter)
            continue
        if criterion_letter not in quandary.priority_ratings:
            missing_priority_factors.add(criterion_letter)
            continue
        bad_ratings_choices.update(filter(lambda letter: letter not in quandary.choices,
                                          criterion.choice_ratings.keys()))
        priority = quandary.priority_ratings[criterion_letter]
        for choice_letter in quandary.choices.keys():
            if choice_letter not in quandary.choices:
                bad_ratings_choices.add(choice_letter)
                continue
            if choice_letter not in criterion.choice_ratings:
                missing_choice_ratings.add(choice_letter)
                continue
            total_choice_ratings[choice_letter] += (
                    criterion.choice_ratings[choice_letter] * priority)
    _report_unknown_letters(bad_ratings_criteria, 'factor', 'ratings')
    _report_unknown_letters(bad_ratings_choices, 'choice', 'ratings')
    choice_rankings: List[ChoiceResult] = []
    for choice_letter in quandary.choices.keys():
        label = quandary.choices[choice_letter]
        rating = total_choice_ratings[choice_letter]
        choice_rankings.append(ChoiceResult(label, rating))
    choice_rankings.sort(key=lambda choice_ranking: choice_ranking.rating, reverse=True)
    return Results(choice_rankings)
