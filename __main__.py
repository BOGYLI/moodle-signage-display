import config
import threading
from MoodleWebService import MoodleWebService
from PresentationParser import PresentationParser
from bs4 import BeautifulSoup


def perform_presentation_update():
    threading.Timer(300, perform_presentation_update).start()
    
    # Get data from mebis/moodle webservice.
    mws = MoodleWebService(config.moodleurl+"/webservice/rest/server.php", config.wstoken)
    fields = mws.request_db_fields(config.databaseid)
    entries = mws.request_db_entries(config.databaseid)
    parser = PresentationParser(mws)
    slides = parser.collect_presentation_slides(entries, fields)
    slides_html = parser.build_slides_html(slides)

    with open("template.html", "r") as tf:
        soup = BeautifulSoup(tf, 'html.parser')
        
    slidesdiv = soup.find(attrs={"class": "slides"})
    slidesdiv.append(slides_html)

    with open("html/index.html", "w", encoding="utf-8") as pf:
        pf.write(soup.prettify(formatter=None))

# run the endless loop.
perform_presentation_update()
