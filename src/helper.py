from pydantic import BaseModel, ValidationError, conlist, conint, constr

models = {
    "model01": "./res/models/model01.pkl",
    "model02": "./res/models/model02.pkl",
    "model03": "./res/models/model03.pkl",
    "model04": "./res/models/model04.joblib",
}

features: dict = {
    "NUM1": (0.0, 100.0, 10.0),
    "no_usefull_NUM": (0.0, 100.0, 50.0),
    "NUM3": (0.0, 100.0, 20.0),
    "with_MISS": (0.0, 10.0, 1.0),
    "cor_NUM": (0.0, 200.0, 100.0),
    # "weakcor_NUM": (0.0, 1.0, 200.0),
    # "strongcor_NUM": (0.0, 1.0, 200.0),
    # "CAT1": ["A", "B", "C"],
    # "CORR2_CAT1": ["AAA", "BBB", "CCC", "ABD"],
    # "no_usefull_CAT": ["KK", "LL", "MM"],
    # "CORR_CAT3": ["SS", "TT", "UU"],
}


class DataToPredict(BaseModel):
    NUM1: float
    no_usefull_NUM: float
    NUM3: float
    with_MISS: float
    cor_NUM: float
    # weakcor_NUM: float
    # strongcor_NUM: float
    # CAT1: str
    # CORR2_CAT1: str
    # no_usefull_CAT: str
    # CORR_CAT3: str

    # Feature_A: conlist(float, min_items=1)
    # Feature_B: conlist(float, min_items=1)
    # Feature_C: conlist(float, min_items=1)
    # Feature_D: conlist(float, min_items=1)
    # Feature_E: conlist(float, min_items=1)
    # Feature_X: conlist(str, min_items=1)
    # Feature_Y: conlist(str, min_items=1)
    # Feature_Z: conlist(str, min_items=1)


if __name__ == "__main__":
    for feat in features:
        print(feat)
