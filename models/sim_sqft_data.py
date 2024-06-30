from typing import List
from models.house import House
from models.house_data import HouseData

class SimSqftData(HouseData):
    def __init__(self, houses: List[House], cmp_house: House, max_diff : int = 75) -> None:
        self.max_diff = max_diff
        
        # get rid of houses with square footage diff by more than max diff
        tmp = []
        for house in houses:
            if abs(house.sq_ft - cmp_house.sq_ft) > self.max_diff:
                continue
            tmp.append(house)
        
        # sort by the difference
        tmp = sorted(tmp, key = lambda x: abs(x.sq_ft - cmp_house.sq_ft))
        super().__init__(tmp)
        


