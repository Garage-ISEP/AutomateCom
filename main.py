import os
import sys

from api import *
import logging
import inquirer
from halo import Halo
from typing import Union
import json
from api import api_generic

EVENT_POSTS_TYPES = {
    "type": ["post", "story", "description"],

    "post": ["workshop", "generated_image"],
    "story": ["classic", "reminder", "citation", "poll", "quiz", "question"],

    "lab": ['General', 'IA', 'Cyber', 'Coder', 'Virtual', 'Blockchain', 'Maker'],

    "info": ["event_name", "description", "date", "hour", "location"],

    "difficulty": ["Débutant", "Intermédiaire", "Confirmé"]
}

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
        self.start()

    def start(self):
        self.menu(
            title="Menu d'accueil",
            message="Choissisez une option dans le menu d'accueil",
            opt={
                "Générer Créa": self.event,
                "Setup": self.setup,
                "Quitter": self.close
            }
        )()

    def setup(self):
        self.menu(
            title="setup",
            message="Mettez à jour les identifiants",
            opt={
                "Post": self.post,
                "Story": self.story,
                "Description": self.description,
            }
        )()

    def update_value(self, variable):
        value = input(f"Update value {variable}: ")
        os.environ[f"{variable}"] = value

    def menu(self, title: str, message: str, opt: dict) -> Union[classmethod, str]:
        """
        Crée un menu carousel avec différentes options.

        :param title: Titre du menu (pas affiché)
        :param message: Description du message (affiché)
        :param opt: Dictionnaire d'options (clé: Message affiché, valeur: Appel de la fonction)
        :rtype: Valeur de l'objet sélectionné parmi opt
        """
        options = [
            inquirer.List(title,
                          message=message,
                          choices=list(opt.keys()),
                          carousel=True, )
        ]
        answer = inquirer.prompt(options)[title]
        return opt.get(answer, lambda: "Indisponible")

    def event(self):
        self.menu(
            title="type",
            message="Choissisez un type de créa",
            opt={
                "Post": self.post,
                "Story": self.story,
                "Description": self.description,
            }
        )()

    def post(self):
        self.menu(
            title="type",
            message="Choissisez un type de post",
            opt={
                "Workshop": self.workshop
            }
        )(tag="post")

    def workshop(self, tag: str):
        infos = [
            inquirer.List("lab",
                          message="Selection lab",
                          choices=EVENT_POSTS_TYPES["lab"],
                          carousel=True, ),
            inquirer.Text("title",
                          message="Nom de l'évènement"),
            inquirer.Text("date",
                          message="Date au complet (Exemple: MERCREDI 12 NOVEMBRE) :"),
            inquirer.Text("hour_location",
                          message="Heure et lieu (Exemple : 18H, L012)"),
            inquirer.List("difficulty",
                          message="Difficulté du Workshop",
                          choices=EVENT_POSTS_TYPES["difficulty"],
                          carousel=True, ),
            inquirer.Text("keywords",
                          message="(Optionel) 3 mots-clés pour le WS, séparés d'une virgule:"
            )
        ]
        infos = inquirer.prompt(infos)
        keywords = infos["keywords"].split(",")
        print(keywords)
        if len(keywords):
            for keyword in keywords:
                infos[f"keyword{keywords.index(keyword)+1}"] = keyword
        infos.pop("keywords")
        for key in infos:
            if key is not ("lab" or "tag"):
                infos[key] = infos[key].upper()
        #infos["lab"] = infos["lab"].lower()
        infos["tag"] = f"{tag}_workshop".lower()
        print(infos)
        print(list(infos.values())[:-1])
        # img = api_generic.generate_image(list(infos.values()))
        img = api_generic.generate_image(infos)
        # img.show()
        self.start()

    def story(self):
        self.menu(
            title="type",
            message="Choissisez un type de post",
            opt={
                "Workshop": self.workshop,
                "Classic": self.story_classic,
                # "reminder":,
                # "citation":,
                # "poll/quiz/question":,
            }
        )(tag="story")

    def story_classic(self, tag):
        infos = [
            inquirer.List("lab",
                          message="Selection lab",
                          choices=EVENT_POSTS_TYPES["lab"],
                          carousel=True, ),
            inquirer.Text("title",
                          message="Nom de l'évènement"),
            inquirer.Text("text",
                          message="Texte"),
            inquirer.Text("date",
                          message="Date (RESPECTEZ LE FORMAT *JJ MMM*, ex: 12 MAR)"),
        ]
        infos = inquirer.prompt(infos)
        infos["tag"] = f"{tag}_classic"
        print(infos)
        print(list(infos.values())[:-1])
        api_generic.generate_image(infos)

    def description(self):
        infos = [
            inquirer.Text("description",
                          message="Donnez simplement un titre pour une description")
        ]
        description = api_generic.generate_text(inquirer.prompt(infos)["description"])
        print(description)

    def close(self):
        exit(0)


if __name__ == '__main__':
    try:
        cli = CLI()
    except KeyboardInterrupt:
        print("\n" + Colors.WARNING + "Arrêt du programme..." + Colors.ENDC)
        sys.exit(0)
