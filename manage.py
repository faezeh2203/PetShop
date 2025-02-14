from app import app
from extensions.extensions import db
from models import Breed  # ایمپورت مدل‌ها

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()

        # بررسی می‌کنیم که آیا مقداردهی اولیه انجام شده یا نه
        if not Breed.query.first():
            initial_breeds = [
                Breed(id=1, name="african", image_url="https://dog.ceo/api/img/african.jpg"),
                Breed(id=2, name="bulldog", image_url="https://dog.ceo/api/img/bulldog.jpg"),
                Breed(id=3, name="beagle", image_url="https://dog.ceo/api/img/beagle.jpg")
            ]

            db.session.bulk_save_objects(initial_breeds)
            db.session.commit()
            print("Database initialized with sample breeds!")

if __name__ == '__main__':
    app.run(debug=True)
