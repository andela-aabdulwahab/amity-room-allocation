[![Build Status](https://travis-ci.org/andela-aabdulwahab/checkpoint_one.svg?branch=develop)](https://travis-ci.org/andela-aabdulwahab/checkpoint_one)
[![Coverage Status](https://coveralls.io/repos/github/andela-aabdulwahab/checkpoint_one/badge.svg?branch=develop)](https://coveralls.io/github/andela-aabdulwahab/checkpoint_one?branch=develop)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/andela-aabdulwahab/checkpoint_one/badges/quality-score.png?b=develop)](https://scrutinizer-ci.com/g/andela-aabdulwahab/checkpoint_one/?branch=develop)

# Office Space Allocation App

Space Allocation app for managing living space and office space at one of Andela's facilities, Amity. Person added to the system can be a FELLOW or a STAFF and a room can be an Office or a Living Space.

Rooms are allocated randomly to person when added to the application. Living space can take a maximum of 4 while office can take 6.

> **Note:** Office is available to Staff and Fellow
> but Living space is available to only fellows
> choose to have one.

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

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