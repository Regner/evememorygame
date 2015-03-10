

from random import choice, sample, shuffle

from evedb.ships     import get_all_published_ships_basic
from evedb.universe  import get_bordering_regions, get_all_non_wh_regions
from evedb.inventory import get_all_published_groups_in_category, get_dogma_attribute_for_type, get_all_traits, get_all_traits_for_type

from eve_utils.image_server import get_type_links


class Question(object):
    """ Base class for creating different question categories.
    
    Each class should be based around a specific category of questions.
    
    Answeres returned must contain the following information:
    {
        "answer": 0,  # Value of the correct answer.
        "choices": [  # List of possible answers including the correct one.
        [
            2,  # Value for the choice.
            "A fictional space detective."  # Display text for the choice.
        ],
        "question": "Poitot is famous for being...?"  # Display text for the question.
    }
    
    You may add other optional fields on top of that.
    
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
            self.select_ship_from_image,
            self.number_of_slots,
            self.ship_trait,
        ]
        
    
    def number_of_slots(self):
        """ Asks the user to select the correct number of hi/med/low slots. """
        
        ships         = get_all_published_ships_basic()
        selected_ship = choice(ships)
        
        # Questions are tuples of dogma attribute, text for question
        questions = [
            (12,  0, 9, 'How many high slots does the {} have?'.format(selected_ship[1])),
            (13,  0, 9, 'How many mid slots does the {} have?'.format(selected_ship[1])),
            (14,  0, 9, 'How many low slots does the {} have?'.format(selected_ship[1])),
            (101, 0, 9, 'How many launcher hardpoints does the {} have?'.format(selected_ship[1])),
            (102, 0, 9, 'How many turret hardpoints does the {} have?'.format(selected_ship[1])),
        ]
        
        question = choice(questions)
        
        answer = get_dogma_attribute_for_type(selected_ship[0], question[0])
    
        possible_answers = range(question[1], question[2])
        possible_answers = list(set(possible_answers) - set([answer]))
        
        choices = sample(possible_answers, self.num_answers)
        choices.append(answer)
        shuffle(choices)
        
        return {
            'question' : question[3],
            'choices'  : convert_choices_to_dict(choices),
            'answer'   : answer,
            'images'   : get_type_links(selected_ship[0]),
        }
    
    def select_ship_from_image(self):
        """ Asks user to select the correct ship name based on an image. """
        
        ships         = get_all_published_ships_basic()
        selected_ship = choice(ships)
        
        choices = sample(ships, self.num_answers)
        choices.append(selected_ship)
        
        choices = [(x[0], x[1]) for x in choices]
        shuffle(choices)
        
        return {
            'question' : 'What ship is pictured?',
            'choices'  : convert_choices_to_dict(choices),
            'answer'   : selected_ship[0],
            'images'   : get_type_links(selected_ship[0]),
        }
        
    
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
            'choices'  : convert_choices_to_dict(choices),
            'answer'   : selected_ship[2],
        }
    
    
    def ship_trait(self):
        """ Asks which of the traits a specific ship has. """
        
        def convert_trait(trait_tuple):
            return (trait_tuple[0], '{}{} {}'.format(trait_tuple[1], trait_tuple[2], trait_tuple[3]))
            
        
        ships = get_all_published_ships_basic()
        
        # There is totally a better way to do this... but no sleep and only a
        #few minutes at a time to do anything means I got this... yuck.
        while True:
            selected_ship = choice(ships)
            
            ship_traits = get_all_traits_for_type(selected_ship[0])
            
            if len(ship_traits) > 0:
                selected_trait = choice(ship_traits)
                break
        
        traits = get_all_traits()
        
        # Remove all the traits for the selected ship so we don't end up with
        # two traits from it in the choices
        traits_to_choose_from = list(set(traits) - set(ship_traits))
        
        choices = [convert_trait(x) for x in sample(traits_to_choose_from, self.num_answers)]
        choices.append(convert_trait(selected_trait))
        shuffle(choices)
        
        return {
            'question' : 'Which of the following traits does the {} have?'.format(selected_ship[1]),
            'choices'  : convert_choices_to_dict(choices),
            'answer'   : selected_ship[0],
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
        answer            = choice(bordering_regions)
        
        regions_to_choose_from = list(set(all_regions) - set(bordering_regions) - set(random_region))
        
        choices = sample(regions_to_choose_from, self.num_answers)
        choices.append(answer)
        shuffle(choices)
        
        return {
            'question' : 'Which of the following regions borders the {} region?'.format(random_region[1]),
            'choices'  : convert_choices_to_dict(choices),
            'answer'   : answer[0],
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
            'choices'  : convert_choices_to_dict(choices),
            'answer'   : 0,
        }


def convert_choices_to_dict(choices):
    new_choices = []
    
    for x in choices:
        if isinstance(x, int) or isinstance(x, float):
            x = (x, x)
        
        new_choices.append({
        'value' : x[0],
        'text'  : x[1],
    })
    
    return new_choices


def random_question_class():
    """ Returns a random Question class. """
    
    selected_class = choice([
        QuestionShip,
        QuestionUniverse,
    ])
    
    return selected_class()