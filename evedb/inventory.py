

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


def get_dogma_attribute_for_type(type_id, dogma_attribute_id):
    with connect() as db:
        effect = db.execute('''
            SELECT COALESCE(dgmTypeAttributes.valueInt, dgmTypeAttributes.valueFloat)
              FROM invTypes
              LEFT JOIN dgmTypeAttributes ON invTypes.typeID = dgmTypeAttributes.typeID
             WHERE invTypes.typeID = {}
               AND dgmTypeAttributes.attributeID = {}
        '''.format(type_id, dogma_attribute_id)).fetchone()[0]
    
    return effect