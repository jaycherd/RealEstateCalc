from typing import Dict,Union,List,Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter

from utils.constants import HouseDataConstants as HDC
from models.house import House


class HouseData:
    def __init__(self, data: Union[Dict[str,House],List[House]], exclude : Optional[House] = None) -> None:
        # normalize incoming data
        if isinstance(data, dict):
            self.houses = list(data.values())
            self.houses_dict = data
        elif isinstance(data, list):
            self.houses = data
            self.houses_dict = {}
            for house in self.houses:
                self.houses_dict[house.address] = house
        else:
            raise ValueError("Houses should be either a dictionary or a list of House objects")

        sum_prices = sum_sq_ft = sum_beds = sum_baths = sum_ppsf = sum_pools = 0
        sum_sold_ppsf = sum_soldlist_diff = sum_remod_score = sum_sold_prices = 0
        num_sold = num_sold_n_listed = num_remodels = num_houses = 0

        for house in self.houses:
            if house.throw_out == 1 or (exclude is not None and house.address == exclude.address):
                continue
            sum_prices += house.price
            sum_sq_ft += house.sq_ft
            sum_beds += house.beds
            sum_baths += house.baths
            sum_ppsf += house.ppsf
            sum_pools += house.pool
            num_houses += 1
            if house.sold_ppsf != House.DEFAULT_INT:
                sum_sold_ppsf += house.sold_ppsf
                sum_sold_prices += house.sold_price
                num_sold += 1
            if house.sold_ppsf != House.DEFAULT_FLOAT and house.list_price != House.DEFAULT_FLOAT:
                sum_soldlist_diff += house.sold_price - house.list_price
                num_sold_n_listed += 1
            if house.remod_score != House.DEFAULT_INT:
                sum_remod_score += house.remod_score
                num_remodels += 1

        self.avg_price = sum_prices / num_houses if num_houses != 0 else 0
        self.avg_sold_price = sum_sold_prices / num_sold if num_sold != 0 else 0
        self.avg_sq_ft = sum_sq_ft / num_houses if num_houses != 0 else 0
        self.avg_beds = sum_beds / num_houses if num_houses != 0 else 0
        self.avg_baths = sum_baths / num_houses if num_houses != 0 else 0
        self.avg_ppsf = sum_ppsf / num_houses if num_houses != 0 else 0
        self.avg_pools = sum_pools / num_houses if num_houses != 0 else 0
        self.avg_sold_ppsf = sum_sold_ppsf / num_sold if num_sold != 0 else 0
        self.avg_soldlist_diff = sum_soldlist_diff / num_sold_n_listed if num_sold_n_listed != 0 else 0
        self.avg_remod_score = sum_remod_score / num_remodels if num_remodels != 0 else 0

    def __repr__(self):
        return (f"Note: not all sales have list price\n"
                f"Avg Zprice      = ${int(self.avg_price):,}\n"
                f"Avg Sold P      = ${int(self.avg_sold_price):,}\n"
                f"Avg sqft        = {int(self.avg_sq_ft)}\n"
                f"Avg beds        = {round(self.avg_beds,1)}\n"
                f"Avg baths       = {round(self.avg_baths,1)}\n"
                f"Avg ppsf        = ${int(self.avg_ppsf):,}\n"
                f"Avg SOLD PPSF   = ${int(self.avg_sold_ppsf):,}\n"
                f"Avg Sold - Lst  = ${int(self.avg_soldlist_diff):,}\n"
                f"Avg pools       = {round(self.avg_pools,2)}\n"
                f"Avg remod score = {round(self.avg_remod_score,1)}\n"
                )
    
    def compare_ranks(self,cmp_house: House) -> str:
        def find_rank(ordered_list: List[House]) -> int:
            for i,house in enumerate(ordered_list):
                if house.address == cmp_house.address:
                    return i
            return -1
        res = []
        res.append("\nHouse Rankings\n(ASC) = Ascending order rank, (DSC) = Descending order rank\n")
        ordered = sorted(self.houses,key=lambda x: x.price)
        rank = find_rank(ordered)
        res.append(f"(ASC) ZPrice   = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):<{HDC.RANK_W}}\n")

        ordered = sorted(self.houses,key=lambda x: (x.sold_price if x.address != cmp_house.address else x.price))
        rank = find_rank(ordered)
        res.append(f"(ASC) Sold P   = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        ordered = sorted(self.houses,key=lambda x: x.sq_ft)
        rank = find_rank(ordered)
        res.append(f"(ASC) sq ft    = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        ordered = sorted(self.houses,key=lambda x: x.ppsf)
        rank = find_rank(ordered)
        res.append(f"(ASC) PPSF     = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")
        
        ordered = sorted(self.houses,key=lambda x: x.sold_ppsf if x.address != cmp_house.address else x.ppsf)
        rank = find_rank(ordered)
        res.append(f"(ASC) Sold PPSF= {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        ordered = sorted(self.houses,key=lambda x: (x.list_price if x.address != cmp_house.address else x.price))
        rank = find_rank(ordered)
        res.append(f"(ASC) List P   = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        ordered = sorted(self.houses,key=lambda x: x.lot_size)
        rank = find_rank(ordered)
        res.append(f"(ASC) Lot Sz   = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        ordered = sorted(self.houses,key=lambda x: x.remod_score)
        rank = find_rank(ordered)
        res.append(f"(ASC) Remod Sc = {rank:{HDC.RANK_W}} of {len(ordered):{HDC.RANK_W}} = {round(rank/len(ordered),2):{HDC.RANK_W}}\n")

        return "".join(res)
    
    def compare_data(self,house: House) -> str:
        res = []
        diff = int(house.price - self.avg_price)
        res.append(f"Diff from Avg Zprice    : {"+"if diff > 0 else ""}${diff:,}")
        diff = int(house.price - self.avg_sold_price)
        res.append(f"Diff from Avg SOLD price: {"+"if diff > 0 else ""}${diff:,}")
        diff = int(house.sq_ft - self.avg_sq_ft)
        res.append(f"Diff from Avg sq ft     : {"+" if diff > 0 else ""}{diff}")
        diff = round(house.beds - self.avg_beds, 1)
        res.append(f"Diff from Avg beds      : {"+" if diff > 0 else ""}{diff}")
        diff = round(house.baths - self.avg_baths, 1)
        res.append(f"Diff from Avg baths     : {"+" if diff > 0 else ""}{diff}")
        diff = int(house.ppsf - self.avg_ppsf)
        res.append(f"Diff from Avg ppsf      : {"+" if diff > 0 else ""}${diff}")
        diff = int(house.ppsf - self.avg_sold_ppsf)
        res.append(f"Diff from Avg sold ppsf : {"+" if diff > 0 else ""}${diff}")
        return "\n".join(res)

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
        scatter = axs[1].scatter(sorted_price_per_sqft, sorted_values, color=colors)
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