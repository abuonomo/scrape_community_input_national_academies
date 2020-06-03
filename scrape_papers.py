# Scrape community input table from the National Academies site.
# author: Anthony Buonomo
# email: arb246@georgetown.edu


import argparse
import logging
import atexit
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

BROWSER = webdriver.Chrome("./chromedriver")
atexit.register(lambda: BROWSER.quit())


def get_table_vals(html_content, base_url):
    LOG.info("Getting table from page")
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(id="ContentPlaceHolder1_gvFileList") # Get the table from the page
    table_rows = table.find_all('tr')
    vals = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        link_path = tr.find_all('a')[0].attrs['href']
        link = f"{base_url}/{link_path}"
        row.append(link)
        vals.append(row)
    return vals[1:-3]


def main(outfile):
    LOG.info("Navigating to the site.")
    base_url = 'https://www8.nationalacademies.org/astro2010'
    url = f'{base_url}/publicview.aspx'
    BROWSER.get(url)

    LOG.info("Getting contents of table on first page.")
    page_buttons_sel = '#ContentPlaceHolder1_gvFileList > tbody > tr:nth-child(27) > td > table > tbody'
    tbody = BROWSER.find_element_by_css_selector(page_buttons_sel)
    page_buttons = tbody.find_elements_by_css_selector('tr > td')
    page_vals = get_table_vals(BROWSER.page_source, base_url)

    LOG.info("Getting contents of table on other pages.")
    click_next = False
    button_index = 0
    while button_index < len(page_buttons):
        button = page_buttons[button_index]
        if click_next is False:
            try:
                button.find_element_by_css_selector('span')
                click_next = True
            except NoSuchElementException:
                pass
        else:
            LOG.info(f"Clicking on page {button.text}")
            next_button = button.find_element_by_css_selector('a')
            next_button.click()

            vals = get_table_vals(BROWSER.page_source, base_url)
            page_vals = page_vals + vals
            try:
                tbody = BROWSER.find_element_by_css_selector(page_buttons_sel)
            except NoSuchElementException:
                LOG.info('Visited all pages')
                break
            page_buttons = tbody.find_elements_by_css_selector('tr > td')
            click_next = False
            button_index = 0
            continue
        button_index += 1

    import ipdb; ipdb.set_trace()
    df = pd.DataFrame(page_vals)
    df.columns = ['Author', 'Institution', 'Title', 'FileName', 'FileUrl']

    LOG.info(f"Writing results to {outfile}.")
    df.to_csv(outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Scrape community input table from the National Academies site.')
    parser.add_argument('o', help='output csv file')
    args = parser.parse_args()
    main(args.o)
