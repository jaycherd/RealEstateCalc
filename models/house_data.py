from typing import Dict,Union,List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter

from utils.constants import HouseDataConstants as HDC
from models.house import House


class HouseData:
    def __init__(self, houses: List[House]) -> None:
        self.houses = houses
        self.min_ppsf = None
        self.max_ppsf = None
        self.avg_baths = None
        self.avg_beds = None
        self.avg_pools = None
        self.avg_ppsf = None
        self.avg_price = None
        self.avg_remod_score = None
        self.avg_sq_ft = None
        self._compute_avgs()

    def _compute_avgs(self):
        sum_prices = sum_sq_ft = sum_beds = sum_baths = sum_ppsf = sum_pools = 0
        sum_remod_score = num_remodels = num_houses = 0
        num_prices = 0
        self.min_ppsf = self.max_ppsf = None

        for house in self.houses:
            if house.throw_out is True:
                continue
            if self.min_ppsf is None:
                self.min_ppsf = self.max_ppsf = house.ppsf if house.ppsf != house.NA else None
            else:
                self.min_ppsf = min(self.min_ppsf,house.ppsf) if house.ppsf != House.NA else self.min_ppsf
                self.max_ppsf = max(self.max_ppsf,house.ppsf) if house.ppsf != House.NA else self.max_ppsf
            if house.price != House.NA and house.ppsf != House.NA and house.sq_ft != House.NA:
                num_prices += 1
                sum_prices += house.price
                sum_ppsf += house.ppsf
                sum_sq_ft += house.sq_ft
            if house.remod_score != House.NA and house.remod_score != -1:
                sum_remod_score += house.remod_score
                num_remodels += 1
            if House.NA not in {house.beds, house.baths, house.pool}:
                sum_beds += house.beds
                sum_baths += house.baths
                sum_pools += house.pool
                num_houses += 1

        self.avg_price = sum_prices / num_prices if num_prices != 0 else 0
        self.avg_sq_ft = sum_sq_ft / num_prices if num_prices != 0 else 0
        self.avg_beds = sum_beds / num_houses if num_houses != 0 else 0
        self.avg_baths = sum_baths / num_houses if num_houses != 0 else 0
        self.avg_ppsf = sum_ppsf / num_prices if num_prices != 0 else 0
        self.avg_pools = sum_pools / num_houses if num_houses != 0 else 0
        self.avg_remod_score = sum_remod_score / num_remodels if num_remodels != 0 else 0

    def __repr__(self):
        return " "
    
    def get_avgs_str(self):
        return (f"Avg Zprice      = ${int(self.avg_price):,}\n"
                f"Avg sqft        = {int(self.avg_sq_ft)}\n"
                f"Avg beds        = {round(self.avg_beds,1)}\n"
                f"Avg baths       = {round(self.avg_baths,1)}\n"
                f"Avg ppsf        = ${int(self.avg_ppsf):,}\n"
                f"Avg pools       = {round(self.avg_pools,2)}\n"
                f"Avg remod score = {round(self.avg_remod_score,1)}\n"
                )
    
    def compare_ranks(self,cmp_house: House) -> str:
        def find_rank(ordered_list: List[House]) -> int:
            for i,house in enumerate(ordered_list):
                if house.address == cmp_house.address:
                    return i+1
            return -1
        res = []
        res.append("\nHouse Rankings\nAfter values placed in Ascending Order\n")
        ordered = sorted(self.houses,key=lambda x: x.price)
        rank = find_rank(ordered)
        res.append(f"ZPrice   = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):<{HDC.RANK_W}}\n")

        ordered = sorted(self.houses,key=lambda x: x.sq_ft)
        rank = find_rank(ordered)
        res.append(f"sq ft    = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        ordered = sorted(self.houses,key=lambda x: x.ppsf)
        rank = find_rank(ordered)
        res.append(f"ZPPSF    = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")
        
        ordered = sorted(self.houses,key=lambda x: x.ppsf if x.address != cmp_house.address else x.for_sale_ppsf)
        rank = find_rank(ordered)
        res.append(f"SalePPSF = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        ordered = sorted(self.houses,key=lambda x: x.lot_size)
        rank = find_rank(ordered)
        res.append(f"Lot Sz   = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        ordered = sorted(self.houses,key=lambda x: x.remod_score)
        rank = find_rank(ordered)
        res.append(f"Remod Sc = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        return "".join(res)
    
    def compare_data(self,house: House) -> str:
        res = []
        diff = int(house.price - self.avg_price)
        res.append(f"Zprice - Avg Zprice     : {"+"if diff > 0 else ""}${diff:,}\n")

        diff = int(house.for_sale_price - self.avg_price)
        res.append(f"Sale P - Avg Zprice     : {"+"if diff > 0 else ""}${diff:,}\n")

        diff = int(house.sq_ft - self.avg_sq_ft)
        res.append(f"sqft - Avg sqft         : {"+" if diff > 0 else ""}{diff}\n")

        diff = round(house.beds - self.avg_beds, 1)
        res.append(f"beds - Avg beds         : {"+" if diff > 0 else ""}{diff}\n")

        diff = round(house.baths - self.avg_baths, 1)
        res.append(f"baths - Avg baths       : {"+" if diff > 0 else ""}{diff}\n")

        diff = int(house.ppsf - self.avg_ppsf)
        res.append(f"Zppsf - Avg Zppsf       : {"+" if diff > 0 else ""}${diff}\n")

        return "".join(res)
    
    def theoretical_prices_ppsf(self, sq_ft):
        res = []
        res.append(f"\nTheoretical prices based on PPSF from {int(self.min_ppsf)} to {int(self.max_ppsf)}\n")
        for curr_ppsf in range(int(self.min_ppsf),int(self.max_ppsf)+1):
            res.append(f"${curr_ppsf}," +
                f" sale price would be ${int(sq_ft * curr_ppsf):,}\n")
        return "".join(res)

    def visualize_price(self,compare_house: House):
        house_values = [house.price for house in self.houses]
        price_per_sqft = [house.ppsf for house in self.houses]
        highlight_value = compare_house.price

        # Sort the house values and corresponding price per square foot values
        sorted_indices = np.argsort(house_values)
        sorted_values = np.array(house_values)[sorted_indices]
        sorted_price_per_sqft = np.array(price_per_sqft)[sorted_indices]

        # Find the index of the value to highlight
        highlight_index = np.where(sorted_values == highlight_value)[0][0]

        # Create a color list where the highlight value is a different color
        colors = ['blue' if i != highlight_index else 'red' for i in range(len(sorted_values))]

        # Apply dark background style
        plt.style.use('dark_background')

        # Create subplots
        fig, axs = plt.subplots(3, 1, figsize=(10, 18))

        # Plot 1: House Value Ranking
        axs[0].bar(np.arange(len(sorted_values)), sorted_values, color=colors)
        axs[0].set_title('House Value Ranking')
        axs[0].set_xlabel('House')
        axs[0].set_ylabel('Value')
        axs[0].set_xticks(np.arange(len(sorted_values)))
        axs[0].set_xticklabels(np.arange(1, len(sorted_values) + 1))
        axs[0].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{int(x):,}'))

        # Plot 2: Price per Square Foot
        axs[1].scatter(sorted_price_per_sqft, sorted_values, color=colors)
        axs[1].set_title('Price per Square Foot vs House Value')
        axs[1].set_xlabel('Price per Square Foot')
        axs[1].set_ylabel('House Value')
        axs[1].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{int(x):,}'))

        # lets visualize the ppsf ranking
        vals = [house.ppsf for house in self.houses]
        sorted_indices = np.argsort(vals)
        sorted_values = np.array(vals)[sorted_indices]
        highlight_value = compare_house.ppsf
        highlight_index = np.where(sorted_values == highlight_value)[0][0]
        colors = ['blue' if i != highlight_index else 'red' for i in range(len(sorted_values))]
        axs[2].bar(np.arange(len(sorted_values)), sorted_values, color=colors)
        axs[2].set_title('House PPSF Ranking')
        axs[2].set_xlabel('PPSF Ranking')
        axs[2].set_ylabel('PPSF')
        axs[2].set_xticks(np.arange(len(sorted_values)))
        axs[2].set_xticklabels(np.arange(1, len(sorted_values) + 1))
        axs[2].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{int(x):,}'))


        # Save the plots to a PDF file
        pdf_filename = 'house_viz.pdf'
        with PdfPages(pdf_filename) as pdf:
            pdf.savefig(fig)
            plt.close()