from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json

# variables (edit below)

skinbox_json = "./skinbox.json"
output_file = "./skinbox-checked.json"

# functions

def check(accepted_ids):
    with open(skinbox_json) as f:
        data = json.load(f)
        skin_list = data["SkinsAdded"]["SkinList"]

        for item in skin_list:
            print(f"Checking {item}:")
            new_skinids = []
            for skin_id in skin_list[item]:
                is_accepted = skin_id in accepted_ids
                if is_accepted:
                    print("    removing: " + accepted_ids[skin_id] + " (is accepted)")
                else:
                    new_skinids.append(skin_id)
            skin_list[item] = new_skinids
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
                    

def download_skinlist():
    print("downloading accepted ids")
    accepted_ids = {}
    req = Request('https://umod.org/documentation/games/rust/definitions', 
                    headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, 'html.parser')
    
    for table in soup.findAll("table",  attrs={"id":"skins-list"}):
        tbody = table.find("tbody")
        if tbody:
            for row in tbody.findAll("tr"):
                skin_id = int(row.find("td", attrs={"class": "col-1"}).string)
                name = row.find("td", attrs={"class": "col-2"}).string
                accepted_ids[skin_id] = name
    print("downloaded list of " + str(len(accepted_ids)) + " accepted skin ids")
    return accepted_ids

accepted_ids = download_skinlist()
check(accepted_ids)