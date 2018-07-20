#!/usr/bin/python3.7
from bs4 import BeautifulSoup as BS
import urllib.request, urllib.error, sys, ssl
import mysql_write

loc = ""
loc_localize = ""

def getData(auct_id, loc_):
    global loc
    global loc_localize
    
    if auct_id.endswith("303"):
        loc += "ugm.ac"
        loc_localize += "LPSE UGM"
    elif auct_id.endswith("367"):
        loc += "kulonprogokab.go"
        loc_localize += "LPSE Kulon Progo"
    elif auct_id.endswith("021"):
        loc += "jogjakota.go"
        loc_localize += "LPSE Yogyakarta Kota"
    elif auct_id.endswith("054"):
        loc += "slemankab.go"
        loc_localize += "LPSE Sleman"
    elif auct_id.endswith("013"):
        loc += "jogjaprov.go"
        loc_localize += "LPSE Provinsi DI Yogyakarta"
    elif auct_id.endswith("621"):
        loc += "gunungkidulkab.go"
        loc_localize += "LPSE Gunungkidul"
    elif auct_id.endswith("285"):
        loc += "bantulkab.go"
        loc_localize += "LPSE Bantul"

    try:
        if not auct_id.endswith("054"):
            html = urllib.request.urlopen("http://lpse."+loc+".id/eproc4/evaluasi/"+auct_id+"/pemenang")
            soup = BS(html, 'html.parser')
        else:
            context = ssl._create_unverified_context()
            html = urllib.request.urlopen("http://lpse."+loc+".id/eproc4/evaluasi/"+auct_id+"/pemenang", context=context)
            soup = BS(html, 'html.parser')

    except urllib.error.HTTPError as e:
        print('Error: ', e.code)
        
    except urllib.error.URLError as e:
        print('Error: ', e.reason)
    else:
        try:
            name = soup.find_all('td')[0].get_text()
            type = soup.find_all('td')[1].get_text()
            instance = soup.find_all('td')[2].get_text()
            if not auct_id.endswith("054"):
                winner = soup.find_all('td')[7].get_text()
            else:
                winner = soup.find_all('td')[6].get_text()
            
            loc = ""
            loc_localize = ""
            
            mysql_write.writeData("root", "", "localhost", "pkl", auct_id, name, type, instance, winner, loc_)
            
        except IndexError:
            print("Pemenang tidak ditemukan")
            loc = ""
            loc_localize = ""

if __name__ == "__main__":
    auct_id = str(sys.argv[1])
    loc_ = str(sys.argv[2])

    getData(auct_id, loc_)