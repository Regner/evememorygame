

import json

from flask.ext.restful import Resource, reqparse, abort, url_for

from emgquestiongenerator.questions import QuestionUniverse, QuestionShip, random_question_class


class QuestionsCollection(Resource):
    """ Resource for listing all the different question resources. """
    
    def get(self):
        questions = {
            'categories' : {
                'random'   : {'href' : url_for('question_random_category',   _external=True)},
                'universe' : {'href' : url_for('question_universe_category', _external=True)},
                'ships'    : {'href' : url_for('question_ships_category',    _external=True)},
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


class QuestionShipsCategory(Resource):
    """ Resource for getting a question from the universe category. """
    
    def get(self):
        ships    = QuestionShip()
        question = ships.get_random_question()
        
        result = question()
        result['category'] = ships.__class__.__name__.lower()
        
        return result


class Test(Resource):
    """ TESTING """
    
    def get(self):
        test = get_dogma_attribute_for_type(641, 12)
        print test
        return {}
    

def register_apis(api):
    """ Registers the API resources defined in this file with the app in it's application factory. """
    
    api.add_resource(Test,                     '/test/')
    api.add_resource(QuestionsCollection,      '/questions/')
    api.add_resource(QuestionRandomCategory,   '/questions/random/',   endpoint='question_random_category')
    api.add_resource(QuestionUniverseCategory, '/questions/universe/', endpoint='question_universe_category')
    api.add_resource(QuestionShipsCategory,    '/questions/ships/',    endpoint='question_ships_category')