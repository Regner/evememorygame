

from evedb.db import connect

def get_all_published_groups_in_category(category_id):
    """ Gets all the published groups for a given category ID. """
    
    with connect() as db:
        groups = db.execute('''
            SELECT groupID, groupName
              FROM invGroups
             WHERE categoryID = {}
               AND published = 1
        '''.format(category_id))
    
    groups = [x for x in groups]
    
    return groups