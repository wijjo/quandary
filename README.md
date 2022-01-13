# Quandary "solver".

Quandaries are problems with a set of difficult choices. This tool provides a
way to break them down into a data format expressed as YAML configuration files.
It evaluates choices based on user-defined factors, ratings, and priorities in
order to produce ranked results.

It also tests the input data by adding some randomization in order to see how
stable the results are. If small random ratings changes alter the rankings it is
considered unstable. The random stress tests all users to decide how confident
they are in the results.

## Input data (from YAML configuration).

Quandaries are defined by the following information:

* A set of alternative choices.
* A set of factors for rating them.
* Spread bars for each factor that rate the choices along an axis.
* A priority spread bar that rates the importance of all the factors.

The above information is defined by the user in quandary configuration (YAML).

## Spread bars.

Spread bars allow placement of letters along an X axis of arbitrary length to
specify multiple ratings in a visually-meaningful arrangement. The position of
each rating letter determines the rating. A choice spread bar use choice letters
placed along the axis. A factor priority spread bar use factor letters placed
along the axis.

If this becomes a graphical application spread bars could be implemented as
slider controls with multiple sliders.

## Output report.

After loading the configuration the program reports the following:

* Best choices in overall ratings order.
* Stability rating.

The stability rating is calculated as follows:

* Apply a series of perturbation percentages (+ and -) to all ratings.
* For each perturbation percentage run a number of random trials.
* If the rankings change more than a threshold percentage of trials that
  perturbation percentage is taken as the stability rating.

## Configuration file example (YAML):

```yaml
title: Premium E-Readers

choices:
  s: Kobo Sage
  l: Kobo Libra 2
  p: Paperwhite Signature

factors:
  a: annotations
  c: cost
  d: display
  e: ergonomics
  i: importing
  l: library
  p: power
  s: store
  u: usability
  v: versatility

ratings:
  a: ______________lp__________________________s_______
  c: __________s___________l___p_______________________
  d: ____________________________________p___l___s_____
  e: ______________________________p_____s___l_________
  i: ____________________________________p__l______s___
  l: __________________________p_____________________sl
  p: ______________________s_______________pl__________
  s: ________________________sl_______________________p
  u: ______________________________p________ls_________
  v: ___________p______________________sl______________

priorities: _____a____________v____c__i__p___u______des___l___
```
