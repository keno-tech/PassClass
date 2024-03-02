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
    data = {
        'type': 'page',
        'title': title,
        'space': {'key': 'TEAM'},
        'body': {
            'storage': {
                'value': new_content,
                'representation': 'storage',
            }
        }
    }
    
    create_url = f'{confluence_base_url}/rest/api/content/'
    response = requests.post(create_url, data=json.dumps(data), headers=headers, auth=auth)
    
    if response.status_code == 200:
        print("Page created successfully.")
        page_id = response.json()['id']
        print(f"Page URL: {confluence_base_url}/spaces/TEAM/pages/{page_id}")
    else:
        print("Failed to create page:", response.json())


