import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import json

import openai

openai.api_key = os.getenv("OPENAI_APIKEY")
PROMPT_PATH = "api/generic/description_prompt.txt"

ASSETS = "ressources/assets"
OUTPUT_DIR = "output"

DATA_JSON = os.path.join(ASSETS, "img_data.json")
POST_WS_DIR = os.path.join(ASSETS, "post_workshop")
FONTS_DIR = os.path.join(ASSETS, "fonts")

LABS_COLORS = {
    "Coder": "#dc251f",
    "Blockchain": "#ffbf29",
    "Cyber": "#fe831e",
    "IA": "#11ad8b",
    "Maker": "#11a1dc",
    "Virtual": "#1e3dae",
}

FONT_OFFSET = 5

def generate_text(title, prompt_path=PROMPT_PATH):
    """
    Generate a description for an event post using OpenAI API.

    :param prompt_path: Path to the selected prompt
    :param title: Title of the event for the prompt
    :return: Generated description of the event.
    """
    prompt = str(open(prompt_path, "r")) + title
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000, n=1, stop=None,
                                        temperature=0.5)
    generated_text = response.choices[0].text.strip()
    return generated_text


def get_optimal_font_size(text, font_path, zone_width, zone_height):
    """
    Estimate the optimal font size that fits the given text within the specified zone.

    Parameters:
        text (str): The text to be placed on the image.
        font_path (str): The path to the TrueType font file (e.g., ".ttf") to be used.
        zone_width (int): The width of the zone where the text will be placed.
        zone_height (int): The height of the zone where the text will be placed.

    Returns:
        int: The calculated optimal font size that fits the text within the zone.
    """
    img = Image.new("RGB", (1000, 1000), color="white")  # Create a temporary image to estimate the font size
    draw = ImageDraw.Draw(img)
    font_size = 1

    # Load the font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        raise Exception("Font not found or unable to load the font. Please provide a valid font path.")

    # Estimate the optimal font size by increasing it until the text fits within the zone
    while True:
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] < zone_width and bbox[3] < zone_height:
            font_size += 1
            font = ImageFont.truetype(font_path, font_size)
        else:
            break

    # Return the previous font size, which fits the text within the zone
    return font_size - 1


def place_text_on_image(img, top_left, bottom_right, text, font_path, COLOR, align):
    """
    Place text on an image within the specified zone defined by the top-left and bottom-right coordinates.

    Parameters:
        :param img: The image on which the text will be placed.
        :param top_left: A tuple containing the (x, y) coordinates of the top-left corner of the zone.
        :param bottom_right: A tuple containing the (x, y) coordinates of the bottom-right corner of the zone.
        :param text: The text to be placed on the image.
        :param font_path: The path to the TrueType font file (e.g., ".ttf") to be used.
        :param COLOR: The color of the text that will be placed.
        :param align: The way the text is going to be aligned.
    Returns:
        None. The text is placed directly on the provided image.
    """
    draw = ImageDraw.Draw(img)
    # Get the coordinates of the zone
    x1, y1 = top_left
    x2, y2 = bottom_right
    zone_width = x2 - x1
    zone_height = y2 - y1

    # Calculate the optimal font size to fit the text within the zone
    font_size = get_optimal_font_size(text, font_path, zone_width, zone_height) - FONT_OFFSET

    # Load the font with the calculated size
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the position to center the text in the zone
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]

    #x_centered = x1 + (zone_width - text_width) // 2
    if align == "left":
        x_centered = x1
    elif align == "right":
        x_centered = x1 + zone_width - text_width
    else:  # default to center
        x_centered = x1 + (zone_width - text_width) // 2

    # Calculate vertical center of the zone
    zone_center_y = y1 + zone_height // 2

    # Adjust y_position so that text is centered vertically
    y_centered = zone_center_y - text_height // 2
    #y_centered = y1 + (zone_height - text_height) // 2

    # Place the text on the image
    draw.text((x_centered, y_centered), text, fill=COLOR, font=font)


def generate_image(info: dict) -> str:
    """
    Generate an image with a template and the informations about the image.
    :param info: Dict that contains the informations for the image.
    :return: String of link to the generated image.
    :rtype: str
    """
    with open(DATA_JSON, 'r', encoding='utf-8') as json_file:
        data = dict(json.load(json_file))
        json_file.close()

    tag = info["tag"]
    data = data[tag]

    image_input = Image.open(os.path.join(ASSETS, f"{tag}/{info['lab']}.png"))

    for coord in list(data.keys()):
        if data[coord] == "ignore":
            continue
        else:
            #print(f"info coord 4 = {data[coord][4]}")
            place_text_on_image(image_input, tuple(data[coord][0]), tuple(data[coord][1]), info[coord],
                                f"{FONTS_DIR}/{data[coord][2]}", LABS_COLORS[f"{info['lab']}"], data[coord][4])

    image_output = os.path.join(OUTPUT_DIR, f"{tag}_{info['date'].replace(' ', '_')}.png")
    try:
        image_input.save(image_output)
    except FileNotFoundError:
        print("Dossier ou fichier introuvable.")

    print("Post generated!")
    #return image_output


if __name__ == '__main__':
    info = {
        'lab': 'Coder',
        'title': 'Coder une blockchain en Python',
        'date': '13 MAR',
        'hour': '18H',
        'location': 'NDC',
        'tag': 'post_workshop'
    }

    generate_image(info)
    # lab, title, date, hour, location, tag
    infos2 = [
        "Coder",
        'Coder une blockchain en Python',
        '12 MAR',
        '18H',
        'NDC',
        'post_workshop'
    ]
    # generate_image(infos2)
