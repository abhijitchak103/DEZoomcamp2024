import sys
import pandas as pd

print(sys.argv)

day = sys.argv[1]

df = pd.DataFrame(
    {
        'Column1': [1,2,3,4,5], 
        'Column2': ['A','B','C','D','E']
    }
)

print(f'...successfully created DataFrame: \n{df}\n\non day: {day}!')