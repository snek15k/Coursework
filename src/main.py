import pandas as pd
import os
from src.services import get_personal_transfers



all_operations = pd.read_excel(os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx"))
all_operations_list_dict = all_operations.to_dict(orient='records')

print(get_personal_transfers(all_operations_list_dict))
