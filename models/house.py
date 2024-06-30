from datetime import datetime

from utils.constants import HomeKeys as HK

class House:
    #class vars
    SEP = " | "
    NA = "NA"

    def __init__(self, **kwargs) -> None:
        def convert_value(value):
            try:
                return float(value) # the string converted to a float
            except (ValueError, TypeError): # ValueError(is string), FloatError(is None bcs key not exists)
                return value # should be the original string
        def get_value(kwargs, key):
            value = convert_value(kwargs.get(key))
            return value if value is not None else House.NA
        def get_bool_val(kwargs, key):
            value = kwargs.get(key)
            return False if (value is None or value == 0 or value == "0") else True

        cleaned_address = kwargs.get(HK.ADDRESS_KEY, House.NA)
        if "," in cleaned_address:
            cleaned_address = cleaned_address.split(",")[0]
        self.address = cleaned_address

        self.price = get_value(kwargs,HK.PRICE_KEY)
        self.beds = get_value(kwargs,HK.BEDS_KEY)
        self.baths = get_value(kwargs,HK.BATHS_KEY)
        self.sq_ft = get_value(kwargs,HK.SQ_FT_KEY)
        self.lot_size = get_value(kwargs,HK.LOT_SIZE_KEY)
        self.pool = get_value(kwargs,HK.POOL_KEY)
        self.remod_score = get_value(kwargs,HK.REMOD_SCORE_KEY)
        self.throw_out = get_bool_val(kwargs,HK.THROW_OUT_KEY)
        self.for_sale = get_bool_val(kwargs,HK.FOR_SALE_KEY)
        self.sold_price = get_value(kwargs,HK.SOLD_PRICE_KEY)
        self.list_price = get_value(kwargs,HK.LIST_PRICE_KEY)
        self.for_sale_price = get_value(kwargs,HK.FOR_SALE_PRICE_KEY)
        self.sold_date = get_value(kwargs,HK.SOLD_DATE_KEY)

        self.sold_date_fmt = House.NA
        if isinstance(self.sold_date, datetime):
            self.sold_date_fmt = self.sold_date.strftime("%m/%d/%Y")

        self.ppsf = (self.price / self.sq_ft) if (self.price != House.NA and self.sq_ft != House.NA) else House.NA
        self.sold_ppsf = (self.sold_price / self.sq_ft) if (self.sold_price != House.NA and self.sq_ft != House.NA) else House.NA
        self.list_ppsf = (self.list_price / self.sq_ft) if (self.list_price != House.NA and self.sq_ft != House.NA) else House.NA
        self.for_sale_ppsf = (self.for_sale_price / self.sq_ft) if (self.for_sale_price != House.NA and self.sq_ft != House.NA) else House.NA


    def __repr__(self):
        remod_str = f"{House.SEP}remod_score={self.remod_score}" if self.remod_score != House.NA else ""
        sold_p_str = f"{House.SEP}sold_price=${int(self.sold_price):,}" if self.sold_price != House.NA else ""
        list_price_str = f"{House.SEP}list_price=${int(self.list_price):,}" if self.list_price != House.NA else ""
        for_sale_price_str = f"{House.SEP}sale_price=${int(self.for_sale_price):,}" if self.for_sale_price != House.NA else ""
        sold_ppsf_str = f"{House.SEP}sold_ppsf=${int(self.sold_ppsf):,}" if self.sold_ppsf != House.NA else ""
        list_ppsf_str = f"{House.SEP}list_ppsf=${int(self.list_ppsf):,}" if self.list_ppsf != House.NA else ""
        fs_ppsf_str = f"{House.SEP}for_sale_ppsf=${int(self.for_sale_ppsf):,}" if self.for_sale_ppsf != House.NA else ""
        sold_date_str = f"{House.SEP}sold_date={self.sold_date_fmt}" if self.sold_date != House.NA else ""
        return (f"[addrs={self.address}{House.SEP}Zprice=${int(self.price):,}{House.SEP}bd={int(self.beds)}{House.SEP}"
                f"ba={int(self.baths)}{House.SEP}sqft={int(self.sq_ft)}{House.SEP}Zppsf=${int(self.ppsf):,}{House.SEP}pool={int(self.pool)}{House.SEP}"
                f"lot_size={self.lot_size}{remod_str}{sold_p_str}{list_price_str}{for_sale_price_str}{fs_ppsf_str}{sold_ppsf_str}"
                f"{list_ppsf_str}{sold_date_str} ]")

    def show_all_vals(self):
        return (f"[address={self.address}{House.SEP}price=${int(self.price):,}{House.SEP}beds={int(self.beds)}{House.SEP}"
                f"baths={int(self.baths)}{House.SEP}sq_ft={int(self.sq_ft)}{House.SEP}ppsf=${int(self.ppsf):,}{House.SEP}pool={int(self.pool)}{House.SEP}"
                f"remod_score={self.remod_score}{House.SEP}throw_out={self.throw_out}{House.SEP}"
                f"for_sale={self.for_sale}{House.SEP}sold_price=${int(self.sold_price):,}{House.SEP}"
                f"sold_date={self.sold_date_fmt}{House.SEP}lot_size={self.lot_size}]")