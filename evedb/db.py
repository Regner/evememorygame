

import sqlite3


def connect(db_file='eve.db'):
    """ Returns a connection cursor. """
    
    return sqlite3.connect(db_file)