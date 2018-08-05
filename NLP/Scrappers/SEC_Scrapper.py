#ce sript il faut qu'il chope les 10_K de toutes les boites pour 2016 pour pouvoir reporduire l'analyse des manos de medium
#essayer un try catch print error
#on a besoin que des 10-K

    
from pymongo import MongoClient



class SecCrawler():

    def __init__(self, filing_type):
        client = MongoClient('localhost', 27017)
        self.db = client['SEC_Datas']
        self.filing_type = self.db[filing_type]
        self.correspondance = {'AAPL':'0000320193', 'Microsoft':'000119312514289961'}


    def get_10ks(self, max_date, count, company):
        count=100
        cik = self.correspondance[company]
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type=10-K&dateb="+str(max_date)+"&owner=exclude&output=xml&count="+str(count)+'&output=xml'
        r = requests.get(base_url)
        data = r.text
        soup = BeautifulSoup(data)
        link_list=[]

        for link in soup.find_all('filinghref'):
            URL = link.string
            link_list.append(URL)
        self.link_list = link_list


    def save_in_mongoDB(self):
        for year_links in self.link_list[:4]:
            K_10_link = get_K_10_link(year_links)
            r=requests.get(K_10_link)
            data = r.text
            soup = BeautifulSoup(data)
            text = soup.get_text(strip=True)
            discussion = text.split('Overview and Highlights')[1].split('Item 8.')[0]
            date = text.split('For the fiscal year ended')[1].split('or')[0][-4:]
            self.filing_type.insert_one({'date':date, '10_K':discussion})


def get_K_10_link(documents_link):
    r = requests.get(documents_link)
    data = r.text
    soup = BeautifulSoup(data)
    tables = soup.findAll('table')
    table = tables[0]
    return 'http://www.sec.gov/'+table.find('tr').nextSibling.nextSibling.find('td').nextSibling.nextSibling.nextSibling.nextSibling.find('a')['href']

SecCrawler_object = SecCrawler('sec_10_K')

SecCrawler_object.get_10ks(2017, 100, 'AAPL')
SecCrawler_object.save_in_mongoDB()
