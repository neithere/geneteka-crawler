import json

import argh
import requests
from bs4 import BeautifulSoup


BASE_HOST = "http://geneteka.genealodzy.pl"
BASE_URL = BASE_HOST + "/index.php"


def main(surname, *, surname2: str | None = None, from_date: str | None = None, to_date: str | None = None):
    search_results = search(surname, surname2=surname2, from_date=from_date, to_date=to_date)

    report = parse_search_results(search_results)

    return json.dumps(report, indent=4)


def search(surname, *, surname2: str | None = None, from_date: str | None = None, to_date: str | None = None):
    params = {
        "search_lastname": surname,
        "search_lastname2": surname2 or "",
        "from_date": from_date or "",
        "to_date": to_date or "",
        "rpp1": "",
        "bdm": "",
        "w": "",
        "op": "se",
        "lang": "pol",
    }
    resp = requests.get(BASE_URL, params=params)
    return resp.text


def parse_search_results(html):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all(lambda tag: tag.name == "table")
    totals = tables[-1].find_all(lambda tag: tag.name == "td" and tag.text == "Razem")[0]
    table = totals.parent.parent
    results = []
    for row in table:
        place, births, deaths, marriages = [cell for cell in row if cell.text != "\n"]

        # skip header and footers
        if place.text.strip() in ("Tereny", "Razem") or not place.text.strip():
            continue

        result = {
            "place": place.text.strip(),
            "births": _parse_subtotal(births),
            "deaths": _parse_subtotal(deaths),
            "marriages": _parse_subtotal(marriages),
        }

        results.append(result)

    report = {
        "totals": {
            "births": int(totals.find_next_sibling().text),
            "deaths": int(totals.find_next_sibling().find_next_sibling().text),
            "marriages": int(totals.find_next_sibling().find_next_sibling().find_next_sibling().text),
        },
        "by_region": results,
    }
    return report


def _parse_subtotal(cell):
    if not cell.text.strip():
        return None

    data = {
        "total": int(cell.text),
    }
    if cell.a:
        data["url"] = BASE_HOST + cell.a["href"]
    return data


def main_cli():
    argh.dispatch_command(main)
