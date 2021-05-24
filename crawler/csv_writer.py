import csv
import re

class CSVWriter:
    header = ['url', 'title', 'description']
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self, url, title, description):
        super().__init__()
        self.url = url
        self.title = title
        self.description = description
        self.writeRow()

    def writeRow(self):
        with open('data/crawled.csv', 'a', encoding='UTF8', newline='') as f:
            if re.match(self.regex, str(self.url)) is not None:
                writer = csv.writer(f)
                writer.writerow([str(self.url), str(self.title), str(self.description)])

class TxtWrite:
    def __init__(self, path, url):
        super().__init__()
        self.path = path
        self.url = url
        self.write()

    def write(self):
        with open(str(self.path), "a") as f:
            if type(self.url) is set:
                for i in self.url:
                    f.write(str(i) + '\n')
            else:
                f.write(str(self.url) + '\n')


class TxtRead:
    def __init__(self, path):
        super().__init__()
        self.path = path

    def readStr(self):
        url = None
        data = None
        with open(str(self.path), "r") as f:
            url = f.readline().rstrip('\n')
            data = f.read().splitlines(True)
        with open(str(self.path), 'w') as f:
            f.writelines(data[1:])
        return url
