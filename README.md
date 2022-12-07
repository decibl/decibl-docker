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

The bread and butter of the file. This function looks into the soundfiles/ folder and adds all the info to the tables. _This includes adding data to multiple databases at once, it handles all the hard work for you._

Realistically, this is the only function we'll be needing to add data to the table.

It accounts for duplicates, so look for WARNING messages in the logs if you're adding a lot of data.

#### insert_song(\*\*kwargs)

Yeah, there's a ton of parameters. This function is used to insert a song into the database. It's a bit of a pain to use, but it's the only way to insert a song into the database. Look at songparser.py for more info.

## config.py

The main file that contains all the configuration variables. Has tons of handy dandy info the rest of the program might need. Here's some important variables it contains:

<!-- LOGGING_LEVEL = logging.DEBUG
# For logging format, do datetime + file location then message
LOGGING_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# make filename based on date
LOGGING_FILENAME = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "log_{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))))
LOGGING_ENCODING = "utf-8"

if not os.path.exists(os.path.dirname(LOGGING_FILENAME)):
    os.makedirs(os.path.dirname(LOGGING_FILENAME))


logging.basicConfig(filename=LOGGING_FILENAME, encoding=LOGGING_ENCODING, level=LOGGING_LEVEL, format=LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)
logging.debug("Making folder for logs")


logging.info("Loading config file")
logger = logging.getLogger("Rotating Time Log")
handler = TimedRotatingFileHandler(LOGGING_FILENAME,
                                    when="h",
                                    interval=1,)
logger.addHandler(handler)

# log a message that the config file has been loaded
logging.info("Loaded config file")

# make logging folder if it doesn't exist

# ---------------------------------------------------------------------------------------------
#                                      Database
# ---------------------------------------------------------------------------------------------

DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "analyticsdb", "analytics.db"))

# make database folder if it doesn't exist
logging.info("Making folder for database")
if not os.path.exists(os.path.dirname(DATABASE_PATH)):
    os.makedirs(os.path.dirname(DATABASE_PATH))

# ---------------------------------------------------------------------------------------------
#                                      Sound Files
# ---------------------------------------------------------------------------------------------

# make sound folder if it doesn't exist
logging.info("Making folder for sound files")
SOUNDFILES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "soundfiles"))
if not os.path.exists(SOUNDFILES_PATH):
    os.makedirs(SOUNDFILES_PATH)


# ---------------------------------------------------------------------------------------------
#                                      Backups
# ---------------------------------------------------------------------------------------------

BACKUPS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups"))
DATABASE_BACKUP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups", "database"))
LOGS_BACKUP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups", "logs"))
# make backup folder if it doesn't exist
logging.info("Making folder for backups")
if not os.path.exists(BACKUPS_PATH):
    os.makedirs(BACKUPS_PATH)
if not os.path.exists(DATABASE_BACKUP_PATH):
    os.makedirs(DATABASE_BACKUP_PATH)
if not os.path.exists(LOGS_BACKUP_PATH):
    os.makedirs(LOGS_BACKUP_PATH) -->

### Logging

- `LOGGING_LEVEL` - The logging level of the project. This should be always be DEBUG, otherwise you might not get any logs
- `LOGGING_FORMAT` - The format of the logs. Those weird variables are the date, file location, and message.
- `LOGGING_DATE_FORMAT` - The format of the date in the logs.
- `LOGGING_FILENAME` - The filename of the logs. This is automatically generated based on the date.
- `LOGGING_ENCODING` - The encoding of the logs. This should always be utf-8.

- `DATABASE_PATH` - The path to the database. This is automatically generated based on the project's directory.

### Database

- `DATABASE_PATH` - The path to the database. This is automatically generated based on the project's directory.

### Sound Files

- `SOUNDFILES_PATH` - The path to the sound files. This is automatically generated based on the project's directory.

### Backups

- `BACKUPS_PATH` - The path to the backups. This is automatically generated based on the project's directory.
- `DATABASE_BACKUP_PATH` - The path to the database backups. This is automatically generated based on the project's directory.
- `LOGS_BACKUP_PATH` - The path to the logs backups. This is automatically generated based on the project's directory.

## songparser.py

Responsible for parsing the song files and extracting their metadata.

### Overview

We are using an abstract class `SongFile` which should be extended by child classes for each file type. For example:

```python
# This is what the parent class looks like
class SongFile(ABC): # ABC means it's an abstract class
    @abstractmethod
    def get_song_table_data(self):
        pass

# This is the class we want to make
class SongFileFLAC(SongFile): # inherit from SongFile

    def get_song_table_data(self): # this is an abstract method, so we have to implement it
        super().get_song_table_data() # call the parent method (named the exact same as current function)
        pass

class SongFileMP3(SongFile): # inherit from SongFile

    def get_song_table_data(self): # this is an abstract method, so we have to implement it
        super().get_song_table_data() # call the parent method (named the exact same as current function)
        pass
```

If you are adding support for a new file, there's some very important things you have to be aware of:

1. Firstly, you need to create a child class of `SongFile` for your file type. Look at the above example for more information.

2. Add your filetype to the `__init__()` function of the SongMetadata class.

```python

    # This is what the init function will look like (maybe a little different since this was written but it will be same gist)

    def __init__(self, filepath):
        """Initialize the SongMetadata object.
            We want to see what file type it is, and load the correct file."""
        self.extension = os.path.splitext(filepath)[1]
        self.songfile = None
        if self.extension == ".flac":
            self.songfile = SongFileFLAC(filepath)
        # Add your file type here! For example, for mp3:
        elif self.extension == ".mp3":
            self.songfile = SongFileMP3(filepath) # change this to the class you made
        else:
            logging.error("File type not supported: " + self.extension)

```

3. Add the required methods. These are the following
   - `get_song_table_data(self)`
   - `get_album_artist_data(self)`
   - `get_song_artist_data(self)`
   - `get_composer_data(self)`
   - `get_genre_data(self)`

Here's the actual hard part, you have to **return certain types of data for each of these methods**

#### get_song_table_data(self)

This one has the most information. Here's the list of stuff you have to return

```python
"filepath": None, # string
"main_artist": None, # string
"filesize": None, # int in bytes
"padding": None, # int in bytes
"album_artwork_bit_depth": None, # int in bits
"album_artwork_colors": None, # int
"album_artwork_height": None, # int in pixels
"album_artwork_width": None, # int in pixels
"bit_depth": None, # int in bits
"bitrate": None, # int in bits, divide by 1000 to get Kbps
"channels": None, # int
"duration": None, # int in seconds
"sample_rate": None, # int in KHz
"album": None, # string
"barcode": None, # string
"date_created": None, # string in YYYY-MM-DD
"disc_number": None, # int
"disc_total": None, # int
"genre": None, # string
"isrc": None, # string
"itunesadvisory": None, # string
"length": None, # int
"publisher": None, # string
"rating": None, # int
"title": None, # string
"track_number": None, # int
"track_total": None, # int
"source": None, # string
"favorited": False, # bool
```

It HAS to be a dict with all these keys, if you don't have the value for one, set it to `None`.

#### get_album_artist_data(self)

This one is a little easier. Just return a list of the album artists

```python
["artist1", "artist2", "artist3"]
```

#### get_song_artist_data(self)

Same thing as above, but for song artists

```python
["artist1", "artist2", "artist3"]
```

#### get_composer_data(self)

Same thing as above, but for composers

```python
["artist1", "artist2", "artist3"]
```

#### get_genre_data(self)

Same thing as above, but for genres

```python
["genre1", "genre2", "genre3"]
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
    * SYNC soundfiles (the actual sound data)
    * SYNC Analyticsdb (there will be an exac copy on the user's end, we want to add their data to our table and delete theirs)
12. Add the API
13. Add AUTH to the API
14. Fix the logs, add option to hold X amount of logs or delete logs older than X days or something so they dont get a gazillion bytes big
15. Overall add a ton of useful database queries.
16. Implement "spotify wrapped" and other cool animated graphics with the data we have! (this will be very late down the line, but think about it still)
17. Implement the [linux-server.io S6 overlay for the docker container](https://github.com/just-containers/s6-overlay).
18. Add the docker container
19. Add automatic image building in circle-ci