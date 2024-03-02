import requests
import json

confluence_base_url = 'https://unihack-lecture.atlassian.net/wiki'
apiToken = 'ATATT3xFfGF0sVeg6ZJQhIpvmllwTYzixrKqv4W7rPEPRUR2mRqsNSBDjbyMWsLuqw-R53kuKqCo_eBFcFmcqFxSh9m0RwvmKgbZWEQhBefUk1wxM3vBOD08T6NklRAhka5tf_kyu3u5mDIoTtEbZvEvT9B4ZPvDS-ylJDUVtq8a3pJ4MNfO8qw=9024E2C2'
email = 'hyzhou@student.unimelb.edu.au'

auth = (email, apiToken)
headers = {
    'Content-Type': 'application/json'
}




def uploadTranscript(title, new_content):
    # Add check to see if the page exists
    check_url = f'{confluence_base_url}/rest/api/content?title={title}&spaceKey=TEAM&expand=version'
    check_response = requests.get(check_url, headers=headers, auth=auth)
    page_exists = False
    if check_response.json()['size'] > 0 and len(check_response.json()['results']) > 0:
        check_data = check_response.json()['results'][0]
        page_exists = True

    if page_exists:
        # Update the data, increase version number
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
        # Simply create data without version number
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


