def get_social_type(social_network):
    return {
        "Telegram": 0,
        "ВКонтакте": 1,
        "Youtube": 2,
        "Инстаграм": 3,
        "Facebook": 4,
        "TikTok": 5,
        "Twitter": 6,
        "Одноклассники": 7,
    }[social_network]
