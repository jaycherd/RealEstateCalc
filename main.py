import json

FOR_SALE_ID = "x"
PRICE_KEY = "price"
SQ_FT_KEY = "sq_ft"
BEDS_KEY = "beds"
BATHS_KEY = "baths"
PPSF_KEY = "price_per_sq_foot"
PPSF_RANK_KEY = "price_per_sq_foot_rank"


#pylint:disable=W0621
def analyze_street_data(data):
    sum_prices, sum_sq_ft, sum_beds, sum_baths, sum_ppsf = 0, 0, 0, 0, 0
    num_houses = 0

    for _ ,house in data.items():
        if house.get("is_anomaly") == 1:
            continue
        house[PPSF_KEY] = round(house[PRICE_KEY] / house[SQ_FT_KEY], 0)
        sum_prices += house[PRICE_KEY]
        sum_sq_ft += house[SQ_FT_KEY]
        sum_beds += house[BEDS_KEY]
        sum_baths += house[BATHS_KEY]
        sum_ppsf += house[PPSF_KEY]
        num_houses += 1

    avg_price = round(sum_prices / num_houses, 0)
    avg_sq_ft = round(sum_sq_ft / num_houses, 0)
    avg_beds = round(sum_beds / num_houses, 0)
    avg_baths = round(sum_baths / num_houses, 0)
    avg_ppsf = round(sum_ppsf / num_houses, 0)

    print("Averages for this street:")
    print(f"Average price: {avg_price}")
    print(f"Average sq ft: {avg_sq_ft}")
    print(f"Average beds : {avg_beds}")
    print(f"Average baths: {avg_baths}")
    print(f"Average ppsf : {avg_ppsf}")

    print("\nComparing these to the house we want to buy:")
    print(f"Average price: {round(data[FOR_SALE_ID][PRICE_KEY] - avg_price,0)}")
    print(f"Average sq ft: {round(data[FOR_SALE_ID][SQ_FT_KEY] - avg_sq_ft,0)}")
    print(f"Average beds : {round(data[FOR_SALE_ID][BEDS_KEY] - avg_beds,0)}")
    print(f"Average baths: {round(data[FOR_SALE_ID][BATHS_KEY] - avg_baths,0)}")
    print(f"Average ppsf : {round(data[FOR_SALE_ID][PPSF_KEY] - avg_ppsf,0)}")

    sorted_items = sorted(
                          ((k, v) for k, v in data.items() if v.get('is_anomaly') != 1),
                          key=lambda x: x[1][PPSF_KEY]
                         )
    for ppsf_lo2hi_rank, (key,entry) in enumerate(sorted_items, start=1):
        entry[PPSF_RANK_KEY] = ppsf_lo2hi_rank
    sorted_data = {key: entry for key, entry in sorted_items}
    
    print(f"The price per sq foot of the for sale house has ranking {sorted_data[FOR_SALE_ID][PPSF_RANK_KEY]} out of {len(sorted_data)} houses")

    print("\nThe houses with cheaper price per square foot are: ")
    for id, house in sorted_data.items():
        if id == FOR_SALE_ID:
            break
        print(house)
    
    print("\nSome theoretical prices based on houses with cheaper price per square foot")
    for id, house in sorted_data.items():
        if id == FOR_SALE_ID:
            break
        curr_ppsf = house[PPSF_KEY]
        print(f"theoretical rank {house[PPSF_RANK_KEY]} of {len(sorted_data)}, if price per square foot was {curr_ppsf}," +
              f" sale price would be {round(sorted_data[FOR_SALE_ID][SQ_FT_KEY] * curr_ppsf , 0)}")
        
    print("\nIf we flip this house and raise the price per square foot to match the highest price per square foot vals on this street we'd get")
    sorted_items.reverse()  # Reverse the sorted list
    theoreticals_shown = 0
    for key, entry in sorted_items:
        if theoreticals_shown == 10:
            break
        curr_ppsf = entry[PPSF_KEY]
        print(f"theoretical rank {entry[PPSF_RANK_KEY]} of {len(sorted_items)}, if price per square foot was {curr_ppsf}, " +
            f"sale price would be {round(sorted_data[FOR_SALE_ID][SQ_FT_KEY] * curr_ppsf, 0)}")
        theoreticals_shown += 1




    



# Load the JSON data from the file
with open('street_vals.json', 'r',encoding="UTF-8") as json_file:
    entries_list = json.load(json_file)

# Convert the list of dictionaries to a dictionary with `id` as keys
street_houses_dict = {entry['id']: entry for entry in entries_list}
print(street_houses_dict)





analyze_street_data(data=street_houses_dict)











