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
            line_data = line.find_all("td")
            tracking_date = clean_text(line_data[0].text)
            tracking_activity = clean_text(line_data[1].text)
            activity.append({"text":tracking_activity, "date":tracking_date})

        return activity