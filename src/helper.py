from pydantic import BaseModel, ValidationError, conlist, conint, constr

features = [
    ("Feature_A", 0.0, 1.0, 0.1),
    ("Feature_B", 0.0, 1.0, 0.1),
    ("Feature_C", 0.0, 1.0, 0.1),
    ("Feature_D", 0.0, 1.0, 0.1),
    ("Feature_E", 0.0, 1.0, 0.1),
    # ("Feature_X", ["Triangle", "Cercle", "Squarre"]),
    # ("Feature_Y", ["Apple", "Orange", "Bannane"]),
    # ("Feature_Z", ["Young", "Old"]),
]


class DataToPredict(BaseModel):
    Feature_A: float
    Feature_B: float
    Feature_C: float
    Feature_D: float
    Feature_E: float
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
        print(feat[0])
