import json
import csv
from datetime import datetime

from utils.constants import HomeKeys as HK



#pylint:disable=W0621
def analyze_data(data,for_sale_address,out_fname):
    sum_prices, sum_sq_ft, sum_beds, sum_baths, sum_ppsf = 0, 0, 0, 0, 0
    num_houses = 0

    for _ ,house in data.items():
        if house.get(HK.THROW_OUT_KEY) == 1:
            continue
        house[HK.PPSF_KEY] = round(house[HK.PRICE_KEY] / house[HK.SQ_FT_KEY], 0)
        sum_prices += house[HK.PRICE_KEY]
        sum_sq_ft += house[HK.SQ_FT_KEY]
        sum_beds += house[HK.BEDS_KEY]
        sum_baths += house[HK.BATHS_KEY]
        sum_ppsf += house[HK.PPSF_KEY]
        num_houses += 1

    avg_price = round(sum_prices / num_houses, 0)
    avg_sq_ft = round(sum_sq_ft / num_houses, 0)
    avg_beds = round(sum_beds / num_houses, 0)
    avg_baths = round(sum_baths / num_houses, 0)
    avg_ppsf = round(sum_ppsf / num_houses, 0)

    with open(out_fname, 'w') as f:
        f.write("Averages for this street:\n")
        f.write(f"Average price: {avg_price}\n")
        f.write(f"Average sq ft: {avg_sq_ft}\n")
        f.write(f"Average beds : {avg_beds}\n")
        f.write(f"Average baths: {avg_baths}\n")
        f.write(f"Average ppsf : {avg_ppsf}\n")

        f.write("\nComparing these to the house we want to buy:\n")
        f.write(f"Average price: {round(data[for_sale_address][HK.PRICE_KEY] - avg_price, 0)}\n")
        f.write(f"Average sq ft: {round(data[for_sale_address][HK.SQ_FT_KEY] - avg_sq_ft, 0)}\n")
        f.write(f"Average beds : {round(data[for_sale_address][HK.BEDS_KEY] - avg_beds, 0)}\n")
        f.write(f"Average baths: {round(data[for_sale_address][HK.BATHS_KEY] - avg_baths, 0)}\n")
        f.write(f"Average ppsf : {round(data[for_sale_address][HK.PPSF_KEY] - avg_ppsf, 0)}\n")

        sorted_items = sorted(
                            ((k, v) for k, v in data.items() if v.get('is_anomaly') != 1),
                            key=lambda x: x[1][HK.PPSF_KEY]
                            )
        for ppsf_lo2hi_rank, (key,entry) in enumerate(sorted_items, start=1):
            entry[HK.PPSF_RANK_KEY] = ppsf_lo2hi_rank
        sorted_data = {key: entry for key, entry in sorted_items}
        
        f.write(f"The price per sq foot of the for sale house has ranking {sorted_data[for_sale_address][HK.PPSF_RANK_KEY]} out of {len(sorted_data)} houses\n")

        f.write("\nThe houses with cheaper price per square foot are:\n")
        for id, house in sorted_data.items():
            if id == for_sale_address:
                break
            f.write(f"{house}\n")

        f.write("\nall the houses collected for this neighborhood ranked by price per square foot: \n")
        for id, house in sorted_data.items():
            f.write(f"{house}\n")
    
        f.write("\nSome theoretical prices based on houses with cheaper price per square foot\n")
        for id, house in sorted_data.items():
            if id == for_sale_address:
                break
            curr_ppsf = house[HK.PPSF_KEY]
            f.write(f"theoretical rank {house[HK.PPSF_RANK_KEY]} of {len(sorted_data)}, if price per square foot was {curr_ppsf}," +
                f" sale price would be {round(sorted_data[for_sale_address][HK.SQ_FT_KEY] * curr_ppsf , 0)}\n")
        
        f.write("\nIf we flip this house and raise the price per square foot to match the highest prices per square foot we'd get\n")
        sorted_items.reverse()  # Reverse the sorted list
        theoreticals_shown = 0
        for key, entry in sorted_items:
            if theoreticals_shown == 15:
                break
            curr_ppsf = entry[HK.PPSF_KEY]
            f.write(f"theoretical rank {entry[HK.PPSF_RANK_KEY]} of {len(sorted_items)}, if price per square foot was {curr_ppsf}, " +
                f"sale price would be {round(sorted_data[for_sale_address][HK.SQ_FT_KEY] * curr_ppsf, 0)}\n")
            theoreticals_shown += 1

        recent_sales = sorted(
                            ((k, v) for k, v in data.items()),
                            key=lambda x: (x[1][HK.SOLD_DATE_KEY] != HK.NA, x[1][HK.SOLD_DATE_KEY] or datetime.min)
                            )
        recent_sales.reverse()
        f.write(f"\nrecent sales:\n")
        for address,house_data in recent_sales:
            if house_data[HK.SOLD_DATE_KEY] == HK.NA:
                break
            f.write(f"{house_data}\n")

        

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
            primary_key = row[HK.ADDRESS_KEY]
            if row[HK.SOLD_PRICE_KEY] != '-1':
                sold_date = datetime.strptime(row[HK.SOLD_DATE_KEY], '%m/%d/%Y')
            else:
                sold_date = HK.NA
            data_dict[primary_key] = {
                HK.ADDRESS_KEY: row[HK.ADDRESS_KEY],
                HK.PRICE_KEY: float(row[HK.PRICE_KEY]),
                HK.BEDS_KEY: float(row[HK.BEDS_KEY]),
                HK.BATHS_KEY: float(row[HK.BATHS_KEY]),
                HK.SQ_FT_KEY: float(row[HK.SQ_FT_KEY]),
                HK.POOL_KEY: float(row[HK.POOL_KEY]),
                HK.REMOD_SCORE_KEY: int(row[HK.REMOD_SCORE_KEY]),
                HK.THROW_OUT_KEY: int(row[HK.THROW_OUT_KEY]),
                HK.FOR_SALE_KEY: int(row[HK.FOR_SALE_KEY]),
                HK.SOLD_PRICE_KEY: float(row[HK.SOLD_PRICE_KEY]),
                HK.SOLD_DATE_KEY: sold_date
            }
    
    return data_dict




    


if __name__ == "__main__":
    fname = "spanish_oaks_data.csv"
    out_fname = "spanish_oaks_out_data.csv"
    FOR_SALE_ADDRESS = "1901 Calle De Espana"

    data = csv_to_dict(file_path=fname)
    print(data)

    analyze_data(data,for_sale_address=FOR_SALE_ADDRESS,out_fname=out_fname)











