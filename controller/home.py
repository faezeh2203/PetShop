from flask import Flask, render_template, request
import requests
from flask import current_app as app


def fetch_breeds():
    try:
        response = requests.get("https://dog.ceo/api/breeds/list/all")
        response.raise_for_status()
        return response.json()['message']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching breed list: {e}")
        return {}

def fetch_breed_image(breed):
    try:
        image_response = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
        image_response.raise_for_status()
        return image_response.json()['message']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image for breed {breed}: {e}")
        return None

class Home:

    def __init__(self, *args, **kwargs):
        pass
    
    def main(self):
        page = request.args.get('page', 1, type=int)  # دریافت شماره صفحه از URL
        per_page = 10  # تعداد نژادها در هر صفحه

        breeds = fetch_breeds()
        breed_list = list(breeds.items())
        total_breeds = len(breed_list)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_breeds = dict(breed_list[start:end])

        breed_images = {breed: fetch_breed_image(breed) for breed in paginated_breeds}

        return render_template('home.html', breeds=paginated_breeds, breed_images=breed_images, page=page, total_breeds=total_breeds, per_page=per_page)