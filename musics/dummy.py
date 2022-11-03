import datetime
import random
import pandas as pd

users_list = range(1,101)
musics_list = range(1,1451)
grade_list = [1,1.5,2,2.5,3,3.5,4,4.5,5]
created_at = datetime.datetime.now()

items_df = pd.DataFrame(columns=['user_id', 'music_id', 'grade', 'created_at'])
for user in users_list:
    for i in range(random.randrange(3,20)):
        user_id = user
        music_id = random.choice(musics_list)
        grade = random.choice(grade_list)
        created_at
        rating = [
                user_id,
                music_id,
                grade,
                created_at,]
        items_df.loc[len(items_df)] = rating

print(items_df.shape)
items_df.head()


csv_path = 'ratings_data.csv'
items_df.to_csv(csv_path, index=False)