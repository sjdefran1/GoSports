import requests
import json
from bs4 import BeautifulSoup
from nba_api.stats.static import teams


# get team primary color 
def main():
    site = requests.get("https://teamcolorcodes.com/nba-team-color-codes/")
    soup = BeautifulSoup(site.content, 'html.parser')
    # get all the tables from the page
    tables = soup.find_all('div', class_="su-table su-table-responsive su-table-alternate")
    # get the hex table, 4th on page
    hex_tables = tables[3]
    
    # get rid of Nba colors row
    rows = hex_tables.find_all('tr')[1:]
    primarys = {}
    
    for row in rows:
        # ' Boston Celtics '
        team_name = row.find('th').get_text().split()[-1]
        team_id = teams.find_teams_by_nickname(team_name)[0].get('id')
        # 'Celtics Green #007A33' .split() -> ['Celtics', 'Green', '#007A33'] 
        # [-1] gets last element in list, the hex value
        team_primary = row.find('td').get_text().split()[-1]
        # {"Celtics": "#007A33"}
        primarys.update({f"{team_id}" : team_primary})
    
    with open("colors.json", "w") as outfile:
        json.dump(primarys, outfile)

if __name__ == "__main__":
    main()