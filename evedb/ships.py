

from evedb.db import connect

def get_all_published_ships_basic():
    """ Gets all region IDs and their name. """
    
    with connect() as db:
        ships = db.execute('''
            SELECT typeID, typeName, invGroups.groupID, invGroups.groupName, invCategories.categoryID, invCategories.categoryName
              FROM invTypes
             INNER JOIN invGroups ON invTypes.groupID = invGroups.groupID
             INNER JOIN invCategories ON invGroups.categoryID = invCategories.categoryID
             WHERE invCategories.categoryID = 6
               AND invTypes.published = 1
        ''')
    
    ships = [x for x in ships]
    
    return ships