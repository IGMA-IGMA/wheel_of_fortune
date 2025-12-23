from .game import WOFGame, set_difficulty
from .file_handler import random_word_generator, save_records, update_record, entry_records, get_high_scores
from .decorators import timer, log_errors
from .utils import display_word

__all__ = ['WOFGame','random_word_generator','save_records','update_record',\
           'timer','log_errors','display_word', 'entry_records', 'set_difficulty', 'get_high_scores']
__version__ = "1.0.0"