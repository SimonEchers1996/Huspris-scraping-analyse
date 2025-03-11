from scraping.for_scraping import get_property, treat_property, get_links, with_page
import pandas as pd

rows = []
types = ['auction','family','normal']
page_nos_by_type = {
    'auction': [i+1 for i in range(2)],
    'family': [i+1 for i in range(55)],
    'normal': [i+1 for i in range(500)]
}
for type in types:
    for page_no in page_nos_by_type[type]:
        print(page_no)
        try:
            url = with_page(page_no,type)
            links = get_links(url)
        except:
            continue
        if links:
            print('There are links!')
        for link in links:
            try:
                content = get_property(link)
                property = treat_property(content,type)
                rows.append(property)
            except:
                continue

df = pd.DataFrame.from_dict(rows, orient='columns')
df = df.drop_duplicates()
df.to_csv('OdenseHousePrices.csv', index=False)
