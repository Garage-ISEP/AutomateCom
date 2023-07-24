import os
from api import *
import logging
import inquirer
from halo import Halo

from api import api_generic



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Colors:
    """

    This class is an Enum that keep all the colors to use in our CLI interface.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CLI:
    def __init__(self):
        """halo_ = Halo(text="Bonjour et bienvenue :")
        halo_.start()"""
        self.options()

    def options(self):
        options = [
                inquirer.List('options',
                        message="Options",
                        choices=['Générer Crea WS',
                                'Quitter'],
                        carousel=True,)
        ]
        answer = inquirer.prompt(options)['options']
        if answer == "Générer Crea WS":
            self.generate_workshop()
        elif answer == 'Quitter':
            exit(0)

    def generate_workshop(self):
        info = ["event_name", "lab", "description", "date", "hour", "location"]
        for e in info:
            question = input(f"{e} ? :")
            info[info.index(e)] = question
        img = api_generic.generate_image(info)
        img.show()
        self.options()

if __name__ == '__main__':
    try:
        cli = CLI()
    except KeyboardInterrupt:
        print("\n" + Colors.WARNING + "Arrêt du programme..." + Colors.ENDC)
        sys.exit(0)