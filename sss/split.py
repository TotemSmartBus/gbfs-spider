import pandas as pd

root_path = r'C:\Users\12400\Desktop\水生所\底栖动物.csv'
root_name = r'C:\Users\12400\Desktop\水生所\底栖动物'
df = pd.read_csv(root_path, encoding='utf-8')
for i in range(1, 9):
    cols = [0, 1, 2, 2 + i, 10 + i]
    selected_df = df.iloc[:, cols]
    selected_df.to_csv(f'{root_name}_WuH_{i}.csv', index=False, encoding='utf-8')
    print(f'File {i} got')
