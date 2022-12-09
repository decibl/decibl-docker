# decibl-docker

## Installation

1. Install Python 3.10+
2. Run `pip install -r requirements.txt`

## File Structure

The Project is Structured as follows:

<!-- src/ has backups/ databases/ core/ logs/ soundfiles/ tests/ -->

```bash
src/
├── databases/
|── backups/
|── core/
|── logs/
|── soundfiles/
|── tests/
```

Let's go over what each one of them does and why they are important.

# src

Also called `source`. Where all the actual code is stored. This is the only folder that is actually required to run the project. All the files outside of this folder are for development purposes only.

Most large projects use a `src` folder.

## analyticsdb

**Note: This folder is generated automatically when the project is run.**

This folder contains the physical database file. This is where analyticsdb.py stores all the data/retrieves it, and is the overall "homebase" for all the analytics. Look at the analyticsdb.py file for more information.

## backups

**Note: This folder is generated automatically when the project is run.**

This folder contains the backups of the database and logs. It is automatically generated when the project is run, and is used to store backups of the database and logs. Look at the analyticsdb.py and config.py files for more information.

## core

This folder contains the core files of the project. These are the files that are used to run the project.

```bash
core/
├── analyticsdb.py
|── config.py
|── songparser.py
```

## logs

**Note: This folder is generated automatically when the project is run.**

This folder contains the logs of the project. It is automatically generated when the project is run, and is used to store logs of the project. Look at the config.py file for more information.

## soundfiles

This folder contains the physical sound files of the project. This is where the project gets the sound files from. Look at the songparser.py file for more information.

## tests

This folder contains the tests for the project. Run `pytest` to run the tests. Look at the tests for more information.

---

# TODO list

1. Add a way to query all songs in a playlist
2. Add a way to query all songs by an artist
3. Add a way to query all songs by a genre
4. Only create tables if they don't already exist
5. Add more support for song files (mp3, wav, m4a, etc.)
6. Add a way to add a song from a raw file
7. Add a way to remove an entry using a raw file
8. Add CircleCI support
9. **ADD MORE UNIT TESTS!!**
10. Start resarching sync algorithms
11. Implement Sync algorithms
    - SYNC soundfiles (the actual sound data)
    - SYNC Analyticsdb (there will be an exac copy on the user's end, we want to add their data to our table and delete theirs)
12. Add the API
13. Add AUTH to the API
14. Fix the logs, add option to hold X amount of logs or delete logs older than X days or something so they dont get a gazillion bytes big
15. Overall add a ton of useful database queries.
16. Implement "spotify wrapped" and other cool animated graphics with the data we have! (this will be very late down the line, but think about it still)
17. Implement the [linux-server.io S6 overlay for the docker container](https://github.com/just-containers/s6-overlay).
18. Add the docker container
19. Add automatic image building in circle-ci
