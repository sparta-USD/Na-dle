import pandas as pd
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


def recommend_users(user_id):
    """
    유저와 비슷한 취향을 가진 사람들을 추려주는 함수입니다.

    Args:
        user_id (int): 현재 user의 id가 parameter로 사용됩니다.

    Returns:
        유저의 id값들이 리스트형태로 리턴됩니다.
        e.g) [2, 25, 66, 24, 91]
    """
    music_user = music_grades_merge()
    user_based_collab = cosine_similarity(music_user, music_user)
    user_based_collab = pd.DataFrame(user_based_collab, index=music_user.index, columns=music_user.index) # numpy행렬 -> pandas DataFrame

    # user_id번 유저와 비슷한 유저를 내림차순으로 정렬한 후에, 상위 5개만 뽑음
    similar_users = user_based_collab[user_id].sort_values(ascending=False)[1:6] # 본인을 제외하기 위해 인덱스 1~6까지
    similar_users_dict = similar_users.to_dict()

    return list(similar_users_dict.keys())


def recommend_musics(user_id):
    # 유저와 비슷한 취향의 유저의 평점을 작성한 음원 출력
    music_grades = music_grades_merge() #title_user
    user_based_collab = pd.read_csv('user_distance_data.csv')
    user_based_collab.index=music_grades.index
    user_based_collab.columns=music_grades.index

    # # # 1번 유저와 가장 비슷한 유저를 뽑고,
    user = user_based_collab[1].sort_values(ascending=False)[:10].index[1]
    # # # 유저가 좋아했던 음악를 평점 내림차순으로 출력
    result_pd = music_grades.query(f"user_id == {user}").sort_values(ascending=False, by=user, axis=1)
    result_dict = result_pd.to_dict()
    result = []

    for key in result_dict:
        if(result_dict[key][80]>0):
            # result.append({
            #     "music_id":key,
            #     "grade":result_dict[key][80]
            # })
            
            result.append(key)
    return result
# print(recommend_musics(1))
