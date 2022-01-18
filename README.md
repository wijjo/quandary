# Quandary Resolver

## Introduction

Quandary is a decision-support tool.

A "quandary" is a problem with a difficult set of choices. The Quandary tool
provides a way for users to break down such problems into a set of data that
allows for automated analysis.

The data format is designed to make it as easy as possible for users to describe
a quandary. Ratings are specified visually, not numerically, in a compact form.

The tool evaluates choices based on user-defined criteria, ratings, and
priorities in order to produce ranked results.

Quandary problems are expressed as [YAML](https://yaml.org) configuration files.
See "Configuration file format reference."

## Confidence and Stress Testing

The Quandary tool stress tests input data in order to produce a "confidence"
rating, which can hint to a user how useful the results might be.

The stress testing process runs a series of tests with increasing
randomization levels applied to choice and criteria ratings.

Each randomization level runs repeated trials, reapplying the same randomization
amount, but producing different input data variations. Having many trial
repetitions should help minimize variability between runs, despite using
randomized data.

A randomization level is considered unstable when it results in more than a
certain percentage trials with altered rankings. The confidence rating
represents the highest randomization level with stable results.

For now, the confidence rating is primarily useful as a relative value to help
users compare multiple results. There is currently no guidance for how to
interpret a confidence rating on its own.

Note that command line options exist which offer ways to alter stress testing
parameters, like the stability threshold percentage, the number of randomization
steps, and the number of trials per step.

## Quandary Configurations (YAML format files)

Quandaries are defined in [YAML](https://yaml.org) format configuration files.

Configurations include the following information:

* A set of choices (alternatives).
* A set of criteria for rating choices.
  * Each criterion has a ratings bar to rate choices along a horizontal axis.
* A priority ratings bar provides relative criteria importance.

Please refer to the [YAML](https://yaml.org) documentation for more information
about its syntax rules. In most cases it may be easier to just start with the
example configuration as a basis for creating your own.

## Ratings Bars

Ratings bars provide a concise format for rating multiple choices or criteria.
It arranges letters corresponding to individual elements, such as choices or
criteria, along a horizontal axis. Quandary converts letter positions to ratings
based on their distance along the axis.

With ratings bars, users can focus on a visual arrangement, and how things 
compare relatively, instead of needing to produce specific numbers.

Ratings bar axes may have arbitrary width. The example configuration use 50
character wide ratings bars. Longer bars can be employed for large alternative
quantities, or for finer ratings resolution.

Gaps between letters can be occupied by most non-alphabetic characters. Blank
(" "), underscore ("_"), period ("."), hyphen ("-"), and caret ("^") of valid
filler characters.

Depending on what filler character is chosen, please be aware that YAML syntax
rules require quotes around strings containing certain special characters. An
editor with YAML syntax support should help highlight YAML rule violations.

Future graphical applications could present ratings bars as slider controls with
multiple "thumb" inputs, one for each choice or criterion letter. This is just
one possible representation, primarily to help visualize how ratings bars
function.

## Results Report

After loading the quandary configuration, the program reports the following
results:

* Ranked choices in calculated total ratings order.
* Confidence rating (see "Confidence and stress testing.").

The "-d"/"--details" option provides more detailed results, including the rating
numbers derived from the configured ratings bars.

## Configuration File Format Reference

The configuration file uses YAML format. The overall format is a YAML dictionary
with four major section keys: "quandary", "choices", "criteria", and
"priorities". See below for more information about each section.

Rather than spending time to read and understand this reference section, it may
be simpler to first look at the configuration example.

### "quandary" Section

The "quandary" section provides general descriptive information.

#### "quandary" Section Properties

* **description**: Description of quandary.

### "choices" Section

The "choices" section lays out alternative choices. It is formatted as a YAML
dictionary with a letter serving as the key for each choice item.

#### "choices" Section Item Properties

* **name** - Choice name.
* **(other)** - Other arbitrary properties can provide additional data, 
  e.g. cost. They are only meaningful to users, and ignored by the tool.

### "criteria" Section

The "criteria" section specifies one or more criteria with accompanying ratings.
It is formatted as a YAML dictionary with a letter serving as the key for each
criterion item.

#### "criteria" Section Item Properties

* **name** - Criterion name or description.
* **choices** - Choices ratings bar for relative ratings by choice letter.

### "priorities" Section

The "priorities" section provides priority ratings for the criteria.

#### "priorities" Properties

* **criteria** - Criteria ratings bar for relative ratings by criterion letter.

## Configuration File Example (YAML)

The quandary configuration below compares 3 premium e-reader devices.

#### File: ereaders.yaml

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

The following is an example shell session for the above configuration.

```bash 
$ quandary ereaders.yaml

::: Premium E-Readers :::

RANK  RATING  CHOICE
   1    4.64  Kobo Libra 2
   2    4.42  Kobo Sage
   3    4.02  Paperwhite Signature

Confidence: 9%

Confidence is the highest random stress percentage with stable rankings.
```

## Installation

For now, the easiest and probably best way to install Quandary is to work with a
Git "clone" of the GitHub project. This method requires Git be installed and
available in the shell environment, and that users have some familiarity with
its commands.

The example below, and the rest of this document, assumes the installation
folder is "quandary" under the user's home folder, i.e. "~/quandary".

The following commands should, at minimum, work in Macintosh and Linux (Bash)
shell environments.

```bash
$ cd
$ git clone https://github.com/wijjo/quandary.git
$ cd quandary
```

## Running

This section assumes an active Bash shell session, e.g. on a Macintosh or Linux
computer.

### Requirements

* A recent Python (version 3).
* PyYAML library.

As of this writing, Quandary has been tested with Python versions 3.9 and 3.10.
All instructions assume the default system Python is a compatible version.

### Option 1 - Use a Python Virtual Environment

Python [virtual environments](https://docs.python.org/3/library/venv.html) avoid
the need to change the system Python library.

The virtual environment must be activated in order to run Quandary. 

The example below also upgrades the virtual environment's "pip" command for good
measure. The "requirements.txt" file provides the PyYAML dependency for "pip", 
the Python package manager.

```bash
$ cd ~/quandary
$ python -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

### Option 2 - Use the System Python Interpreter

The "pip" command needs administrative permission via the "sudo" command in
order to update the system Python library.

```bash
$ cd ~/quandary
$ sudo pip install -r requirements.txt
```

### Running With the Full Script Path

Quandary can function by using the full path to the "quandary" Bash script in
the project "bin" folder. The script automatically activates any virtual
environment found in a sub-folder named "venv".

```bash
$ ~/quandary/bin/quandary
```

### Running Without the Full Script Path

Quandary can run without the full script path by adding it to the system
execution path. This requires permission to modify one of the system path
folders.

A simple way to add "quandary" to the path is to create a soft link, a.k.a. 
"symlink", back to the "bin/quandary" script in one of the path folders.

When run through a symlink, the "quandary" script finds all required components
using paths relative to the script source file.

The example below assumes the user "~/bin" folder is in the execution path, and
that Quandary resides in "~/quandary". It tests the command by requesting help.

```bash
$ cd ~/bin
$ ln -s ~/quandary/bin/quandary .
$ hash -r
$ cd
$ quandary -h
```

### Requesting Command Line Help

The "-h"/"--help" command line option list describes the program and its
supported options and arguments.

```bash
$ quandary -h
```

### Running a Configured Quandary

Given a quandary configuration file "myquandary.yaml", run the following to
display quandary analysis results.

```bash
$ quandary myquandary.yaml
```

### Running a Configured Quandary With Detailed Output

The "-d"/"--details" option provides more detailed results, including the rating
values derived from configured ratings bars.

```bash
$ quandary myquandary.yaml -d
```
