import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import json
#import openai

#openai.api_key = os.getenv("OPENAI_APIKEY")
PROMPT_PATH = "api/generic/description_prompt.txt"

WS_DATA_JSON = "/workspaces/AutomateCom/ressources/assets/workshop_img_data.json"
WS_IMG_DIR = "/workspaces/AutomateCom/ressources/assets/workshop_img"
FONTS_DIR = "/workspaces/AutomateCom/ressources/assets/fonts"

def generate_text(title):
    """
    Generate a description for an event post using OpenAI API.

    :param title: Title of the event for the prompt
    :return: Generated description of the event.
    """
    prompt = str(open(PROMPT_PATH, "r")) + title
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
    while font.getsize(text)[0] < zone_width and font.getsize(text)[1] < zone_height:
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)

    # Return the previous font size, which fits the text within the zone
    return font_size - 1

def place_text_on_image(img, top_left, bottom_right, text, font_path, COLOR):
    """
    Place text on an image within the specified zone defined by the top-left and bottom-right coordinates.

    Parameters:
        img (PIL.Image.Image): The image on which the text will be placed.
        top_left (tuple): A tuple containing the (x, y) coordinates of the top-left corner of the zone.
        bottom_right (tuple): A tuple containing the (x, y) coordinates of the bottom-right corner of the zone.
        text (str): The text to be placed on the image.
        font_path (str): The path to the TrueType font file (e.g., ".ttf") to be used.

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
    font_size = get_optimal_font_size(text, font_path, zone_width, zone_height)

    # Load the font with the calculated size
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the position to center the text in the zone
    text_width, text_height = draw.textsize(text, font)
    x_centered = x1 + (zone_width - text_width) // 2
    y_centered = y1 + (zone_height - text_height) // 2

    # Place the text on the image
    draw.text((x_centered, y_centered), text, fill=COLOR, font=font)

def generate_image(info):
    # ... (other parts of your code)
    event_name, lab, description, date, hour, location = info

    # Generate the image with the post content
    image_path = os.path.join(WS_IMG_DIR, f"{lab}.png")
    img = Image.open(image_path)

    with open(WS_DATA_JSON, 'r', encoding='utf-8') as json_file:
        data = dict(json.load(json_file))
        json_file.close()

    text_coord = [tuple(xy) for xy in data["workshop_img"]["desc_zone_coordinates"]]
    time_coord = [tuple(xy) for xy in data["workshop_img"]["time_zone_coordinates"]]
    date_coord = [tuple(xy) for xy in data["workshop_img"]["date_zone_coordinates"]]

    print(text_coord,time_coord,date_coord)
    # Place the description text on the image
    place_text_on_image(img, text_coord[0], text_coord[1], description, f"{FONTS_DIR}/LeagueSpartan-Bold.ttf","black")
    place_text_on_image(img, time_coord[0], time_coord[1], hour, f"{FONTS_DIR}/LeagueSpartan-Bold.ttf","white")
    place_text_on_image(img, date_coord[0], date_coord[1], date, f"{FONTS_DIR}/LeagueSpartan-Bold.ttf","white")

    # Save the generated image
    post_image_path = "/workspaces/AutomateCom/output/generated_post.png"
    img.save(post_image_path)
    print("Instagram post generated!")

    # Display the image
    img.show()

# ... (other parts of your code)

if __name__ == '__main__':
    info = ["Programmation", "Coder", "description un peu longue pour voir le resize", "19/07", "21H", "NDC"]
    generate_image(info)