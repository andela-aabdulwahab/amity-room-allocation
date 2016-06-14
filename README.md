[![Build Status](https://travis-ci.org/andela-aabdulwahab/amity-room-allocation.svg?branch=develop)](https://travis-ci.org/andela-aabdulwahab/amity-room-allocation)
[![Coverage Status](https://coveralls.io/repos/github/andela-aabdulwahab/checkpoint_one/badge.svg?branch=develop)](https://coveralls.io/github/andela-aabdulwahab/checkpoint_one?branch=develop)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/andela-aabdulwahab/checkpoint_one/badges/quality-score.png?b=develop)](https://scrutinizer-ci.com/g/andela-aabdulwahab/checkpoint_one/?branch=develop)

# Room Allocation Software

Room allocation software for managing living space and office space at one of Andela's facilities, Amity. Person added to the system can be a **fellow** or a **staff** and a room can be an **office** or a **living** Space.

Rooms are allocated randomly to person when added to the application. Living space can take a maximum of 4 while office can take 6.

> **Note:** Office is available to Staff and Fellow
> but Living space is available to only fellows who
> choose to have one.

### Requirements

The application needs the folloing modules to work

* Docopt
* coverage
* nose
* pytest


### Set Up

You'll need python 3.* to run the application

Activate Virtual enviroment for installing requirements

```sh
$ git clone https://github.com/andela-aabdulwahab/checkpoint_one.git
$ cd checkpoint_one
$ pip install -r requirements
$ python app/app.py --help
```

# Usage
```sh
$ app.py create_room (<room_name> <room_type> [-g=RG])...
$ app.py add_person <first_name> <last_name> <gender> <person_type> [-w=WA]
$ app.py relocate_person <person_identifier> <new_room_name>
$ app.py delete_room <room_name>
$ app.py delete_person <person_id>
$ app.py print_persons
$ app.py print_allocation [-o=FN]
$ app.py print_unallocated [-o=FN]
$ app.py print_room <room_name>
$ app.py save_state [-b=SQLD]
$ app.py load_state <db_path>

```
## options
```sh
option:
   -help -h                               Geting help on using the program
   -g RG, --rgender=RG                    To specify gender of Occupant of a living room
   -w WA, --wants_accom=WA                An option argument to specify that person want accomodation
   -o FN, --option=FN                     Optional file name when printing to file
   -b SQLD --db=SQLD                      Database to load from the path provided
```
### Demonstration
> demo video can be found at
> [checkpoint_one_demo](https://asciinema.org/a/6oxp8ocmdx5qhc4c3v534dg94)
