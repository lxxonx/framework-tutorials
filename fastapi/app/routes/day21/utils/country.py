import csv


def get_country_from_country_code(country_code: str):
    with open("app/routes/day21/libs/country_map.csv") as csvfile:
        reader = csv.reader(csvfile, doublequote=False)
        for [country, alpha2, _, _, _, _] in reader:
            if alpha2.strip().replace('"', "") == country_code.upper():
                return country
