import datetime
import random
import pandas as pd
from csv import DictWriter

users_list = range(1,101)
musics_list = range(1,1451)
grade_list = [1,1.5,2,2.5,3,3.5,4,4.5,5]
created_at = datetime.datetime.now()
def save_grades_data_csv():
        items_df = pd.DataFrame(columns=['user_id', 'music_id', 'grade', 'created_at'])
        for user in users_list:
                for i in range(random.randrange(10,20)):
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

        items_df.head()
        
        csv_path = 'data/grades_data.csv'
        items_df.to_csv(csv_path, index=False)

# 리뷰가 남을때마다, grades_data.csv에 행추가해주는 함수.
def grade_to_csv(grades_data):
    with open('data/grades_data.csv', 'a', newline='') as csv_file:
            headers = ['user_id', 'music_id', 'grade', 'created_at']
            write_data = DictWriter(csv_file, fieldnames=headers)
            write_data.writerow(grades_data)
            csv_file.close()