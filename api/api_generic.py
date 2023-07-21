import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import openai

openai.api_key = os.getenv("OPENAI_APIKEY")
PROMPT_PATH = "api/generic/description_prompt.txt"

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
    while draw.textsize(text, font)[0] < zone_width and draw.textsize(text, font)[1] < zone_height:
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)

    # Return the previous font size, which fits the text within the zone
    return font_size - 1

def place_text_on_image(image_path, top_left, bottom_right, text, font_path):
    """
    Place text on an image within the specified zone defined by the top-left and bottom-right coordinates.

    Parameters:
        image_path (str): The path to the image on which the text will be placed.
        top_left (tuple): A tuple containing the (x, y) coordinates of the top-left corner of the zone.
        bottom_right (tuple): A tuple containing the (x, y) coordinates of the bottom-right corner of the zone.
        text (str): The text to be placed on the image.
        font_path (str): The path to the TrueType font file (e.g., ".ttf") to be used.

    Returns:
        PIL.Image.Image: The resulting image with the text placed within the specified zone.
    """
    # Open the image
    img = Image.open(image_path)
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
    return draw.text((x_centered, y_centered), text, fill="black", font=font)


def generate_image(event_name, lab, description, date, hour, location):
    """
    Generate an image for an instagram post based on a template
    :param event_name: Title of the event
    :param lab: Name of the lab doing the event
    :param description: Description of the event
    :param date: Date of the event
    :param hour: Hour of the event
    :param location: Location of the event
    :return: image with all this information.
    """
    # Create the title and description for the Instagram post
    title = f"{event_name}"
    lines = textwrap.wrap(description, width=30)
    description = "\n".join(lines)

    # Generate the image with the post content -- NEED UPDATE
    image_path = os.path.join("assets", f"{lab}.png")
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    title_font = ImageFont.truetype("ressources/fonts/LeagueSpartan-Bold.ttf", 50)
    desc_font = ImageFont.truetype("ressources/fonts/LeagueSpartan-Bold.ttf", 40)

    #Place text on image with the following command :
    #place_text_on_image(image_path, top_left, bottom_right, text, font_path)


    # Save the generated image
    post_image_path = "output/generated_post.png"
    img.save(post_image_path)
    print("Instagram post generated!")

    # Display the image
    img.show()


if __name__ == '__main__':
    pass
