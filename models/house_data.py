from typing import Dict,Union,List

from models.house import House

class HouseData:
    def __init__(self, data: Union[Dict[str,House],List[House]]) -> None:
        # normalize incoming data
        if isinstance(data, dict):
            self.houses = list(data.values())
        elif isinstance(data, list):
            self.houses = data
        else:
            raise ValueError("Houses should be either a dictionary or a list of House objects")

        sum_prices, sum_sq_ft, sum_beds, sum_baths, sum_ppsf, sum_pools = 0, 0, 0, 0, 0, 0
        num_houses = len(self.houses)

        for house in self.houses:
            if house.throw_out == 1:
                continue
            sum_prices += house.price
            sum_sq_ft += house.sq_ft
            sum_beds += house.beds
            sum_baths += house.baths
            sum_ppsf += house.ppsf
            sum_pools += house.pool

        self.avg_price = sum_prices / num_houses
        self.avg_sq_ft = sum_sq_ft / num_houses
        self.avg_beds = sum_beds / num_houses
        self.avg_baths = sum_baths / num_houses
        self.avg_ppsf = sum_ppsf / num_houses
        self.avg_pools = sum_pools / num_houses

    def __repr__(self):
        return (f"Avg price = ${int(self.avg_price):,}\n"
                f"Avg sqft  = {int(self.avg_sq_ft)}\n"
                f"Avg beds  = {round(self.avg_beds,1)}\n"
                f"Avg baths = {round(self.avg_baths,1)}\n"
                f"Avg ppsf  = ${int(self.avg_ppsf):,}\n"
                f"Avg pools = {round(self.avg_pools,2)}\n")