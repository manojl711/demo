import pandas as pd

# concat_master_df = pd.read_csv('concat_master.csv')
# concat_daily_df = pd.read_csv('concat_daily.csv')
#
# print('\nconcat_master_df = ', concat_master_df.shape)
# print('\n', concat_master_df.dtypes)
# print(concat_master_df.to_string())
#
# print('\nconcat_daily_df = ', concat_daily_df.shape)
# print('\n', concat_daily_df.dtypes)
# print(concat_daily_df.to_string())
#
# set_diff_df = pd.concat([concat_master_df, concat_daily_df, concat_master_df], sort=True).drop_duplicates(keep=False)
# print('\nset_diff_df = ', set_diff_df.shape)
# print('\n', set_diff_df.dtypes)
# print(set_diff_df.to_string())
#
# # This is kinda working (A-B)
# set_diff2_df = concat_master_df.merge(concat_daily_df, indicator=True, how="left")[
#     lambda x: x._merge == 'left_only'].drop('_merge', 1)
# print('\nset_diff2_df = ', set_diff2_df.shape)
# print('\n', set_diff2_df.dtypes)
# print(set_diff2_df.to_string())
#
# new_df = concat_daily_df.combine_first(concat_master_df)
# print('\nnew_df = ', new_df.shape)
# print('\n', new_df.dtypes)
# print(new_df.to_string())
#
# # df[['b1', 'b2']] = df[['b1', 'b2']].where(df[['b1', 'b2']] != '', df[['a1', 'a2']].values)


# Dataframe Comparision
dataA = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake'],
         'last_name': ['Miller', 'Jacobson', 'Ali', 'Milner'],
         'age': [42, 50, 36, 24],
         'preTestScore': [4, 24, 31, 2],
         'postTestScore': [25, 94, 57, 62]}
dataB = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
         'last_name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze'],
         'age': [42, 52, 36, 24, 73],
         'preTestScore': [4, 24, 31, 2, 3],
         'postTestScore': [25, 94, 57, 62, 70]}

dfA = pd.DataFrame(dataA, columns=['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
dfB = pd.DataFrame(dataB, columns=['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])

print('\ndfA')
print(dfA.to_string())
print('\ndfB')
print(dfB.to_string())

# left_on=['first_name','last_name'],right_on=['first_name','last_name']
new_df = dfA.merge(dfB, indicator=True, how="left", )[
    lambda x: x._merge == 'left_only'].drop('_merge', 1)
print('\nnew_df')
print(new_df.to_string())

r_new_df = \
dfB.merge(dfA, indicator=True, how="left", left_on=['first_name', 'last_name'], right_on=['first_name', 'last_name'])[
    lambda x: x._merge == 'left_only'].drop('_merge', 1)
print('\nr_new_df')
print(r_new_df.to_string())

# i_new_df = dfA.merge(dfB, indicator=True, how="inner", left_on=['first_name','last_name'],right_on=['first_name','last_name'])[
#     lambda x: x._merge == 'left_only'].drop('_merge', 1)
# print('\ni_new_df')
# print(i_new_df.to_string())
