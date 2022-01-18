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

"""Quandary main."""

from quandary.analysis import resolve_quandary, analyze_stability
from quandary.configuration import parse_configuration_file
from quandary.report import produce_report


import argparse

from .data import Options, DESCRIPTION, \
    DEFAULT_DECIMAL_PLACES, MINIMUM_DECIMAL_PLACES, MAXIMUM_DECIMAL_PLACES, \
    DEFAULT_RANDOM_STEPS, MINIMUM_RANDOM_STEPS, MAXIMUM_RANDOM_STEPS, \
    DEFAULT_RANDOM_TRIALS, MINIMUM_RANDOM_TRIALS, MAXIMUM_RANDOM_TRIALS, \
    DEFAULT_STABILITY_PERCENTAGE
from .utility import critical_error


def _get_integer_argument(args: argparse.Namespace,
                          dest: str,
                          min_value: int,
                          max_value: int,
                          ) -> int:
    try:
        value = int(getattr(args, dest))
        if value < min_value:
            critical_error(f'{dest} value must be >= {min_value}.')
        if value > max_value:
            critical_error(f'{dest} value must be <= {max_value}.')
        return value
    except TypeError as exc:
        critical_error(f'{dest} value exception: {getattr(args, dest)}: {exc}')


def _parse_command_line() -> Options:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-p', '--decimal-places',
        dest='DECIMAL_PLACES',
        default=DEFAULT_DECIMAL_PLACES,
        help=f'number of decimal places to display'
             f' (default: {DEFAULT_DECIMAL_PLACES})')
    parser.add_argument(
        '-r', '--random-steps',
        dest='RANDOM_STEPS',
        default=DEFAULT_RANDOM_STEPS,
        help=f'number of stability randomization steps'
             f' (default: {DEFAULT_RANDOM_STEPS})')
    parser.add_argument(
        '-t', '--random-trials',
        dest='RANDOM_TRIALS',
        default=DEFAULT_RANDOM_TRIALS,
        help=f'number of stability randomization trials'
             f' (default: {DEFAULT_RANDOM_TRIALS})')
    parser.add_argument(
        '-s', '--stability-percent',
        dest='STABILITY_PERCENTAGE',
        default=DEFAULT_STABILITY_PERCENTAGE,
        help=f'unchanged rankings trials %% considered stable'
             f' (default: {DEFAULT_STABILITY_PERCENTAGE}%%,'
             f' 0: disabled)')
    parser.add_argument(
        '-d', '--details',
        dest='DETAILS',
        action='store_true',
        help='display extra details in report')
    parser.add_argument(
        dest='QUANDARY_PATHS',
        nargs='+',
        help='configuration file path(s)')
    args = parser.parse_args()
    decimal_places = _get_integer_argument(
        args, 'DECIMAL_PLACES', MINIMUM_DECIMAL_PLACES, MAXIMUM_DECIMAL_PLACES)
    random_steps = _get_integer_argument(
        args, 'RANDOM_STEPS', MINIMUM_RANDOM_STEPS, MAXIMUM_RANDOM_STEPS)
    random_trials = _get_integer_argument(
        args, 'RANDOM_TRIALS', MINIMUM_RANDOM_TRIALS, MAXIMUM_RANDOM_TRIALS)
    stability_percentage = _get_integer_argument(
        args, 'STABILITY_PERCENTAGE', 0, 100)
    return Options(decimal_places,
                   random_steps,
                   random_trials,
                   stability_percentage,
                   args.DETAILS,
                   args.QUANDARY_PATHS)


def main():
    """Main function parses the command line and produces report(s)."""
    options = _parse_command_line()
    for config_path in options.quandary_paths:
        quandary = parse_configuration_file(config_path)
        results = resolve_quandary(quandary)
        stability = analyze_stability(quandary,
                                      results,
                                      random_steps=options.random_steps,
                                      random_trials=options.random_trials,
                                      stability_percentage=options.stability_percentage)
        produce_report(quandary,
                       results,
                       decimal_places=options.decimal_places,
                       confidence=stability,
                       details=options.details)


# This module can be run directly.
if __name__ == '__main__':
    main()
