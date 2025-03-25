import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import os.path

def scrape() -> None:
    # creating folders if don't exist
    os.makedirs(os.path.dirname('results/ee_rdn/ee_rdn.csv'), exist_ok=True)
    # os.makedirs(os.path.dirname('results/ee_rdb_pln/ee_rdb_pln.csv'), exist_ok=True)
    # os.makedirs(os.path.dirname('results/ee_rdb_eur/ee_rdb_eur.csv'), exist_ok=True)
    os.makedirs(os.path.dirname('results/gz_rdn/gz_rdn.csv'), exist_ok=True)
    # os.makedirs(os.path.dirname('results/gz_rdb/gz_rdb.csv'), exist_ok=True)

    # creating calendar
    base = datetime.today().date()
    date_list = [(base - timedelta(days=x)).strftime("%d-%m-%Y") for x in reversed(range(60))]


    for date in date_list:
        if not os.path.exists(f"results/ee_rdn/EE_RDN_{date}.csv"):
            r = requests.get(f'https://tge.pl/energia-elektryczna-rdn?dateShow={date}&dateAction=next')
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, "html.parser")

                table = soup.find_all('table', attrs={'id': 'footable_kontrakty_godzinowe'})
                table_rows = table[0].find_all('tr')

                li = []
                for tr in table_rows:
                    td = tr.find_all('td')
                    row = ["".join(tr.get_text().split()) for tr in td]
                    li.append(row)
                df = pd.DataFrame(li, columns=["Time", "F1_Price", "F1_Vol", "F2_Price", "F2_Vol", "Const_Price", "Const_Vol"])
                df.drop(index=df.index[:2],
                        axis=0,
                        inplace=True)
                df.reset_index(drop=True,
                            inplace=True)
                df.to_csv(f"results/ee_rdn/EE_RDN_{date}.csv", index=False)


        # RDB w PLN
    #     if not os.path.exists(f"ee_rdb_pln/EE_RDB_PLN_{date}.csv"):
    #         r = requests.get(f'https://tge.pl/energia-elektryczna-rdb?dateShow={date}&dateAction=')
    #         if r.status_code == 200:
    #             soup = BeautifulSoup(r.content, "html.parser")

    #             table = soup.find_all('table', attrs={'id': 'footable_kontrakty_godzinowe'})
    #             table_rows = table[0].find_all('tr')

    #             li = []
    #             for tr in table_rows:
    #                 td = tr.find_all('td')
    #                 row = ["".join(tr.find('span').get_text().split())
    #                        if tr.find('span', attrs={'class':'table-pln'}) else "".join(tr.get_text().split())
    #                        for tr in td]
    #                 li.append(row)
    #             df = pd.DataFrame(li, columns=["Time", "Chart", "Min_Price_Today", "Max_Price_Today",
    #                                            "Last_Price_Today", "Vol_Today", "Chart",
    #                                            "Min_Price_Tomorrow", "Max_Price_Tomorrow",
    #                                            "Last_Price_Today", "Vol_Today"])
    #             df.drop(index=df.index[:2],
    #                     axis=0,
    #                     inplace=True)
    #             df.reset_index(drop=True,
    #                            inplace=True)
    #             df.to_csv(f"ee_rdb_pln/EE_RDB_PLN_{date}.csv", index=False)

    #     #RDB w EUR
    #     if not os.path.exists(f"ee_rdb_eur/EE_RDB_EUR_{date}.csv"):
    #         r = requests.get(f'https://tge.pl/energia-elektryczna-rdb?dateShow={date}&dateAction=')
    #         if r.status_code == 200:
    #             soup = BeautifulSoup(r.content, "html.parser")

    #             table = soup.find_all('table', attrs={'id': 'footable_kontrakty_godzinowe'})
    #             table_rows = table[0].find_all('tr')

    #             li = []
    #             for tr in table_rows:
    #                 td = tr.find_all('td')
    #                 row = ["".join(tr.find_all('span')[1].get_text().split())
    #                        if tr.find('span', attrs={'class':'table-pln'}) else "".join(tr.get_text().split())
    #                        for tr in td]
    #                 li.append(row)
    #             df = pd.DataFrame(li, columns=["Time", "Chart", "Min_Price_Today", "Max_Price_Today",
    #                                            "Last_Price_Today", "Vol_Today", "Chart",
    #                                            "Min_Price_Tomorrow", "Max_Price_Tomorrow",
    #                                            "Last_Price_Today", "Vol_Today"])
    #             df.drop(index=df.index[:2],
    #                     axis=0,
    #                     inplace=True)
    #             df.reset_index(drop=True,
    #                            inplace=True)
    #             df.drop(columns=['Chart'],
    #                     inplace=True)
    #             df = df.convert_dtypes()
    #             df.to_csv(f"ee_rdb_eur/EE_RDB_EUR_{date}.csv", index=False)


        # #GZ - RDN
        if not os.path.exists(f"results/gz_rdn/GZ_RDN_{date}.csv"):
            r = requests.get(f'https://tge.pl/gaz-rdn?dateShow={date}&dateAction=')
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, "html.parser")

                table = soup.find('table', attrs={'id': 'footable_indeksy_0'})
                table_rows = table.find_all('tr')

                li = []
                for tr in table_rows:
                    td = tr.find_all('td')
                    row = ["".join(tr.get_text().split()) for tr in td]
                    li.append(row)
                df = pd.DataFrame(li, columns=["Index", "Chart", "Price", "Price_Change", "Vol", "Vol_Change"])
                df.drop(index=df.index[:1],
                        axis=0,
                        inplace=True)
                df.drop(index=df.index[1:],
                        axis=0,
                        inplace=True)
                df.reset_index(drop=True,
                            inplace=True)
                df.drop(columns=['Chart'],
                        inplace=True)
                df = df.convert_dtypes()
                df.to_csv(f"results/gz_rdn/GZ_RDN_{date}.csv", index=False)


    #     #GZ - RDB
    #     if not os.path.exists(f"gz_rdb/GZ_RDB_{date}.csv"):
    #         r = requests.get(f'https://tge.pl/gaz-rdb?dateShow={date}&dateAction=')
    #         if r.status_code == 200:
    #             soup = BeautifulSoup(r.content, "html.parser")

    #             table = soup.find('table', attrs={'id': 'footable_indeksy_0'})
    #             table_rows = table.find_all('tr')

    #             li = []
    #             for tr in table_rows:
    #                 td = tr.find_all('td')
    #                 row = ["".join(tr.get_text().split()) for tr in td]
    #                 li.append(row)
    #             df = pd.DataFrame(li, columns=["Index", "Chart", "Price", "Price_Change", "Vol", "Vol_Change"])
    #             df.drop(index=df.index[:1],
    #                     axis=0,
    #                     inplace=True)
    #             df.drop(index=df.index[1:],
    #                     axis=0,
    #                     inplace=True)
    #             df.reset_index(drop=True,
    #                            inplace=True)
    #             df.drop(columns=['Chart'],
    #                     inplace=True)
    #             df = df.convert_dtypes()
    #             df.to_csv(f"gz_rdb/GZ_RDB_{date}.csv", index=False)

