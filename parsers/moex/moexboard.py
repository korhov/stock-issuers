from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime

from html.parser import HTMLParser

from models.issuers import DataIssuers


class MyHTMLParser(HTMLParser):
    is_tr = False
    is_td = False

    row: list = []

    rows: list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.is_tr = True
            self.row = []
        if tag == 'td':
            self.is_td = True

    def handle_data(self, data):
        if self.is_tr and self.is_td:
            self.row.append(data)

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.is_tr = False
            self.rows.append(self.row.copy())
        if tag == 'td':
            self.is_td = False


class InstrumentsList(object):
    _browser: Chrome = None

    def __init__(self):
        if not os.path.exists(self.path_data):
            os.makedirs(self.path_data)
        if not os.path.exists(self.path_data_source):
            os.makedirs(self.path_data_source)

    @property
    def path_data(self):
        return './data/'

    @property
    def path_data_source(self):
        return self.path_data + 'instruments-list/'

    @property
    def browser(self) -> Chrome:
        if self._browser is None:
            # @todo: Нужно ещё раз протестировать
            print('new browser')

            opts = Options()
            opts.headless = True
            opts.add_argument('--no-sandbox')
            opts.add_argument('window-size=1920x1440')
            opts.add_argument("--start-maximized")
            opts.add_argument("--allow-http-screen-capture")
            opts.add_argument("--start-fullscreen")

            browser = Chrome(chrome_options = opts)
            # browser.implicitly_wait(10)

            return browser
        else:
            return self._browser

    def load_page(self, page_load: int):
        if page_load > 20:
            return

        time.sleep(randint(10, 20))

        with open(self.path_data_source + 'page-' + str(page_load) + '.html', 'w') as file:
            file.write(self.browser.page_source)
        self.browser.save_screenshot(self.path_data_source + 'page-' + str(page_load) + '.png')

        is_span = False
        current_page = 1
        for page in self.browser \
                .find_element_by_id('ctl00_PageContent_gvInstrumentsList') \
                .find_element_by_class_name('pagination') \
                .find_element_by_tag_name('tr') \
                .find_elements_by_tag_name('td'):
            text = page.get_attribute('innerHTML')
            if str(text).startswith('<span>'):
                is_span = True
            elif not is_span:
                current_page += 1
            else:
                link = page.find_element_by_tag_name('a')
                link.click()

                time.sleep(2)  # @todo: Это не правильно, нужно что-то другое придумать/найти

                element = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'ctl00_PageContent_gvInstrumentsList'))
                )

                self.load_page(page_load + 1)

                break

    def parser(self):
        self.browser.get('https://www.moex.com/ru/moexboard/instruments-list.aspx')

        self.load_page(1)

    def html_to_csv(self):
        parser = MyHTMLParser()

        with open(self.path_data + "issuers.csv", "w+", newline = '') as out_file:
            writer = csv.writer(out_file, delimiter = '\t', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for root, dirs, files in os.walk(self.path_data_source):
                for file in files:
                    if file.endswith(".html"):
                        with open(os.path.join(root, file), "r") as page_file:
                            html = page_file.read()
                            page_file.close()

                            _start = html.find('<tbody>', html.find('<table class="table1 table-securities-list" border="0" id="ctl00_PageContent_gvInstrumentsList">')) + 7

                            parser.rows = []
                            parser.feed(html[_start:html.find('<tr class="pagination" align="left" valign="middle">', _start)])

                            for row in parser.rows[1:]:
                                row[4] = str(row[4]).upper()
                                if len(str(row[7]).replace('\xa0', '')) != 0:
                                    row[7] = datetime.datetime.strptime(str(row[7]), u'%d.%m.%Y')
                                row[10] = str(row[10]).replace('\xa0', '')
                                row[8] = str(row[8]).replace('\xa0', '').replace(',', '.')
                                if len(row[8]) == 0:
                                    row[8] = None
                                else:
                                    row[8] = float(str(row[8]))

                                del row[0]
                                writer.writerow(row)
