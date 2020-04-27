import wikipedia, re
from BeautifulSoup import BeautifulSoup
 
def get_hispanic_population_data():
    wiki_search_string = "NCAA Division I Men's Basketball"
    wiki_page_title = "2018 NCAA Division I Men's Basketball Tournament"
    wiki_table_caption = "South Regional"
    parsed_table_data = []
 
    search_results = wikipedia.search(wiki_search_string)
    for result in search_results:
        if wiki_page_title in result:
            my_page = wikipedia.page(result)
            #download the HTML source
            soup = BeautifulSoup(my_page.html())
            #Using a simple regex to do 'caption contains string'
            table = soup.find('caption',text=re.compile(r'%s'%wiki_table_caption)).findParent('table')
            rows = table.findAll('tr')
            for row in rows:
                children = row.findChildren(recursive=False)
                row_text = []
                for child in children:
                    clean_text = child.text
                    #This is to discard reference/citation links
                    clean_text = clean_text.split('&#91;')[0]
                    #This is to clean the header row of the sort icons
                    clean_text = clean_text.split('&#160;')[-1]
                    clean_text = clean_text.strip()
                    row_text.append(clean_text)
                parsed_table_data.append(row_text)
    return parsed_table_data