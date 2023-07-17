import os
from linkedin import linkedin

linkedin_client_id = os.getenv()
linkedin_client_secret = os.getenv()
linkedin_access_token = os.getenv()

def post_on_linkedin(image_path, caption):
    """
    Post an image on LinkedIn with the LinkedIn credentials
    :param image_path: Path to the image
    :param caption: Caption of the post
    :return: None
    """
    authentication = linkedin.LinkedInDeveloperAuthentication(linkedin_client_id, linkedin_client_secret,
                                                              linkedin_access_token,
                                                              permissions=linkedin.PERMISSIONS.enums.values())
    app = linkedin.LinkedInApplication(authentication)

    # Upload the image
    # Add options for video post
    with open(image_path, "rb") as image:
        image_urn = app.upload_image(image)

    # Add exception handling (in case of errors)
    app.post_share(comment=caption, image_urn=image_urn)
    # Implement the LinkedIn posting code using the LinkedIn API

if __name__ == '__main__':
    pass