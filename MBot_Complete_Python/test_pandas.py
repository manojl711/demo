import pandas as pd

print('\nConcatenating Dataframes')
df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                    'B': ['B0', 'B1', 'B2', 'B3'],
                    'C': ['C0', 'C1', 'C2', 'C3'],
                    'D': ['D0', 'D1', 'D2', 'D3']},
                   index=[0, 1, 2, 3])

# Creating second dataframe
df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                    'B': ['B4', 'B5', 'B6', 'B7'],
                    'C': ['C4', 'C5', 'C6', 'C7'],
                    'D': ['D4', 'D5', 'D6', 'D7']},
                   index=[4, 5, 6, 7])

# Creating third dataframe
df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                    'B': ['B8', 'B9', 'B10', 'B11'],
                    'C': ['C8', 'C9', 'C10', 'C11'],
                    'D': ['D8', 'D9', 'D10', 'D11']},
                   index=[8, 9, 10, 11])

print(df1)
print(df2)
print(df3)

print('\nConcatenate dataframes')
print(pd.concat([df1, df2, df3]))

print('\nConcatenate same dataframes df1, 3 times')
print(pd.concat([df1, df1, df1]))

print('\nConcatenate same dataframes df1, duplicates removed')
print(pd.concat([df1, df1, df1]).drop_duplicates())

print('\nMerging Data frame')
left = pd.DataFrame({'Key': ['K0', 'K1', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
print(left)

right = pd.DataFrame({'Key': ['K0', 'K1', 'K2', 'K3'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
print(right)

print('\nInner Join - When both df has all Keys')
print(pd.merge(left, right, how='inner', on='Key'))

left = pd.DataFrame({'Key': ['K0', 'K1', 'K2', 'K3', 'K1'],
                     'A': ['A0', 'A1', 'A2', 'A3', 'C2'],
                     'B': ['B0', 'B1', 'B2', 'B3', 'C3']})
print(left)

right = pd.DataFrame({'Key': ['K0', 'K5', 'K2', 'K1'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
print(right)

print('\nInner Join - When both df has dissimilar Keys')
print(pd.merge(left, right, how='inner', on='Key'))

left = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3', 'A1'],
                     'B': ['B0', 'B1', 'B2', 'B3', 'B1']},
                    index=['K0', 'K1', 'K2', 'K3', 'K3'])

right = pd.DataFrame({'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']},
                     index=['K0', 'K1', 'K2', 'K3'])

print('\nRight Join')
print(left.join(right))
