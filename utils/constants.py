from pathlib import Path

class PathConstants:
    parent_dir = Path(__file__).parent.parent
    SQFT_VIZ = parent_dir / "output/visuals/sqft_visual.pdf"
    HOUSE_VIZ = parent_dir / "output/visuals/house_visual.pdf"


class HomeKeys:
    ID_KEY = "id"
    ADDRESS_KEY = "address"
    PRICE_KEY = "price"
    SQ_FT_KEY = "sq_ft"
    BEDS_KEY = "beds"
    BATHS_KEY = "baths"
    POOL_KEY = "pool"
    REMOD_SCORE_KEY = "subj_remodel_score"
    THROW_OUT_KEY = "throw_out"
    FOR_SALE_KEY = "for_sale"
    FOR_SALE_PRICE_KEY = "for_sale_price"
    SOLD_PRICE_KEY = "sold_price"
    SOLD_DATE_KEY = "sold_date"
    LOT_SIZE_KEY = "lot_size"
    LIST_PRICE_KEY = "list_price"
    PPSF_KEY = "price_per_sq_foot"
    PPSF_RANK_KEY = "price_per_sq_foot_rank"

class HouseDataConstants:
    RANK_W = 3

