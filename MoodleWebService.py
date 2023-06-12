import requests

class MoodleWebService:
    def __init__(self, request_url, authtoken) -> None:
        self.request_url = request_url
        self.authtoken = authtoken
    
    # Get the fields of moodle database activity.
    def request_db_fields(self, dbid) -> dict:
        params = {
            "wstoken": self.authtoken,
            "wsfunction": "mod_data_get_fields",
            "moodlewsrestformat": "json",
            "databaseid": dbid
        }
        
        try:
            response = requests.post(self.request_url, params=params)
            response.raise_for_status()
            dbfields = response.json()["fields"]
            fields = dict()
            for field in dbfields:
                fields[field["name"]] = field["id"]
            return fields
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error")
            print(errh.args[0])
    
    # Get the list of moodle database entries.
    def request_db_entries(self, dbid) -> list:
        params = {
            "wstoken": self.authtoken,
            "wsfunction": "mod_data_get_entries",
            "moodlewsrestformat": "json",
            "databaseid": dbid,
            "returncontents": 1
        }
        try:
            response = requests.post(self.request_url, params=params)
            response.raise_for_status()
            return response.json()["entries"]
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error")
            print(errh.args[0])
    
    # Download file form URL and save it in media folder.
    def download_file(self, filename, fileurl) -> str:
        try:
            r = requests.get(fileurl+"?token="+self.authtoken)
            r.raise_for_status()
            with open("html/media/"+filename,'wb') as f:
                f.write(r.content)
            return "media/"+filename
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error")
            print(errh.args[0])