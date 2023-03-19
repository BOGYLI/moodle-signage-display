import MoodleWebService
from datetime import datetime 
class PresentationParser:
    def __init__(self, moodlewebservice) -> None:
        self.mws = moodlewebservice
    
    def filter_active_db_entries(self, dbentries) -> list:
        approved = list()
        for entry in dbentries:
            if entry["approved"] == True:
                approved.append(entry)
        return approved
    
    def build_slide_from_db_entry(self, dbentry, fields) -> dict:
        slide = dict()
        for content in dbentry["contents"]:
            if content["fieldid"] == fields["Slide"]: slide["html"] = content["content"]
            if "@PLUGINFILE@" in slide["html"]:
                for f in content["files"]:
                    self.mws.download_file(f["filename"], f["fileurl"])
                slide["html"] = slide["html"].replace("@@PLUGINFILE@@", "media")
            if content["fieldid"] == fields["Anzeige Start"]: slide["start"] = content["content"]
            if content["fieldid"] == fields["Anzeige Ende"]: slide["end"] = content["content"]
            if content["fieldid"] == fields["Anzeigedauer"]: slide["duration"] = content["content"]
            if content["fieldid"] == fields["Priorität"]: slide["priority"] = content["content"]
            if content["fieldid"] == fields["Hintergrund"]:
                fname = content["content"]
                for f in content["files"]:
                    if f["filename"] == fname: 
                        slide["background"] = self.mws.download_file(f["filename"], f["fileurl"])
        return slide
    
    def collect_presentation_slides(self, dbentries, fields) -> list:
        entries = self.filter_active_db_entries(dbentries)
        slides = list()
        for entry in entries:
            slide = self.build_slide_from_db_entry(entry, fields)
            now = datetime.now().timestamp()
            if int(slide["start"]) < now and int(slide["end"]) > now:
                slides.append(slide)
        return slides
    
    def build_slides_html(self, slides) -> str:
        html = ""
        prio = False
        for slide in slides:
            if slide["priority"] == "ja":
                prio = True
            if prio == True and slide["priority"] == "nein":
                continue
            
            html += "<section"
            if "background" in slide.keys() and slide["background"]:
                if any(suffix in slide["background"] for suffix in ["mp4", "mov"]):
                    html += " data-background-video=\""+slide["background"]+"\" data-background-size=contain data-background-video-loop"
                else:
                    html += " data-background=\""+slide["background"]+"\""
            if "duration" in slide.keys() and slide["duration"] != None:
                html += " data-autoslide=\""+str(int(slide["duration"])*1000)+"\""
            
            html += ">"
            html += slide["html"]
            html += "</section>"
        
        return html