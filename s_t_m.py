def recommend_content(users_data, target_user, top_n=3):
    if target_user not in users_data:
        return []

    target_items = set(users_data[target_user])
    scores = {}

    for user, items in users_data.items():
        if user == target_user:
            continue

        user_items = set(items)
        common_items = target_items & user_items
        similarity = len(common_items)

        if similarity == 0:
            continue

        new_items = user_items - target_items

        for item in new_items:
            scores[item] = scores.get(item, 0) + similarity

    result = sorted(scores, key = scores.get, reverse = True)

    return result[:top_n]





users_data = {"Ali": ["Action", "Drama", "Comedy"],
    "hossein": ["Action", "Drama", "Horror"],
    "Reza": ["Action", "Comedy", "Sci-Fi"],
    "Mina": ["Romance", "Animation", "Musical"],
    "Nima": ["Drama", "Comedy", "Horror"]}

print(recommend_content(users_data, "Ali", 3))

