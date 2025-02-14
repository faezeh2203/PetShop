import os

def allow_extension(filename):
    ext = filename.split('.')[-1].lower()
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return ext in allowed_extensions
