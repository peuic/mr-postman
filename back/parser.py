import re
from bs4 import BeautifulSoup


def clean_text(text):
    return text.replace("\n","").replace("\t","").replace("\xa0"," ").replace("\r"," ").strip()

class Parser:
    def parse(self, html, tracking):
        parsed = BeautifulSoup(html, 'html.parser')

        package_info = {
            "tracking_code": tracking,
            "activity": self.get_package_activity(parsed)
        }

        return package_info

    
    def get_package_activity(self, data):
        activity = []
        table = data.find("table", class_="listEvent sro")
        table_lines = table.find_all("tr")

        for line in table_lines:
            tracking_date = ""
            tracking_city = ""
            date = re.compile(r"\d{2}/\d{2}/\d{2,4}\s*?\d{1,2}:\d{2}")
            line_data = line.find_all("td")
            tracking_date_raw = clean_text(line_data[0].text)
            tracking_activity = clean_text(line_data[1].text)
            tracking_date_search = re.search(date, tracking_date_raw)
            if tracking_date_search:
                tracking_date = tracking_date_search.group()
                tracking_city = re.sub(date, "", tracking_date_raw).strip()
            activity.append({"text":tracking_activity, "date":tracking_date, "city": tracking_city})

        return activity