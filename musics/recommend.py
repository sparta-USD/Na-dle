import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def music_grades_merge():
    grades = pd.read_csv('grades_data.csv')
    musics = pd.read_csv('music_data.csv')
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 300)

    # grades, musics 결합
    music_ratings = pd.merge(grades, musics, on='music_id').sort_values(by='user_id', ascending=True)
    title_user = music_ratings.pivot_table('grade', index='user_id', columns='music_id')
    title_user = title_user.fillna(0)

    return title_user

def collaborative_filtering(title_user):
    #코사인 유사도
    user_based_collab = cosine_similarity(title_user, title_user)
    user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)
    
    csv_path = 'user_distance_data.csv'
    user_based_collab.to_csv(csv_path, index=False)



def func01():
    # 1번 유저와 비슷한 유저를 내림차순으로 정렬한 후에, 상위 5개만 뽑음
    print(user_based_collab[2].sort_values(ascending=False)[:10])

    

def recommend_musics(user_id):
    # 유저와 비슷한 취향의 유저의 평점을 작성한 음원 출력
    music_grades = music_grades_merge() #title_user
    user_based_collab = pd.read_csv('user_distance_data.csv')
    user_based_collab.index=music_grades.index
    user_based_collab.columns=music_grades.index

    # # # 1번 유저와 가장 비슷한 266번 유저를 뽑고,
    user = user_based_collab[1].sort_values(ascending=False)[:10].index[1]
    # # # 266번 유저가 좋아했던 음악를 평점 내림차순으로 출력
    result_pd = music_grades.query(f"user_id == {user}").sort_values(ascending=False, by=user, axis=1)
    result_dict = result_pd.to_dict()
    result = []

    for key in result_dict:
        if(result_dict[key][80]>0):
            result.append({
                "music_id":key,
                "grade":result_dict[key][80]
            })
    return result