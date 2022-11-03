import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def music_grades_merge():
    grades = pd.read_csv('grades_data.csv')
    musics = pd.read_csv('music_data.csv')
    # 데이터프레임을 출력했을때 더 많은 열이 보이도록 함
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 300)

    # movieId를 기준으로 ratings 와 movies 를 결합함
    music_ratings = pd.merge(grades, musics, on='music_id').sort_values(by='user_id', ascending=True)
    # user별로 영화에 부여한 rating 값을 볼 수 있도록 pivot table 사용
    title_user = music_ratings.pivot_table('grade', index='user_id', columns='music_id')
    # 평점을 부여안한 영화는 그냥 0이라고 부여
    title_user = title_user.fillna(0)
    print(title_user.head)

    return title_user

def collaborative_filtering(title_user):
    # 유저 1~610 번과 유저 1~610 번 간의 코사인 유사도를 구함
    user_based_collab = cosine_similarity(title_user, title_user)
    user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)
    
    csv_path = 'user_distance_data.csv'
    user_based_collab.to_csv(csv_path, index=False)
    return
    
##################################################
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