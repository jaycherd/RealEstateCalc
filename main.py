import json
import csv
import pathlib
from datetime import datetime
from typing import Dict

from models.house import House
from models.house_data import HouseData
from utils.constants import HomeKeys as HK



#pylint:disable=W0621
def analyze_data(data: Dict[str,House],for_sale_address,out_fname):
    house_data = HouseData(data=data)

    with open(out_fname, 'w', encoding="UTF-8") as f:
        f.write(f"Averages for this street:\n{house_data}")

        f.write("\nComparing these to the house we want to buy:\n")
        diff = int(data[for_sale_address].price - house_data.avg_price)
        f.write(f"Diff from Average price: {"+"if diff > 0 else ""}${diff:,}\n")
        diff = int(data[for_sale_address].sq_ft - house_data.avg_sq_ft)
        f.write(f"Diff from Average sq ft: {"+" if diff > 0 else ""}{diff}\n")
        diff = round(data[for_sale_address].beds - house_data.avg_beds, 1)
        f.write(f"Diff from Average beds : {"+" if diff > 0 else ""}{diff}\n")
        diff = round(data[for_sale_address].baths - house_data.avg_baths, 1)
        f.write(f"Diff from Average baths: {"+" if diff > 0 else ""}{diff}\n")
        diff = int(data[for_sale_address].ppsf - house_data.avg_ppsf)
        f.write(f"Diff from Average ppsf : {"+" if diff > 0 else ""}${diff}\n")

        house_data.visualize_price(data[for_sale_address])

        sorted_ppsf = sorted(
                            (house for _, house in data.items() if house.throw_out != 1),
                            key=lambda x: x.ppsf
                            )
        for_sale_ppsf_rank = -1
        for i,house in enumerate(sorted_ppsf):
            if house.address == for_sale_address:
                for_sale_ppsf_rank = i+1        
        f.write(f"The price per sq foot of the for sale house has ranking {for_sale_ppsf_rank} out of {len(sorted_ppsf)} houses\n")
        f.write("\nall the houses collected for this neighborhood ranked by price per square foot: \n")
        for house in sorted_ppsf:
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")
            f.write(f"{house}\n")
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")
            
        f.write("\nSome theoretical prices based on price per square foot\n")
        for i,house in enumerate(sorted_ppsf):
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")
            curr_ppsf = house.ppsf
            f.write(f"theoretical rank {i + 1} of {len(sorted_ppsf)}, if price per square foot was ${int(curr_ppsf)}," +
                f" sale price would be ${int(data[for_sale_address].sq_ft * curr_ppsf):,}\n")
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")

        recent_sales_sorted = sorted(
                            (house for _, house in data.items() if house.sold_date != house.DEFAULT_STR),
                            key=lambda x: (x.sold_date or datetime.max)
                            )
        recent_sales_sorted.reverse()
        f.write(f"\n{len(recent_sales_sorted)} recent sales:\n")
        for house in recent_sales_sorted:
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")
            f.write(f"{house}\n")
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")

        recent_sales_sorted_data = HouseData(recent_sales_sorted)
        f.write(f"\nAverages from the {len(recent_sales_sorted)} recent sales:\n{recent_sales_sorted_data}")

        f.write("\nComparing these recent sales to the house we want to buy:\n")
        diff = int(data[for_sale_address].price - recent_sales_sorted_data.avg_price)
        f.write(f"Diff from Avg price     : {"+"if diff > 0 else ""}${diff:,}\n")
        diff = int(data[for_sale_address].sq_ft - recent_sales_sorted_data.avg_sq_ft)
        f.write(f"Diff from Avg sq ft     : {"+" if diff > 0 else ""}{diff}\n")
        diff = round(data[for_sale_address].beds - recent_sales_sorted_data.avg_beds, 1)
        f.write(f"Diff from Avg beds      : {"+" if diff > 0 else ""}{diff}\n")
        diff = round(data[for_sale_address].baths - recent_sales_sorted_data.avg_baths, 1)
        f.write(f"Diff from Avg baths     : {"+" if diff > 0 else ""}{diff}\n")
        diff = int(data[for_sale_address].ppsf - recent_sales_sorted_data.avg_ppsf)
        f.write(f"Diff from Avg ppsf      : {"+" if diff > 0 else ""}${diff}\n")
        diff = int(data[for_sale_address].ppsf - recent_sales_sorted_data.avg_sold_ppsf)
        f.write(f"Diff from Avg sold ppsf : {"+" if diff > 0 else ""}${diff}\n")

        recent_sales_ppsf_asc = sorted((house for house in recent_sales_sorted),
                                       key=lambda x: x.sold_ppsf)
        f.write("\nRecent Sales ranked by ppsf in ascending order: \n")
        for house in recent_sales_ppsf_asc:
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")
            f.write(f"{house}\n")
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")

        f.write("\nSome theoretical prices based on price per square foot of Recent Sales\n")
        for i,house in enumerate(recent_sales_ppsf_asc):
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")
            curr_ppsf = house.sold_ppsf
            f.write(f"theoretical rank {i + 1} of {len(recent_sales_ppsf_asc)}, if price per square foot was ${int(curr_ppsf)}," +
                f" sale price would be ${int(data[for_sale_address].sq_ft * curr_ppsf):,}\n")
            if house.address == for_sale_address:
                f.write("*** for sale house ***\n")


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
                    except ValueError:
                        continue
            else:
                sold_date = HK.NA
            cleaned_address = row.get(HK.ADDRESS_KEY,"NA")
            if "," in cleaned_address:
                cleaned_address = cleaned_address.split(",")[0]
            house_data = {
                HK.ADDRESS_KEY: row.get(HK.ADDRESS_KEY, "NA"),
                HK.PRICE_KEY: float(row.get(HK.PRICE_KEY, -1.0)),
                HK.BEDS_KEY: float(row.get(HK.BEDS_KEY, -1.0)),
                HK.BATHS_KEY: float(row.get(HK.BATHS_KEY, -1.0)),
                HK.SQ_FT_KEY: float(row.get(HK.SQ_FT_KEY, -1.0)),
                HK.POOL_KEY: float(row.get(HK.POOL_KEY, -1.0)),
                HK.REMOD_SCORE_KEY: int(row.get(HK.REMOD_SCORE_KEY, -1)),
                HK.THROW_OUT_KEY: int(row.get(HK.THROW_OUT_KEY, -1)),
                HK.FOR_SALE_KEY: int(row.get(HK.FOR_SALE_KEY, -1)),
                HK.SOLD_PRICE_KEY: float(row.get(HK.SOLD_PRICE_KEY, -1.0)),
                HK.SOLD_DATE_KEY: sold_date,
                HK.LOT_SIZE_KEY: int(row.get(HK.LOT_SIZE_KEY, -1)),
                HK.LIST_PRICE_KEY: float(row.get(HK.LIST_PRICE_KEY,-1))
            }
            data_dict[cleaned_address] = House(**house_data)
    
    return data_dict




    


if __name__ == "__main__":
    current_dir = pathlib.Path(__file__).parent
    fname = current_dir / pathlib.Path("data/campbell_data_w_list.csv")
    out_fname = current_dir / pathlib.Path("output/campbell_out_data.txt")
    FOR_SALE_ADDRESS = "1250 Campbell Dr"


    data = csv_to_dict(file_path=fname)

    analyze_data(data,for_sale_address=FOR_SALE_ADDRESS,out_fname=out_fname)











