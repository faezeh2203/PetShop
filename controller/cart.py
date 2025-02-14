from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from flask import current_app as app
from extensions.extensions import db
from flask import request

from models import Cart, Breed, Order  # اضافه کردن مدل Order

class CartController:
    @login_required
    def view_cart(self):
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            flash('Your cart is empty.', 'info')
        return render_template('cart.html', cart_items=cart_items)


    @login_required
    def add_to_cart(self):
        breed_id = request.form.get('breed_id')
        
        # بررسی مقدار breed_id
        if not breed_id:
            flash('Invalid request. Breed ID is missing.', 'error')
            return redirect(url_for('main'))
        
        # بررسی اینکه نژاد موردنظر در دیتابیس وجود دارد
        breed = Breed.query.get(breed_id)
        if not breed:
            flash('Breed not found.', 'error')
            return redirect(url_for('main'))

        # بررسی اینکه آیا محصول در سبد خرید موجود است یا نه
        cart_item = Cart.query.filter_by(user_id=current_user.id, breed_id=breed_id).first()
        
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = Cart(user_id=current_user.id, breed_id=breed_id, quantity=1)  # مقداردهی quantity
            db.session.add(cart_item)

        db.session.commit()
        flash('Product added to cart!', 'success')
        return redirect(url_for('main'))


    @login_required
    def remove_from_cart(self, cart_item_id):
        cart_item = Cart.query.get_or_404(cart_item_id)
        if cart_item.user_id != current_user.id:
            abort(403)

        db.session.delete(cart_item)
        db.session.commit()
        flash('Product removed from cart!', 'success')
        return redirect(url_for('view_cart'))

    @login_required
    def checkout(self):
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        
        if not cart_items:
            flash('Your cart is empty.', 'info')
            return redirect(url_for('view_cart'))
        
        for item in cart_items:
            print(f"Processing order: user_id={current_user.id}, breed_id={item.breed_id}, quantity={item.quantity}")  # نمایش مقدار قبل از ذخیره

            order = Order(user_id=current_user.id, breed_id=item.breed_id, quantity=item.quantity)
            db.session.add(order)
            db.session.delete(item)

        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('main'))
