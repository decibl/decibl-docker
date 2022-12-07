# decibl-docker

## Installation

1. Install Python 3.10+
2. Run `pip install -r requirements.txt`

## File Structure

The Project is Structured as follows:

<!-- src/ has backups/ analyticsdb/ core/ logs/ soundfiles/ tests/ -->
```bash
src/
├── analyticsdb/
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

__Note: This folder is generated automatically when the project is run.__

This folder contains the physical database file. This is where analyticsdb.py stores all the data/retrieves it, and is the overall "homebase" for all the analytics. Look at the analyticsdb.py file for more information.

## backups

__Note: This folder is generated automatically when the project is run.__

This folder contains the backups of the database and logs. It is automatically generated when the project is run, and is used to store backups of the database and logs. Look at the analyticsdb.py and config.py files for more information.

## core

This folder contains the core files of the project. These are the files that are used to run the project. 

```bash
core/
├── analyticsdb.py
|── config.py
|── songparser.py
```

## analyticsdb.py

### Overview

The main file that interacts with the database. Responsible for creating, adding, and retrieving data from the database. Here's some important infomation about the file:

This file interacts with the analytics database using a SQLite3 database. This is the main file that interacts with the database. It is responsible for creating, adding, and retrieving data from the database. 

Create an AnalyticsDBHandler object and run commands to do stuff. 

```python
dbhandler = AnalyticsDBHandler() # make the object
dbhandler.create_all_tables() # create all the tables
dbhandler.populate_database() # looks into soundfiles/ folder and adds all the info to the tables
dbhandler.get_song_by_id(1) # get the song with the id of 1
```

The file is split up into different sections, you'll see a large comment break between each section.

All the funtions run raw sqlite3, so there isn't a rigid structure to the database. 

### Important Functions

#### create_all_tables()

**You have to create the tables before doing anything with the data!**

If you don't run this command (if the tables don't already exist), you'll get constant errors. Also once created, the data persists between runs of the program (they're stored in the file analyticsdb.db). 

If you delete the file or it doesn't exist, run this command to create the tables.

#### populate_database()

The bread and butter of the file. This function looks into the soundfiles/ folder and adds all the info to the tables. *This includes adding data to multiple databases at once, it handles all the hard work for you.*

Realistically, this is the only function we'll be needing to add data to the table.

It accounts for duplicates, so look for WARNING messages in the logs if you're adding a lot of data.

#### insert_song(**kwargs)

Yeah, there's a ton of parameters. This function is used to insert a song into the database. It's a bit of a pain to use, but it's the only way to insert a song into the database. Look at songparser.py for more info.



## config.py

The main file that contains all the configuration variables. Look at the file for more information.

#### songparser.py

Responsible for parsing the song files and extracting their metadata.

### logs

__Note: This folder is generated automatically when the project is run.__

This folder contains the logs of the project. It is automatically generated when the project is run, and is used to store logs of the project. Look at the config.py file for more information.

### soundfiles

This folder contains the physical sound files of the project. This is where the project gets the sound files from. Look at the songparser.py file for more information.

### tests

This folder contains the tests for the project. Run `pytest` to run the tests. Look at the tests for more information.  

---

# TODO list

1. Add a way to query all songs in a playlist
2. Add a way to query all songs by an artist
3. Add a way to query all songs by a genre
4. Only create tables if they don't already exist
5. Add more support for song files (mp3, wav, m4a, etc.)