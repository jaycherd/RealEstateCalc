from typing import Dict, List
from models.house import House
from models.house_data import HouseData

class SimSqftData(HouseData):
    def __init__(self, data: Dict[str, House] | List[House], cmp_house: House, max_diff : int = 75) -> None:
        super().__init__(data)
        self.max_diff = max_diff
        tmp = []
        for house in self.houses:
            if abs(house.sq_ft - cmp_house.sq_ft) > self.max_diff:
                continue
            tmp.append(house)
        self.houses = tmp

