import json
import csv
import pathlib
from datetime import datetime
from typing import Dict

from models.house import House
from models.house_data import HouseData
from models.recent_sale_data import RecentSaleData
from models.sim_sqft_data import SimSqftData
from utils.constants import HomeKeys as HK



#pylint:disable=W0621
def analyze_data(data: Dict[str,House],for_sale_address,out_fname):
    house_data = HouseData(houses=[house for _,house in data.items()])
    # house_data.compute_avgs()

    with open(out_fname, 'w', encoding="UTF-8") as f:
        f.write(f"Averages for this street:\n{house_data.get_avgs_str()}")
        f.write("\nComparing these averages to the house we want to buy:\n")
        f.write(f"{house_data.compare_data(data[for_sale_address])}\n")
        f.write(house_data.compare_ranks(data[for_sale_address]))

        house_data.visualize_price(data[for_sale_address])

        sorted_ppsf = sorted(
                            (house for _, house in data.items() if house.throw_out != 1),
                            key=lambda x: x.ppsf
                            )
        f.write("\nall the houses collected for this neighborhood "
                "ranked by price per square foot: \n")
        for house in sorted_ppsf:
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")
            f.write(f"{house}\n")
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")

        f.write(f"{house_data.theoretical_prices_ppsf(data[for_sale_address].sq_ft)}")

        recent_sales_sorted = sorted(
                            (house for _, house in data.items() if house.sold_date != House.NA),
                            key=lambda x: (x.sold_date or datetime.max)
                            )
        recent_sales_sorted.reverse()
        start_months = 18
        previous_num_sold = curr_num_sold = None
        for num_months in range(start_months,-1,-1):
            recent_sales_sorted_data = RecentSaleData(recent_sales_sorted + [data[for_sale_address]],
                                                      exclude=data[for_sale_address], months=num_months)
            curr_num_sold = len(recent_sales_sorted_data.houses)
            if previous_num_sold is None:
                previous_num_sold = curr_num_sold
                continue
            if curr_num_sold == previous_num_sold:
                continue
            previous_num_sold = curr_num_sold
            recent_sales_sorted_data = RecentSaleData(recent_sales_sorted + [data[for_sale_address]],
                                                      exclude=data[for_sale_address], months=num_months+1)
            # recent_sales_sorted_data.compute_avgs()
            f.write(f"\n{len(recent_sales_sorted_data.houses)} sales within {num_months+1} months:\n")
            for house in recent_sales_sorted_data.houses:
                if house.address == for_sale_address:
                    f.write("*** for sale house ***\n")
                f.write(f"{house}\n")
                if house.address == for_sale_address:
                    f.write("*** for sale house ***\n")
            f.write(f"\n{recent_sales_sorted_data.get_avgs_str()}")
            f.write("\nComparing these recent sales to the house we want to buy:\n")
            f.write(f"{recent_sales_sorted_data.compare_data(data[for_sale_address])}\n")
            f.write(recent_sales_sorted_data.compare_ranks(data[for_sale_address]))

        subjective_scores_desc = sorted(
                                        (house for _, house in data.items()),
                                        key=lambda x: x.remod_score
                                        )
        subjective_scores_desc.reverse()
        f.write("\nranked subjectively descending order:\n")
        for house in subjective_scores_desc:
            if house.remod_score == -1:
                break
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")
            f.write(f"{house}\n")
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")

        max_sqft_diff = 90
        sim_sqft_data = SimSqftData(houses=[house for _,house in data.items()],
                                    cmp_house=data[for_sale_address],max_diff=max_sqft_diff)
        f.write(f"\nAverages from {len(sim_sqft_data.houses)} houses within {max_sqft_diff}"
                f" sqft:\n{sim_sqft_data.get_avgs_str()}")
        f.write("\nComparing these to the house we want to buy:\n")
        f.write(f"{sim_sqft_data.compare_data(data[for_sale_address])}\n")
        f.write(sim_sqft_data.compare_ranks(data[for_sale_address]))
        f.write(f"\nHouses within {max_sqft_diff} sq ft")
        for house in sim_sqft_data.houses:
            f.write(f"\n{house}")
        sim_sqft_data.visualize(compare_house=data[for_sale_address])


def json_to_dict(file_path):
    # Load the JSON data from the file
    with open(file_path, 'r',encoding="UTF-8") as json_file:
        entries_list = json.load(json_file)

    # Convert the list of dictionaries to a dictionary with `id` as keys
    res = {entry['id']: entry for entry in entries_list}
    return res

def csv_to_dict(file_path):
    data_dict = {}

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row[HK.THROW_OUT_KEY] == '1':
                continue
            if row[HK.SOLD_PRICE_KEY] != '-1':
                for date_format in ('%m/%d/%Y', '%m/%d/%y'):
                    try:
                        sold_date = datetime.strptime(row[HK.SOLD_DATE_KEY], date_format)
                        row[HK.SOLD_DATE_KEY] = sold_date
                    except ValueError:
                        continue
            else:
                sold_date = House.NA

            cleaned_address = row.get(HK.ADDRESS_KEY,"NA")
            if "," in cleaned_address:
                cleaned_address = cleaned_address.split(",")[0]
            data_dict[cleaned_address] = House(**row)

    return data_dict


if __name__ == "__main__":
    current_dir = pathlib.Path(__file__).parent
    fname = current_dir / pathlib.Path("data/bharborcomps.csv")
    out_fname = current_dir / pathlib.Path("output/bharbor.txt")
    FOR_SALE_ADDRESS = "8104 Bay Harbor Dr"

    data = csv_to_dict(file_path=fname)

    analyze_data(data,for_sale_address=FOR_SALE_ADDRESS,out_fname=out_fname)











