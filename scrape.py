from requests import get
from bs4 import BeautifulSoup
import os

BASE_URL = "https://courses.engr.illinois.edu"
URL = "https://courses.engr.illinois.edu/cs225/sp2021/pages/lectures.html"

def get_rows(page):
    rows = page.find_all('div', class_="lecture-row")
    rows.reverse() # to get the proper order
    return rows

def get_row_info(row):
    cards = row.find_all('div', class_="card-body")
    return [get_card_info(card) for card in cards]

def get_card_info(card):
    title = card.find('h5').text
    slide_links = card.find_all('li', string="slides")
    download_link = None # in case there is nothing
    if len(slide_links) > 0:
        download_link = BASE_URL + slide_links[0].find('a')['href']

    return title, download_link

def test_extractors():
    page = BeautifulSoup(get(URL).text, features="html.parser")
    rows = get_rows(page)
    assert len(rows) == 15, "There are 15 weeks of lectures"
    assert "Introduction" in rows[0].text, "The first row has the intro lecture"

    # normal row
    third_row = rows[2]
    third_week_info = get_row_info(third_row)
    assert len(third_week_info) == 3, "Get all three lectures"
    
    sample_title, sample_url = third_week_info[0]
    assert sample_title == "Overloading"
    assert sample_url == "https://courses.engr.illinois.edu/cs225/sp2021/assets/lectures/slides/cs225sp21-07-overloading-slides.pdf"

    # missing row
    missing_row = rows[5]
    missing_row_info = get_row_info(missing_row)
    assert missing_row_info[2] == ("Exam 1", None), "Missing links get None"

if __name__ == "__main__":
    page_html = get(URL).text

    page = BeautifulSoup(page_html, features="html.parser")
    rows = get_rows(page)

    for i, row in enumerate(rows):
        week_num = i + 1
        folder_name = f"week{week_num}"
        os.makedirs(folder_name, exist_ok=True)

        row_info = get_row_info(row)
        for title, slide_url in row_info:
            if slide_url is None:
                continue
            
            file_name = f"{folder_name}/{title}.pdf"
            print(file_name)
            slide_content = get(slide_url).content
            with open(file_name, "wb") as slide_file:
                slide_file.write(slide_content)
            print(f"Downloaded: {file_name}")
        
        print(f"Downloaded Week{week_num}")
        print()
    
    breakpoint()