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

"""Quandary data types and constants."""

from dataclasses import dataclass
from typing import List, Dict

# GenericLetter type is cast or replaced by more specific type where it is known.
GenericLetter = str
ChoiceLetter = GenericLetter
CriterionLetter = GenericLetter

ChoiceLabel = str
CriterionLabel = str
RatingsBar = str
Rating = float

# GenericRatings type is cast or replaced by more specific type where it is known.
GenericRatings = Dict[GenericLetter, Rating]
ChoiceRatings = Dict[ChoiceLetter, Rating]
CriteriaChoiceRatings = Dict[CriterionLetter, ChoiceRatings]
PriorityRatings = Dict[CriterionLetter, Rating]
ChoicesMap = Dict[ChoiceLetter, ChoiceLabel]

# Various constants and defaults.
DESCRIPTION = 'Quandary resolver'
DEFAULT_DECIMAL_PLACES = 2
MINIMUM_DECIMAL_PLACES = 0
MAXIMUM_DECIMAL_PLACES = 10
DEFAULT_RANDOM_STEPS = 100
MINIMUM_RANDOM_STEPS = 10
MAXIMUM_RANDOM_STEPS = 1000
DEFAULT_RANDOM_TRIALS = 1000
MINIMUM_RANDOM_TRIALS = 10
MAXIMUM_RANDOM_TRIALS = 10000
DEFAULT_STABILITY_PERCENTAGE = 70
MINIMUM_RATINGS_BAR_WIDTH = 20


@dataclass
class Options:
    """Runtime options."""
    decimal_places: int
    random_steps: int
    random_trials: int
    stability_percentage: int
    details: bool
    quandary_paths: List[str]


@dataclass
class Criterion:
    """Parsed criterion data."""
    label: CriterionLabel
    choice_ratings: ChoiceRatings


CriteriaMap = Dict[CriterionLetter, Criterion]


@dataclass
class Quandary:
    """Quandary definition based on the parsed configuration."""
    description: str
    choices: ChoicesMap
    criteria: CriteriaMap
    priority_ratings: PriorityRatings


@dataclass
class ChoiceResult:
    """Choice result, with rating."""
    label: ChoiceLabel
    rating: float


@dataclass
class Results:
    """Evaluation results with ranked choice results."""
    choice_rankings: List[ChoiceResult]
