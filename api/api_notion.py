import requests
import json
import os

NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

HEADERS = {
    'Authorization': 'Bearer ' + NOTION_TOKEN,
    'Content-Type': 'application/json',
    'Notion-Version': '2021-05-13'
}


def update_line(line_id, properties):
    """
    Function to update a line in a Notion database
    :param line_id:
    :param properties:
    :return:
    """

    data = {
        'properties': properties
    }

    response = requests.patch(f'https://api.notion.com/v1/pages/{line_id}', headers=HEADERS, json=data)

    if response.status_code == 200:
        print('Line updated successfully.')
    else:
        print('Failed to update line. Error:', response.json())


def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=HEADERS)

    data = response.json()

    # Comment this out to dump all data to a file
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=HEADERS)
        data = response.json()
        results.extend(data["results"])

    return results


if __name__ == '__main__':
    pass
