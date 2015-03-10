

import json

from flask.ext.restful import Resource, reqparse, abort, url_for

from emgquestiongenerator.questions import QuestionUniverse, QuestionShip, random_question_class


class QuestionsCollection(Resource):
    """ Resource for listing all the different question resources. """
    
    def get(self):
        questions = {
            'categories' : {
                'random' : {
                    'href' : url_for('question_random_category',   _external=True),
                    'name' : 'Random',
                },
                'universe' : {
                    'href'           : url_for('question_universe_category', _external=True),
                    'name'           : 'Universe',
                    'sub_categories' : {
                        'bordering_region' : {
                            'href' : url_for('question_universe_bordering_region_category', _external=True),
                            'name' : 'Bordering Regions',
                        },
                        'poitot' : {
                            'href' : url_for('question_universe_poitot_category', _external=True),
                            'name' : 'Poitot',
                        },
                    },
                },
                'ships' : {
                    'href' : url_for('question_ships_category',    _external=True),
                    'name' : 'Ships',
                    'sub_categories' : {
                        'class_id' : {
                            'href' : url_for('question_ships_class_id_category', _external=True),
                            'name' : 'Class Identification',
                        },
                        'image_id' : {
                            'href' : url_for('question_ships_image_id_category', _external=True),
                            'name' : 'Image Identification',
                        },
                        'slots' : {
                            'href' : url_for('question_ships_slots_category', _external=True),
                            'name' : 'Slots',
                        },
                        'traits' : {
                            'href' : url_for('question_ships_traits_category', _external=True),
                            'name' : 'Traits',
                        },
                    },
                },
            }
        }
        
        return questions


class QuestionRandomCategory(Resource):
    """ Resource for getting a question from a random category. """
    
    def get(self):
        random_class = random_question_class()
        question     = random_class.get_random_question()
        
        result = question()
        result['category'] = random_class.__class__.__name__.lower()
        
        return result


class QuestionUniverseCategory(Resource):
    """ Resource for getting a question from the universe category. """
    
    def get(self):
        universe = QuestionUniverse()
        question = universe.get_random_question()
        
        result = question()
        result['category'] = universe.__class__.__name__.lower()
        
        return result


class QuestionUniverseBorderingRegionCategory(Resource):
    """ Resource for getting a question about what region borders a given region. """
    
    def get(self):
        universe = QuestionUniverse()
        
        result = universe.region_boardering_region()
        result['category'] = universe.__class__.__name__.lower()
        
        return result


class QuestionUniversePoitotCategory(Resource):
    """ Resource for getting a question about Poitot. """
    
    def get(self):
        universe = QuestionUniverse()
        
        result = universe.region_with_poitot()
        result['category'] = universe.__class__.__name__.lower()
        
        return result


class QuestionShipsCategory(Resource):
    """ Resource for getting a question from the universe category. """
    
    def get(self):
        ships    = QuestionShip()
        question = ships.get_random_question()
        
        result = question()
        result['category'] = ships.__class__.__name__.lower()
        
        return result


class QuestionShipsClassCategory(Resource):
    """ Resource for getting a question about what class a ship is. """
    
    def get(self):
        ships = QuestionShip()
        
        result = ships.ship_class()
        result['category'] = ships.__class__.__name__.lower()
        
        return result


class QuestionShipsIdentificationCategory(Resource):
    """ Resource for getting a question about identifying a ship from an image. """
    
    def get(self):
        ships = QuestionShip()
        
        result = ships.select_ship_from_image()
        result['category'] = ships.__class__.__name__.lower()
        
        return result


class QuestionShipsSlotsCategory(Resource):
    """ Resource for getting a question about the number of slots a ship has. """
    
    def get(self):
        ships = QuestionShip()
        
        result = ships.number_of_slots()
        result['category'] = ships.__class__.__name__.lower()
        
        return result


class QuestionShipsTraitsCategory(Resource):
    """  """
    
    def get(self):
        ships = QuestionShip()
        
        result = ships.ship_trait()
        result['category'] = ships.__class__.__name__.lower()
        
        return result


class Test(Resource):
    """ TESTING """
    
    def get(self):
        return {}
    

def register_apis(api):
    """ Registers the API resources defined in this file with the app in it's application factory. """
    
    api.add_resource(Test,                                    '/test/')
    api.add_resource(QuestionsCollection,                     '/questions/')
    api.add_resource(QuestionRandomCategory,                  '/questions/random/',                    endpoint='question_random_category')
    api.add_resource(QuestionUniverseCategory,                '/questions/universe/',                  endpoint='question_universe_category')
    api.add_resource(QuestionUniverseBorderingRegionCategory, '/questions/universe/bordering_region/', endpoint='question_universe_bordering_region_category')
    api.add_resource(QuestionUniversePoitotCategory,          '/questions/universe/poitot/',           endpoint='question_universe_poitot_category')
    api.add_resource(QuestionShipsCategory,                   '/questions/ships/',                     endpoint='question_ships_category')
    api.add_resource(QuestionShipsClassCategory,              '/questions/ships/class_id/',            endpoint='question_ships_class_id_category')
    api.add_resource(QuestionShipsIdentificationCategory,     '/questions/ships/image_id/',            endpoint='question_ships_image_id_category')
    api.add_resource(QuestionShipsSlotsCategory,              '/questions/ships/slots/',               endpoint='question_ships_slots_category')
    api.add_resource(QuestionShipsTraitsCategory,             '/questions/ships/traits/',              endpoint='question_ships_traits_category')
    