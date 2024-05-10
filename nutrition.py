import enum

class Nutrition(enum.Enum):
    Calories = 'calories'
    Protein = 'protein'
    Fat = 'fat'
    Sodium = 'sodium'
    Fiber = 'fiber'
    Carbohydrate = 'carbo'
    Sugar = 'sugars'
    Potassium = 'potass'
    Vitamin = 'vitamins'

    def __getitem__(self, item):
        return self.value[item]