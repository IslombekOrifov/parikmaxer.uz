def upload_avatar_path(instance, avatar):
    return f"users/{instance.USERNAME_FIELD}/avatar/{avatar}"

def upload_news_path(instance, image):
    return f"news/{image}"
