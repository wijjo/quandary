# Quandary "solver".

Quandaries are problems with a set of difficult choices. This tool provides a
way to break them down into a data format expressed as YAML configuration files.
It evaluates choices based on user-defined criteria, ratings, and priorities in
order to produce ranked results.

It also tests the input data by adding some randomization in order to see how
stable the results are. If small random ratings changes alter the rankings it is
considered unstable. The random stress tests all users to decide how confident
they are in the results.

## Input data (from YAML configuration).

Quandaries are defined by the following information:

* A set of choices (alternatives).
* A set of criteria for rating them.
* Spread bars for each criterion that rate the choices along an axis.
* A priority spread bar that rates the importance of all the criteria.

The above information is defined by the user in quandary configuration (YAML).

## Spread bars.

Spread bars provide ratings for choices or criteria by arranging corresponding
letters along a horizontal axis. Letter positions imply ratings based on their
distance along the axis. 

The axis can have an arbitrary length. The spread bars in the example
configuration below are 50 characters wide. A longer axis can help when there
are more choices or criteria, or when a finer resolution is desired.

Gaps between letters can be occupied by blanks or any non-letter characters,
e.g. underscore ("_"), period ("."), hyphen ("-"), caret ("^"), etc.. Whatever
filler characters you choice, make sure to quote the spread bar string if YAML
syntax rules require it.

The spread bar format allows specification of multiple ratings in a
visually-meaningful arrangement. 

Criterion "choices" spread bars rates choices relative to each other.

A priorities "criteria" spread bar rates criteria relative to each other.

In a graphical application a spread bar could be represented by a slider control
with multiple thumb inputs, one for each choice or criterion letter.

## Output report.

After loading the configuration the program reports the following:

* Best choices in overall ratings order.
* Stability rating.

The stability rating is calculated as follows:

* Apply a series of perturbation percentages (+ and -) to all ratings.
* For each perturbation percentage run a number of random trials.
* If the rankings change more than a threshold percentage of trials that
  perturbation percentage is taken as the stability rating.

## Configuration file format.

The configuration file uses YAML format. The overall format is a YAML dictionary
with four major section keys, "quandary", "choices", "criteria", and
"priorities". See below for more information about each section.

### "quandary" section.

The "quandary" section provides general descriptive information.

#### "quandary" properties.

- **description**: Description of quandary.

### "choices" section.

The "choices" section lays out alternative choices. It is formatted as a YAML
dictionary with a letter serving as the key for each choice item.

#### Choice item properties.

- **name** - Choice name.
- **(other)** - Other arbitrary properties can provide additional data, 
  e.g. cost.  

### "criteria" section.

The "criteria" section specifies one or more criteria with accompanying ratings.
It is formatted as a YAML dictionary with a letter service as the key for each
criterion item.

#### Criterion item properties.

- **name** - Criterion name or description.
- **choices** - Choices spread bar for relative ratings by choice letter.

### "priorities" section.

The "priorities" section provides priority ratings for the criteria.

#### "priorities" properties.

- **criteria** - Criteria spread bar for relative ratings by criterion letter.

## Configuration file example (YAML):

The example configuration compares 3 premium e-readers. It should work as input
to the quandary program, and produce a reasonable result.

```yaml
quandary:
  description: Premium E-Readers

choices:
  S:
    name: Kobo Sage
    cost: 260
  L:
    name: Kobo Libra 2
    cost: 180
  P:
    name: Paperwhite Signature
    cost: 152

criteria:
  A:
    name: Annotation support
    ratings: ______________LP__________________________S_______
  B:
    name: Battery and power
    ratings: ______________________S_______________PL__________
  C:
    name: Cost
    ratings: __________S___________L___P_______________________
  D:
    name: Display
    ratings: ____________________________________P___L___S_____
  E:
    name: Ergonomics
    ratings: ______________________________P_____S___L_________
  F:
    name: File format support
    ratings: ____________________________________P__L______S___
  L:
    name: Library
    ratings: __________________________P_____________________SL
  S:
    name: Store
    ratings: ________________________SL_______________________P
  U:
    name: Usability
    ratings: ______________________________P________LS_________
  V:
    name: Versatility
    ratings: ___________P______________________SL______________

priorities:
  ratings: _____A____________V____C__F__B___U___S___DE___L___
```
