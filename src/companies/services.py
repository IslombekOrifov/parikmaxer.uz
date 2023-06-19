def upload_logo_path(instance, image):
    return f"companies/{instance.name}/logo/{image}"

def upload_serv_image_path(instance, image):
    return f"companies/{instance.name}/sevice/{image}"