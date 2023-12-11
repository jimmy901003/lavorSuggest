import math
import numpy as np
from restaurants import restaurants
from users import user_1_location, user_1_tags

# 權重變數
WEIGHT_DISH = 0.9
WEIGHT_DISTANCE = 0.1

def calculate_dish_similarity(user_tags, dish_tags):
    intersection_len = len(set(user_tags) & set(dish_tags))
    union_len = len(set(user_tags) | set(dish_tags))
    similarity = intersection_len / union_len if union_len != 0 else 0
    return similarity

def calculate_distance_score(user_location, restaurant_location):
    user_lat, user_lon = user_location
    restaurant_lat, restaurant_lon = restaurant_location
    distance = np.linalg.norm(np.array([user_lat, user_lon]) - np.array([restaurant_lat, restaurant_lon]))
    distance_score = 1 / (1 + distance)
    return distance_score

def recommend_restaurants(user_location, user_tags, restaurants):
    scores = []

    for restaurant in restaurants:
        # 計算菜品相似性分數
        dish_similarity_scores = (
            calculate_dish_similarity(user_tags, dish["tags"]) for dish in restaurant["menu"]
        )
        avg_dish_similarity_score = np.mean(list(dish_similarity_scores))

        # 計算距離分數
        distance_score = calculate_distance_score(user_location, restaurant["location"])

        total_score = WEIGHT_DISH * avg_dish_similarity_score + WEIGHT_DISTANCE * distance_score

        scores.append((restaurant["name"], total_score))

    recommended_restaurants = sorted(scores, key=lambda x: x[1], reverse=True)

    return recommended_restaurants

# 餐廳排序結果
recommended_restaurants = recommend_restaurants(user_1_location, user_1_tags, restaurants)

# 印出推薦結果
for restaurant, score in recommended_restaurants:
    print(f"{restaurant}: {score}")
