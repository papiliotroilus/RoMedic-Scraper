import requests
from bs4 import BeautifulSoup, SoupStrainer

# initialise contact links list
links = set()

# open and process specialisations file
with open('specializari.txt') as specializari:
    for specializare in specializari:
        specializare = specializare.rstrip('\r\n')
        print('processing', specializare)
        # initialise specialisation processing
        keep_going = True
        page_num = 1
        old_links = []
        new_links = []
        while keep_going:
            # parse search page
            try:
                print('processing page', page_num)
                url = specializare + "/pag--" + str(page_num)
                page = requests.get(url).content
                # identify results container
                soup = BeautifulSoup(page, parse_only=SoupStrainer(class_='shortdes'), features="html.parser")
                # identify doctor links in search results
                for link in soup.find_all('a', href=True):
                    # process doctor links to contact links
                    new_links.append('https://www.romedic.ro' + link['href'] + '/contact')
                # determine if last page is reached
                if len(new_links) == 0 or set(old_links) == set(new_links):
                    print('done with', specializare)
                    keep_going = False
                # add new links to list
                else:
                    links.update(new_links)
                    old_links = new_links
                    new_links = []
            except Exception as e:
                print('broke')
                keep_going = False
                break
            # iterate to next page
            page_num += 1

# write contact links to file
with open('adrese.txt', 'w') as f:
    for link in links:
        f.write("%s\n" % link)
    print('all done :)')
