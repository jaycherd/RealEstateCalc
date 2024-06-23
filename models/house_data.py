from typing import Dict,Union,List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter

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

        sum_prices = sum_sq_ft = sum_beds = sum_baths = sum_ppsf = sum_pools = 0
        sum_sold_ppsf = sum_soldlist_diff = 0
        num_houses = len(self.houses)
        num_sold = 0

        for house in self.houses:
            if house.throw_out == 1:
                continue
            sum_prices += house.price
            sum_sq_ft += house.sq_ft
            sum_beds += house.beds
            sum_baths += house.baths
            sum_ppsf += house.ppsf
            sum_pools += house.pool
            if house.sold_ppsf != House.DEFAULT_FLOAT:
                sum_sold_ppsf += house.sold_ppsf
                sum_soldlist_diff += house.sold_price - house.list_price
                num_sold += 1

        self.avg_price = sum_prices / num_houses
        self.avg_sq_ft = sum_sq_ft / num_houses
        self.avg_beds = sum_beds / num_houses
        self.avg_baths = sum_baths / num_houses
        self.avg_ppsf = sum_ppsf / num_houses
        self.avg_pools = sum_pools / num_houses
        self.avg_sold_ppsf = sum_sold_ppsf / num_sold
        self.avg_soldlist_diff = sum_soldlist_diff / num_sold

    def __repr__(self):
        return (f"Avg price = ${int(self.avg_price):,}\n"
                f"Avg sqft  = {int(self.avg_sq_ft)}\n"
                f"Avg beds  = {round(self.avg_beds,1)}\n"
                f"Avg baths = {round(self.avg_baths,1)}\n"
                f"Avg ppsf  = ${int(self.avg_ppsf):,}\n"
                f"Avg sold ppsf = ${int(self.avg_sold_ppsf):,}\n"
                f"Avg sold - list price = ${int(self.avg_soldlist_diff):,}\n"
                f"Avg pools = {round(self.avg_pools,2)}\n"
                )

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