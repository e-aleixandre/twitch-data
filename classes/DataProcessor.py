from typing import Dict, List, Set, Tuple
from itertools import combinations
from datetime import datetime
from tabulate import tabulate
import hashlib
import pandas


class DataProcessor:
    def __init__(self, data: List[Dict[str, List[str]]], min_date: datetime, max_date: datetime, exports: str = "./"):
        self.__min_date__ = min_date
        self.__max_date__ = max_date
        self.__streamers_map__: Dict[str, Set[str]] = self.__build_streamers_map__(data)
        self.__common__viewers__: Dict[Tuple[str, str], int] = self.__build_common_viewers__()
        self.__exports = exports

    @staticmethod
    def __build_streamers_map__(data: List) -> Dict[str, Set[str]]:
        streamers_map = dict()
        for scrape in data:
            for streamer, viewers in scrape["streamers"].items():
                try:
                    streamers_map[streamer] |= set(viewers)  # We assume the key already exists
                except KeyError:
                    streamers_map[streamer] = set(viewers)  # In case it didnt we create it

        return streamers_map

    def __build_common_viewers__(self) -> Dict[Tuple[str, str], int]:
        common_viewers = dict()

        for a, b in combinations(self.__streamers_map__, 2):
            common = self.__streamers_map__[a] & self.__streamers_map__[b]
            common_viewers[(a, b)] = len(common)

        return common_viewers

    def print_results(self):
        print("Viewers per Streamer CSV:\n")
        tmp_list = []
        for key, value in self.__streamers_map__.items():
            tmp_list.append([key, len(value)])

        print(tabulate(tmp_list, headers=["Streamer", "Viewers"]))

        tmp_list.clear()
        for key, value in self.__common__viewers__.items():
            tmp_list.append([key[0], key[1], value])

        print("\nCommon Viewers CSV:\n")
        print(tabulate(tmp_list, headers=["Streamer A", "Streamer B", "Comunes"]))

    def export(self) -> str or None:
        filename = self.__get_filename__()

        sheet_one = self.__get_streamers_viewers_dataframe__()
        sheet_two = self.__get_common_viewers_dataframe__()

        writer = pandas.ExcelWriter(self.__exports + '/' + filename, engine="xlsxwriter")
        # TODO: Write min_date - max_date on cell A1
        sheet_one.to_excel(writer, sheet_name="Viewers per Streamer")
        sheet_two.to_excel(writer, sheet_name="Common viewers")

        writer.save()

        return filename

    def __get_filename__(self) -> str:
        # TODO CONSIDER:
        #  Is it reasonable to use a hashed filename?
        date_format = "%Y-%m-%d %Hh"

        min_date = self.__min_date__.strftime(date_format)
        max_date = self.__max_date__.strftime(date_format)

        hashed_name = hashlib.sha224()
        hashed_name.update(min_date.encode('utf-8'))
        hashed_name.update(max_date.encode('utf-8'))
        hashed_name = hashed_name.hexdigest()

        return hashed_name + '.xlsx'

    def __get_streamers_viewers_dataframe__(self):
        data = []
        for key, value in self.__streamers_map__.items():
            data.append((key, len(value)))

        return pandas.DataFrame(data, columns=["Streamer", "Viewers"])

    def __get_common_viewers_dataframe__(self):
        data = []
        for key, value in self.__common__viewers__.items():
            data.append((key[0], key[1], value))

        return pandas.DataFrame(data, columns=["Streamer A", "Streamer B", "Common Viewers"])
