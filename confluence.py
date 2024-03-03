import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

apiToken = os.getenv('apiToken')
email = os.getenv('email')
confluence_base_url = 'https://unihack-lecture.atlassian.net/wiki'

auth = (email, apiToken)
headers = {
    'Content-Type': 'application/json'
}


def uploadTranscript(title, new_content):
    check_url = f'{confluence_base_url}/rest/api/content?title={title}&spaceKey=TEAM&expand=version'
    check_response = requests.get(check_url, headers=headers, auth=auth)
    page_exists = False
    if check_response.json()['size'] > 0 and len(check_response.json()['results']) > 0:
        check_data = check_response.json()['results'][0]
        page_exists = True

    if page_exists:
        page_id = check_data['id']
        current_version = check_data['version']['number']
        new_url = f'{confluence_base_url}/rest/api/content/{page_id}'
        data = {
            'type': 'page',
            'title': title,
            'space': {'key': 'TEAM'},
            'body': {
                'storage': {
                    'value': new_content,
                    'representation': 'storage',
                }
            },
            'version': {'number': current_version + 1}
        }
        response = requests.put(new_url, data=json.dumps(data), headers=headers, auth=auth)
    else:
        data = {
            'type': 'page',
            'title': title,
            'space': {'key': 'TEAM'},
            'body': {
                'storage': {
                    'value': new_content,
                    'representation': 'storage',
                }
            },
        }
        create_url = f'{confluence_base_url}/rest/api/content/'
        response = requests.post(create_url, data=json.dumps(data), headers=headers, auth=auth)
        page_id = response.json().get('id', 'N/A')
    
    if response.status_code == 200:
        print("Page created successfully.")
        page_id = response.json()['id']
        print(f"Page URL: {confluence_base_url}/spaces/TEAM/pages/{page_id}")
    elif response.status_code == 204:
        print("Page updated successfully")
    else:
        print("Failed to create page:", response.json())


