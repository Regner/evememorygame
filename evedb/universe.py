

from evedb.db import connect

def get_all_regions_basic():
    """ Gets all region IDs and their name. """
    
    with connect() as db:
        regions = db.execute('''
            SELECT regionID, regionName
              FROM mapRegions
        ''')
    
    regions = [x for x in regions]
    
    return regions


def get_all_non_wh_regions():
    """ Gets all region IDs and their name minus WH regions. """
    
    with connect() as db:
        regions = db.execute('''
            SELECT regionID, regionName
              FROM mapRegions
             WHERE regionID < 11000000
        ''')
    
    regions = [x for x in regions]
    
    return regions
    
    
def get_bordering_regions(region_id):
    """ Gets all the regions bordering a given region. """
    
    with connect() as db:
        regions = db.execute('''
            SELECT toRegionID, regionName
              FROM mapRegionJumps
             INNER JOIN mapRegions ON mapRegionJumps.toRegionID = mapRegions.regionID
             WHERE fromRegionID = {}
        '''.format(region_id)).fetchall()
    
    regions = [x for x in regions]
    
    return regions