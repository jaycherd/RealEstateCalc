from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter

from models.house import House
from models.house_data import HouseData
from utils.constants import PathConstants as PthC

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
        
    def visualize(self,compare_house: House):
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
        pdf_filename = PthC.SQFT_VIZ
        with PdfPages(pdf_filename) as pdf:
            pdf.savefig(fig)
            plt.close()

