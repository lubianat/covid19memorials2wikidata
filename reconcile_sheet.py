#!/usr/bin/env python3
import json
import os
import re
import time
import traceback

import pandas as pd
from wdcuration import convert_date_to_quickstatements
import wikidata
from wikidataintegrator import wdi_core, wdi_login


def main():
    global DICTS
    os.system(
        "wget -O memorials.xlsx https://docs.google.com/spreadsheets/d/e/"
        "2PACX-1vRIg3Ed2JZGe4cEiZIAgzI3f0gLkgIrfAHYDkLKnzbkuZbas_p6hOLHN1y9clvd-5ushxaFJHszUSln/"
        "pub?output=xlsx"
    )

    memorials = pd.read_excel("memorials.xlsx", sheet_name="Página1")
    keys_df = pd.read_excel("memorials.xlsx", sheet_name="Reconciliação")
    wikidata_dict = dict(zip(keys_df.label, keys_df.qid))

    qs = ""
    for i, row in memorials.iterrows():
        if row["Altura"] != row["Altura"]:
            continue
        qs += f"""
        CREATE
        LAST|Len|"{row['Nome']}"
        LAST|Lpt|"{row['Nome']}"
        LAST|Den|"COVID-19 memorial in {row['Cidade']}"
        LAST|Len|"Memorial da COVID-19 em {row['Cidade']}"  
        LAST|P31|Q110852723|S854|"{row['Link da fonte']}"
        LAST|P17|Q155
        LAST|P571|{convert_date_to_quickstatements(str(row['Data de criação']),"%Y%m%d")}
        LAST|P131|{wikidata_dict[row["Cidade"]]}
        LAST|P973|"{row['Link da fonte']}"
        """

        for name in ["Autoria1", "Autoria2", "Autoria3"]:
            if row[name] == row[name]:  # Check for nan
                qs += f"""
                LAST|P50|{wikidata_dict[row[name]]}"""

        for name in ["Material1", "Material2"]:
            if row[name] == row[name]:  # Check for nan
                qs += f"""
                LAST|P186|{wikidata_dict[row[name]]}"""

        for name in ["Tipo1", "Tipo2", "Tipo3"]:
            if row[name] == row[name]:  # Check for nan
                qs += f"""
                LAST|P31|{wikidata_dict[row[name]]}"""

        if row["Altura"] == row["Altura"]:  # Check for nan
            qs += f"""
          LAST|P2048|{row["Altura"].replace("m", "")}U11573"""

        if row["Largura"] == row["Largura"]:  # Check for nan
            qs += f"""
          LAST|P2048|{row["Largura"].replace("m", "")}U11573"""

        if row["Área (m²)"] == row["Área (m²)"]:  # Check for nan
            qs += f"""
          LAST|P2048|{row["Área (m²)"]}U25343"""

        if row["Peso (T)"] == row["Peso (T)"]:  # Check for nan
            qs += f"""
          LAST|P2048|{row["Peso (T)"]}U191118"""

        lat = str(row["Lat. (sem form.)"])[:2] + "." + str(row["Lat. (sem form.)"])[2:]
        long = (
            str(row["Long. (sem form.)"])[:2] + "." + str(row["Long. (sem form.)"])[2:]
        )

        qs += f"""
        LAST|P625|@-{lat}/-{long}
        """
        print(qs)
        break


if __name__ == "__main__":
    main()
