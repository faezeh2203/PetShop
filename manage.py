from app import app
from extensions.extensions import db  # تغییر ایمپورت db به extensions.py

@app.cli.command("init-db")
def init_db():
    with app.app_context():  # اضافه کردن context اپلیکیشن
        db.create_all()
        print('Database Created Successfully')

if __name__ == '__main__':
    app.run(debug=True)
