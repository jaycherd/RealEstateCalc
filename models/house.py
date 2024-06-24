from datetime import datetime

from utils.constants import HomeKeys as HK
from utils.constants import HouseConstants as HC

class House:
    #class vars
    DEFAULT_FLOAT = -1.0
    DEFAULT_INT = -1
    DEFAULT_STR = "NA"

    def __init__(self, **kwargs) -> None:
        cleaned_address = kwargs.get(HK.ADDRESS_KEY, 'N/A')
        if "," in cleaned_address:
            cleaned_address = cleaned_address.split(",")[0]
        self.address = cleaned_address
        self.price = float(kwargs.get(HK.PRICE_KEY, House.DEFAULT_FLOAT))
        self.beds = float(kwargs.get(HK.BEDS_KEY, House.DEFAULT_FLOAT))
        self.baths = float(kwargs.get(HK.BATHS_KEY, House.DEFAULT_FLOAT))
        self.sq_ft = float(kwargs.get(HK.SQ_FT_KEY, House.DEFAULT_FLOAT))
        self.pool = float(kwargs.get(HK.POOL_KEY, House.DEFAULT_FLOAT))
        self.remod_score = int(kwargs.get(HK.REMOD_SCORE_KEY, House.DEFAULT_INT))
        self.throw_out = int(kwargs.get(HK.THROW_OUT_KEY, House.DEFAULT_INT))
        self.for_sale = int(kwargs.get(HK.FOR_SALE_KEY, House.DEFAULT_INT))
        self.sold_price = float(kwargs.get(HK.SOLD_PRICE_KEY, House.DEFAULT_FLOAT))
        self.list_price = float(kwargs.get(HK.LIST_PRICE_KEY, House.DEFAULT_FLOAT))
        self.for_sale_price = float(kwargs.get(HK.FOR_SALE_PRICE_KEY, House.DEFAULT_FLOAT))
        self.sold_date = kwargs.get(HK.SOLD_DATE_KEY, House.DEFAULT_STR)
        self.sold_date_fmt = House.DEFAULT_STR
        if isinstance(self.sold_date, datetime):
            self.sold_date_fmt = self.sold_date.strftime("%m/%d/%Y")
        self.lot_size = int(kwargs.get(HK.LOT_SIZE_KEY, House.DEFAULT_INT))
        self.ppsf = self.price / self.sq_ft
        if self.sold_price == House.DEFAULT_FLOAT:
            self.sold_ppsf = House.DEFAULT_INT
            self.list_ppsf = House.DEFAULT_INT
        else:
            self.sold_ppsf = self.sold_price / self.sq_ft
            self.list_ppsf = self.list_price / self.sq_ft
        if self.list_price == House.DEFAULT_FLOAT:
            self.list_ppsf = House.DEFAULT_INT
        else:
            self.list_ppsf = self.list_price / self.sq_ft

        self.tmp = kwargs.get("notakey","NONE")

    def __repr__(self):
        remod_str = f"{HC.SEP}remod_score={self.remod_score}" if self.remod_score != House.DEFAULT_INT else ""
        sold_p_str = f"{HC.SEP}sold_price=${int(self.sold_price):,}" if self.sold_price != House.DEFAULT_FLOAT else ""
        list_price_str = f"{HC.SEP}list_price=${int(self.list_price):,}" if self.list_price != House.DEFAULT_FLOAT else ""
        for_sale_price_str = f"{HC.SEP}sale_price=${int(self.for_sale_price):,}" if self.for_sale_price != House.DEFAULT_FLOAT else ""
        sold_ppsf_str = f"{HC.SEP}sold_ppsf=${int(self.sold_ppsf):,}" if self.sold_ppsf != House.DEFAULT_INT else ""
        list_ppsf_str = f"{HC.SEP}list_ppsf=${int(self.list_ppsf):,}" if self.list_ppsf != House.DEFAULT_INT else ""
        sold_date_str = f"{HC.SEP}sold_date={self.sold_date_fmt}" if self.sold_date != House.DEFAULT_STR else ""
        return (f"[addrs={self.address}{HC.SEP}price=${int(self.price):,}{HC.SEP}bd={int(self.beds)}{HC.SEP}"
                f"ba={int(self.baths)}{HC.SEP}sqft={int(self.sq_ft)}{HC.SEP}ppsf=${int(self.ppsf):,}{HC.SEP}pool={int(self.pool)}{HC.SEP}"
                f"lot_size={self.lot_size}{remod_str}{sold_p_str}{list_price_str}{for_sale_price_str}{sold_ppsf_str}"
                f"{list_ppsf_str}{sold_date_str} ]")

    def show_all_vals(self):
        return (f"[address={self.address}{HC.SEP}price=${int(self.price):,}{HC.SEP}beds={int(self.beds)}{HC.SEP}"
                f"baths={int(self.baths)}{HC.SEP}sq_ft={int(self.sq_ft)}{HC.SEP}ppsf=${int(self.ppsf):,}{HC.SEP}pool={int(self.pool)}{HC.SEP}"
                f"remod_score={self.remod_score}{HC.SEP}throw_out={self.throw_out}{HC.SEP}"
                f"for_sale={self.for_sale}{HC.SEP}sold_price=${int(self.sold_price):,}{HC.SEP}"
                f"sold_date={self.sold_date_fmt}{HC.SEP}lot_size={self.lot_size}]")