from flask import Flask, render_template, send_file
import qrcode
import io

app = Flask(__name__)

# Sample menu items
menu_items = {
    "Appetizers": [
        {"name": "Garlic Bread", "description": "Toasted bread with garlic.", "price": 150, "votes": 8, "image": "https://spicecravings.com/wp-content/uploads/2021/09/Air-Fryer-Garlic-Bread-Featured.jpg"},
        {"name": "Cheese Nachos", "description": "Crispy nachos with cheese.", "price": 220, "votes": 12, "image": "https://iambaker.net/wp-content/uploads/2019/07/chili-cheese-nacho-final.jpg"},
        {"name": "Chicken Wings", "description": "Spicy chicken wings.", "price": 300, "votes": 15, "image": "https://bakerbynature.com/wp-content/uploads/2015/02/Sweet-and-Spicy-Sriracha-Chicken-Wings-0-6.jpg"},
        {"name": "Paneer Tikka", "description": "Grilled paneer marinated with spices.", "price": 250, "votes": 10, "image": "https://www.cookwithmanali.com/wp-content/uploads/2015/07/Restaurant-Style-Recipe-Paneer-Tikka-500x500.jpg"},
        {"name": "French Fries", "description": "Crispy golden fries.", "price": 120, "votes": 20, "image": "https://sailorbailey.com/wp-content/uploads/2022/08/Crispy-Homemade-Fries2.jpg"},
    ],
    "Main Course": [
        {"name": "Butter Chicken", "description": "Creamy butter chicken curry.", "price": 450, "votes": 18, "image": "https://static.toiimg.com/thumb/74654861.cms?width=573&height=430"},
        {"name": "Paneer Butter Masala", "description": "Paneer cooked in buttery gravy.", "price": 400, "votes": 15, "image": "https://www.indianhealthyrecipes.com/wp-content/uploads/2023/07/paneer-butter-masala-recipe.jpg"},
        {"name": "Grilled Fish", "description": "Fresh fish grilled to perfection.", "price": 550, "votes": 14, "image": "https://www.lanascooking.com/wp-content/uploads/2021/07/simple-seasoned-grilled-fish-feature-1200.jpg"},
        {"name": "Vegetable Biryani", "description": "Spiced rice with mixed vegetables.", "price": 350, "votes": 12, "image": "https://www.indianveggiedelight.com/wp-content/uploads/2020/04/veg-biryani-instant-pot.jpg"},
        {"name": "Chicken Biryani", "description": "Fragrant rice with marinated chicken.", "price": 400, "votes": 16, "image": "https://ministryofcurry.com/wp-content/uploads/2024/06/chicken-biryani-5.jpg"},
        # Additional items
        {"name": "Dal Makhani", "description": "Creamy lentils simmered with spices.", "price": 350, "votes": 10, "image": "https://5.imimg.com/data5/SELLER/Default/2023/9/345465731/JQ/IR/EX/91848690/ready-to-eat-dal-makhani.jpg"},
        {"name": "Palak Paneer", "description": "Spinach and paneer in a rich gravy.", "price": 400, "votes": 11, "image": "https://healthynibblesandbits.com/wp-content/uploads/2020/01/Saag-Paneer-FF.jpg"},
        {"name": "Chole Bhature", "description": "Spicy chickpeas with fried bread.", "price": 320, "votes": 14, "image": "https://media.vogue.in/wp-content/uploads/2020/08/chole-bhature-recipe.jpg"},
        {"name": "Prawn Curry", "description": "Spicy prawn curry with coconut milk.", "price": 550, "votes": 15, "image": "https://i.ytimg.com/vi/xMdhea4fLjU/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCpYdTQOCF9hIv_49vPKriuga6aIw"},
        {"name": "Lamb Rogan Josh", "description": "Slow-cooked lamb in aromatic spices.", "price": 600, "votes": 13, "image": "https://hips.hearstapps.com/hmg-prod/images/rogan-josh-wide-1572547980.jpg"},
        {"name": "Vegetable Korma", "description": "Mixed vegetables in a creamy sauce.", "price": 380, "votes": 9, "image": "https://holycowvegan.net/wp-content/uploads/2013/12/vegetable-korma-kurma-mixed-vegetable-curry-8.jpg"},
        {"name": "Chicken Tikka Masala", "description": "Grilled chicken in spiced tomato sauce.", "price": 480, "votes": 17, "image": "https://cafedelites.com/wp-content/uploads/2018/04/Best-Chicken-Tikka-Masala-IMAGE-2.jpg"},
        {"name": "Fish Curry", "description": "Spicy fish curry with a tangy sauce.", "price": 500, "votes": 12, "image": "https://vismaifood.com/storage/app/uploads/public/daa/96d/7bc/thumb__1200_0_0_0_auto.jpg"},
        {"name": "Stuffed Paratha (Aloo/Gobhi)", "description": "Stuffed flatbread with spices.", "price": 250, "votes": 10, "image": "https://lh6.googleusercontent.com/proxy/umlZlcu6rMjAAp1XbqfVw3Dafcvf8q4plIWHPQ8ASwKz62EMu8SA3rdEgNAQSfNr42TySd2ItcQwdB98TRPZidonT0RBhy_gH4M"},
        {"name": "Egg Biryani", "description": "Spiced rice with boiled eggs.", "price": 370, "votes": 11, "image": "https://www.indianhealthyrecipes.com/wp-content/uploads/2020/02/instant-pot-egg-biryani.jpg"},
    ],
    "Pasta": [
        {"name": "White Sauce Pasta", "description": "Pasta in creamy white sauce.", "price": 300, "votes": 10, "image": "https://www.whiskaffair.com/wp-content/uploads/2021/05/White-Sauce-Paste-2-3-500x375.jpg"},
        {"name": "Red Sauce Pasta", "description": "Pasta in tangy red sauce.", "price": 320, "votes": 8, "image": "https://aartimadan.com/wp-content/uploads/2020/09/red-sauce-pasta-blog-4.jpg"},
        {"name": "Penne Arrabbiata", "description": "Penne pasta in spicy tomato sauce.", "price": 340, "votes": 9, "image": "https://finefoodsblog.com/wp-content/uploads/2021/03/penne-allArrabbiata-1200.jpg"},
        {"name": "Spaghetti Aglio e Olio", "description": "Spaghetti with garlic and olive oil.", "price": 350, "votes": 11, "image": "https://assets.tmecosys.com/image/upload/t_web767x639/img/recipe/ras/Assets/2de91e83-2502-47a6-aaa6-99a65eec8bea/Derivates/59952bab-94cb-42e4-8ae4-3e3925f737b3.jpg"},
    ],
    "Pizza": [
        {"name": "Margherita Pizza", "description": "Classic cheese and tomato pizza.", "price": 280, "votes": 20, "image": "https://foodbyjonister.com/wp-content/uploads/2020/01/MargheritaPizza.jpg"},
        {"name": "Pepperoni Pizza", "description": "Pizza topped with pepperoni slices.", "price": 350, "votes": 18, "image": "https://atsloanestable.com/wp-content/uploads/2023/06/new-york-style-pizza2-500x500.jpg"},
        {"name": "Farmhouse Pizza", "description": "Topped with vegetables and cheese.", "price": 320, "votes": 16, "image": "https://i.ytimg.com/vi/fHo1j3VF7VE/maxresdefault.jpg"},
        {"name": "BBQ Chicken Pizza", "description": "Chicken topped with BBQ sauce.", "price": 370, "votes": 14, "image": "https://i0.wp.com/www.slapyodaddybbq.com/wp-content/uploads/BBQChickenPizza-foodgawker.jpg?fit=600%2C600&ssl=1"},
    ],
    "Drinks": [
        {"name": "Mojito", "description": "Refreshing mint and lime drink.", "price": 180, "votes": 10, "image": "https://www.bitensip.com/wp-content/uploads/2022/12/blue-virjin-mojito.jpg"},
        {"name": "Cold Coffee", "description": "Iced coffee with milk.", "price": 150, "votes": 12, "image": "https://www.indianhealthyrecipes.com/wp-content/uploads/2021/03/cold-coffee-recipe-500x500.jpg"},
        {"name": "Lemonade", "description": "Chilled lemonade with mint.", "price": 100, "votes": 20, "image": "https://www.kanakflavours.com/wp-content/uploads/2021/07/Lemonade.jpg"},
        {"name": "Fresh Juice", "description": "Seasonal fresh juice.", "price": 200, "votes": 15, "image": "https://www.cookwithmanali.com/wp-content/uploads/2020/04/vegetable-juice-recipe.jpg"},
    ]
}

# Sample waiters
waiters = [
    {"name": "Manas Jadhav", "upi_id": "manas.jadhav.7779@okhdfcbank"},
    {"name": "Jane Smith", "upi_id": "jane.smith@upi"},
]

@app.route('/')
def index():
    return render_template('hotel_dashboard.html', menu_items=menu_items, waiters=waiters)

@app.route('/generate_qr/<path:upi_url>')
def generate_qr(upi_url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    # Bind to all interfaces to make the app accessible across devices on the same network
    app.run(host='0.0.0.0', port=5000, debug=True)
