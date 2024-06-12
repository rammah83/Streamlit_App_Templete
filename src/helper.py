from pydantic import BaseModel, ValidationError, conlist, conint, constr

features = [
    ("Feature A", 0.0, 1.0, 0.1),
    ("Feature B", 0.0, 1.0, 0.1),
    ("Feature C", 0.0, 1.0, 0.1),
    ("Feature D", 0.0, 1.0, 0.1),
    ("Feature E", 0.0, 1.0, 0.1),
    ("Feature X", ["Triangle", "Cercle", "Squarre"]),
    ("Feature Y", ["Apple", "Orange", "Bannane"]),
    ("Feature Z", ["Young", "Old"]),
]


class Data(BaseModel):
    Feature_A: conlist(float, min_items=1)
    Feature_B: conlist(float, min_items=1)
    Feature_C: conlist(float, min_items=1)
    Feature_D: conlist(float, min_items=1)
    Feature_E: conlist(float, min_items=1)
    Feature_X: conlist(str, min_items=1)
    Feature_Y: conlist(str, min_items=1)
    Feature_Z: conlist(str, min_items=1)

if __name__ == "__main__":
    for feat in features:
        print(feat[0])
