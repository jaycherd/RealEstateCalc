import copy
from datetime import datetime,timedelta
from typing import List

from models.house import House
from models.house_data import HouseData
from utils.constants import HouseDataConstants as HDC


class RecentSaleData(HouseData):
    def __init__(self, houses: List[House], exclude: House | None = None, months: int = 24) -> None:
        self.exclude = exclude
        self.months = months # how many months back to look
        self.avg_sold_price = None
        self.avg_sold_ppsf = None
        self.avg_soldlist_diff = None
        
        # check houses are recent enough
        tmp = []
        cutoff_date = datetime.now() - timedelta(days=months*30)
        for house in houses:
            if isinstance(house.sold_date, datetime) and house.sold_date > cutoff_date:
                tmp.append(house)
        super().__init__(houses=tmp)

    def _compute_avgs(self):
        super()._compute_avgs()
        sum_sold_ppsf = sum_soldlist_diff = sum_sold_prices = 0
        num_sold = num_sold_n_listed = 0

        for house in self.houses:
            if house.throw_out is True or (self.exclude is not None and house.address == self.exclude.address):
                continue
            if house.sold_ppsf != House.NA and house.sold_price != House.NA:
                sum_sold_ppsf += house.sold_ppsf
                sum_sold_prices += house.sold_price
                num_sold += 1
            if house.sold_price != House.NA and house.list_price != House.NA:
                sum_soldlist_diff += house.sold_price - house.list_price
                num_sold_n_listed += 1

        self.avg_sold_price = sum_sold_prices / num_sold if num_sold != 0 else 0
        self.avg_sold_ppsf = sum_sold_ppsf / num_sold if num_sold != 0 else 0
        self.avg_soldlist_diff = sum_soldlist_diff / num_sold_n_listed if num_sold_n_listed != 0 else 0

    def get_avgs_str(self):
        base_str = super().get_avgs_str()
        return (f"Avgs from {len(self.houses)} sales within {self.months} months\n"
                f"Note: not all sales have list price\n{base_str}"
                f"Avg Sold P      = ${int(self.avg_sold_price):,}\n"
                f"Avg SOLD PPSF   = ${int(self.avg_sold_ppsf):,}\n"
                f"Avg Sold - Lst  = ${int(self.avg_soldlist_diff):,}\n")

    def compare_ranks(self,cmp_house: House) -> str:
        def find_rank(ordered_list: List[House]) -> int:
            for i,house in enumerate(ordered_list):
                if house.address == cmp_house.address:
                    return i+1
            return -1
        # base_str = super().compare_ranks(cmp_house=cmp_house)

        res = []

        tmp_houses = copy.deepcopy(self.houses)
        tmp_houses.append(cmp_house)

        ordered = sorted(tmp_houses,key=lambda x: (x.sold_price if x.address != cmp_house.address else x.for_sale_price))
        rank = find_rank(ordered)
        res.append(f"Sold P   = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        ordered = sorted(tmp_houses,key=lambda x: x.ppsf)
        rank = find_rank(ordered)
        res.append(f"ZPPSF    = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")
        
        ordered = sorted(tmp_houses,key=lambda x: x.sold_ppsf if x.address != cmp_house.address else x.ppsf)
        rank = find_rank(ordered)
        res.append(f"Sold PPSF= {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        ordered = sorted(tmp_houses,key=lambda x: (x.list_price if x.address != cmp_house.address else x.for_sale_price))
        rank = find_rank(ordered)
        res.append(f"List P   = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        return f"Rankings from sales within {self.months} months\n{"".join(res)}"

    def compare_data(self,house: House) -> str:
        base_str = super().compare_data(house=house)

        res = []

        diff = int(house.price - self.avg_sold_price)
        res.append(f"Zprice - Avg SOLD price : {"+"if diff > 0 else ""}${diff:,}\n")

        diff = int(house.for_sale_price - self.avg_sold_price)
        res.append(f"Sale P - Avg Sold P     : {"+"if diff > 0 else ""}${diff:,}\n")

        diff = int(house.ppsf - self.avg_sold_ppsf)
        res.append(f"Zppsf - Avg sold ppsf   : {"+" if diff > 0 else ""}${diff}\n")

        diff = int(house.for_sale_ppsf - self.avg_sold_ppsf)
        res.append(f"Sale ppsf - Avg Soldppsf: {"+" if diff > 0 else ""}${diff}\n")

        return f"Comparisons from sales within {self.months} months\n{base_str}{"".join(res)}"
    
