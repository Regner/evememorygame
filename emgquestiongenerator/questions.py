

from random import choice, sample, shuffle

from evedb.ships     import get_all_published_ships_basic
from evedb.universe  import get_bordering_regions, get_all_non_wh_regions
from evedb.inventory import get_all_published_groups_in_category


class Question(object):
    """ Base class for creating different question categories.
    
    Each class should be based around a specific category of questions.
    
    Answeres returned must conform to the following format:
    {
        "answer": 0,  # Value of the correct answer.
        "choices": [  # List of possible answers including the correct one.
        [
            2,  # Value for the choice.
            "A fictional space detective."  # Display text for the choice.
        ],
        "question": "Poitot is famous for being...?"  # Display text for the question.
    }
    
    """
    
    def __init__(self, num_answers=3):
        
        # We subtract 1 because we will always add the answer as well.
        self.num_answers       = num_answers - 1
        self.question_registry = []
    
    def get_random_question(self):
        return choice(self.question_registry)


class QuestionAmmo(Question):
    def __init__(self, num_answers=3):
        super(QuestionAmmo, self).__init__(num_answers)
        
        self.question_registry = [
        ]
        

class QuestionShip(Question):
    def __init__(self, num_answers=3):
        super(QuestionShip, self).__init__(num_answers)
        
        self.question_registry = [
            self.ship_class,
        ]
    
    
    def ship_class(self):
        """ Asks what class a specific ship is. """
        
        ships         = get_all_published_ships_basic()
        selected_ship = choice(ships)
        
        ships_category      = 6
        all_groups          = get_all_published_groups_in_category(ships_category)
        selected_ship_group = (selected_ship[2], selected_ship[3])
        
        groups_to_choose_from = list(set(all_groups) - set(selected_ship_group))
        
        choices = sample(groups_to_choose_from, self.num_answers)
        choices.append(selected_ship_group)
        shuffle(choices)
        
        return {
            'question' : 'Which of the following categories does the {} belong to?'.format(selected_ship[1]),
            'choices'  : choices,
            'answer'   : selected_ship[2],
        }
        


class QuestionUniverse(Question):
    def __init__(self, num_answers=3):
        super(QuestionUniverse, self).__init__(num_answers)
        
        self.question_registry = [
            self.region_boardering_region,
            self.region_with_poitot,
        ]
    
    def region_boardering_region(self):
        """ Picks a random region and asks which the possible answers boarders it.
        
        This excludes WH regions.
        """
        
        all_regions       = get_all_non_wh_regions()
        random_region     = choice(all_regions)
        bordering_regions = get_bordering_regions(random_region[0])
        
        excluded_regions = bordering_regions
        excluded_regions.append(random_region)
        
        regions_to_choose_from = list(set(all_regions) - set(excluded_regions))
        
        choices = sample(regions_to_choose_from, self.num_answers)
        choices.append(random_region)
        shuffle(choices)
        
        return {
            'question' : 'Which of the following regions borders the {} region?'.format(random_region[1]),
            'choices'  : choices,
            'answer'   : random_region[0],
        }
        
    def region_with_poitot(self):
        """ Asks what Poitot is famous for being. """
        
        possible_choices = [
            (1, 'Kind to Animals.'),
            (2, 'A fictional space detective.'),
            (3, 'Adjacent to F67E-Q.'),
        ]
        
        choices = sample(possible_choices, self.num_answers)
        choices.append((0, 'The only named system in Syndicate.'))
        shuffle(choices)
        
        return {
            'question' : 'Poitot is famous for being...?',
            'choices'  : choices,
            'answer'   : 0,
        }


def random_question_class():
    """ Returns a random Question class. """
    
    return choice([
        QuestionShip,
        QuestionUniverse,
    ])