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
        
        response = requests.post(self.request_url, params=params)
        dbfields = response.json()["fields"]
        fields = dict()
        for field in dbfields:
            fields[field["name"]] = field["id"]
        return fields
    
    # Get the list of moodle database entries.
    def request_db_entries(self, dbid) -> list:
        params = {
            "wstoken": self.authtoken,
            "wsfunction": "mod_data_get_entries",
            "moodlewsrestformat": "json",
            "databaseid": dbid,
            "returncontents": 1
        }
        response = requests.post(self.request_url, params=params)
        return response.json()["entries"]
    
    # Download file form URL and save it in media folder.
    def download_file(self, filename, fileurl) -> str:
        r = requests.get(fileurl+"?token="+self.authtoken)
        with open("html/media/"+filename,'wb') as f:
            f.write(r.content)
        return "media/"+filename