"""
COMPLETE Menu Database Populator for Start Food Telegram Bot
Adds ALL products from the menu images
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Category, SubCategory, Product

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database.db")
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def populate_database():
    session = SessionLocal()
    
    try:
        print("=" * 50)
        print("CREATING CATEGORIES")
        print("=" * 50)
        
        # 1. Create Categories
        drinks_cat = Category(name_uz="Ichimliklar", name_ru="Напитки", name_en="Drinks")
        foods_cat = Category(name_uz="Ovqatlar", name_ru="Еда", name_en="Foods")
        
        session.add_all([drinks_cat, foods_cat])
        session.commit()
        session.refresh(drinks_cat)
        session.refresh(foods_cat)
        
        print(f"✅ Drinks Category ID: {drinks_cat.id}")
        print(f"✅ Foods Category ID: {foods_cat.id}")
        
        print("\n" + "=" * 50)
        print("CREATING SUBCATEGORIES")
        print("=" * 50)
        
        # 2. Create Subcategories under FOODS
        pizza_sub = SubCategory(category_id=foods_cat.id, name_uz="Pizza", name_ru="Пицца", name_en="Pizza")
        session.add(pizza_sub)
        session.commit()
        session.refresh(pizza_sub)
        print(f"✅ Pizza Subcategory ID: {pizza_sub.id} (under Foods category {foods_cat.id})")
        
        burger_sub = SubCategory(category_id=foods_cat.id, name_uz="Burger", name_ru="Бургер", name_en="Burger")
        session.add(burger_sub)
        session.commit()
        session.refresh(burger_sub)
        print(f"✅ Burger Subcategory ID: {burger_sub.id} (under Foods category {foods_cat.id})")
        
        hotdog_sub = SubCategory(category_id=foods_cat.id, name_uz="Hot-dog", name_ru="Хот-дог", name_en="Hot-dog")
        session.add(hotdog_sub)
        session.commit()
        session.refresh(hotdog_sub)
        print(f"✅ Hot-dog Subcategory ID: {hotdog_sub.id} (under Foods category {foods_cat.id})")
        
        lavash_sub = SubCategory(category_id=foods_cat.id, name_uz="Lavash", name_ru="Лаваш", name_en="Lavash")
        session.add(lavash_sub)
        session.commit()
        session.refresh(lavash_sub)
        print(f"✅ Lavash Subcategory ID: {lavash_sub.id} (under Foods category {foods_cat.id})")
        
        chicken_sub = SubCategory(category_id=foods_cat.id, name_uz="Tovuq", name_ru="Курица", name_en="Chicken")
        session.add(chicken_sub)
        session.commit()
        session.refresh(chicken_sub)
        print(f"✅ Chicken Subcategory ID: {chicken_sub.id} (under Foods category {foods_cat.id})")
        
        combo_sub = SubCategory(category_id=foods_cat.id, name_uz="Kombo", name_ru="Комбо", name_en="Combo")
        session.add(combo_sub)
        session.commit()
        session.refresh(combo_sub)
        print(f"✅ Combo Subcategory ID: {combo_sub.id} (under Foods category {foods_cat.id})")
        
        # 3. Create Subcategories under DRINKS
        soft_drinks_sub = SubCategory(category_id=drinks_cat.id, name_uz="Gazlangan ichimliklar", name_ru="Газированные напитки", name_en="Soft Drinks")
        session.add(soft_drinks_sub)
        session.commit()
        session.refresh(soft_drinks_sub)
        print(f"✅ Soft Drinks Subcategory ID: {soft_drinks_sub.id} (under Drinks category {drinks_cat.id})")
        
        hot_drinks_sub = SubCategory(category_id=drinks_cat.id, name_uz="Issiq ichimliklar", name_ru="Горячие напитки", name_en="Hot Drinks")
        session.add(hot_drinks_sub)
        session.commit()
        session.refresh(hot_drinks_sub)
        print(f"✅ Hot Drinks Subcategory ID: {hot_drinks_sub.id} (under Drinks category {drinks_cat.id})")
        
        print("\n" + "=" * 50)
        print("ADDING ALL PRODUCTS")
        print("=" * 50)
        
        # ============ PIZZA PRODUCTS ============
        print(f"\n🍕 Adding Pizza products (subcategory_id={pizza_sub.id})...")
        pizzas = [
            {"name": "Assorti", "name_en": "Assorti", "name_ru": "Ассорти", "price": 30000},
            {"name": "Donarli", "name_en": "Donarli", "name_ru": "Донарли", "price": 30000},
            {"name": "Go'shtli", "name_en": "Go'shtli", "name_ru": "Гоштли", "price": 30000},
            {"name": "Qazili", "name_en": "Qazili", "name_ru": "Казили", "price": 30000},
            {"name": "Pishlоqli", "name_en": "Pishlоqli", "name_ru": "Пишлокли", "price": 26000},
            {"name": "Pepperoni", "name_en": "Pepperoni", "name_ru": "Пепперони", "price": 26000},
            {"name": "Tovuqli", "name_en": "Tovuqli", "name_ru": "Товуоли", "price": 26000},
            {"name": "Vegetarian", "name_en": "Vegetarian", "name_ru": "Вегетариан", "price": 26000},
            {"name": "Margarita", "name_en": "Margarita", "name_ru": "Маргарита", "price": 26000},
            {"name": "Smart", "name_en": "Smart", "name_ru": "Смарт", "price": 26000},
            {"name": "Ikki karra pepperoni", "name_en": "Double Pepperoni", "name_ru": "Двойной пепперони", "price": 30000},
            {"name": "Rimiskaya", "name_en": "Rimiskaya", "name_ru": "Римская", "price": 30000},
            {"name": "Pepperoni + Tovuqli", "name_en": "Pepperoni + Chicken", "name_ru": "Пепперони + Курица", "price": 30000},
            {"name": "Tovuqu", "name_en": "Tovuqu", "name_ru": "Товуоу", "price": 30000},
            {"name": "Burgerli", "name_en": "Burger Pizza", "name_ru": "Бургерли", "price": 30000},
            {"name": "Sezar", "name_en": "Caesar", "name_ru": "Цезарь", "price": 30000},
            {"name": "Baqlajоnli", "name_en": "Eggplant", "name_ru": "Баклажанли", "price": 30000},
            {"name": "Smart Tuхumli", "name_en": "Smart with Egg", "name_ru": "Смарт Тухумли", "price": 30000},
            {"name": "Milano", "name_en": "Milano", "name_ru": "Милано", "price": 30000},
            {"name": "Go'ziqorinli", "name_en": "Mushroom", "name_ru": "Гозикоринли", "price": 30000},
            {"name": "Vegetariana", "name_en": "Vegetariana", "name_ru": "Вегетариана", "price": 30000},
            {"name": "Meksikano", "name_en": "Mexicano", "name_ru": "Мексикано", "price": 30000},
        ]
        
        for p in pizzas:
            session.add(Product(subcategory_id=pizza_sub.id, name_uz=p["name"], name_en=p["name_en"], name_ru=p["name_ru"], price=p["price"], image_url=f"./product_images/{p['name_en'].lower().replace(' ', '_')}.jpg"))
        session.commit()
        print(f"   ✅ Added {len(pizzas)} pizzas")
        
        # ============ BURGER PRODUCTS ============
        print(f"\n🍔 Adding Burger products (subcategory_id={burger_sub.id})...")
        burgers = [
            {"name": "Chicken Burger", "name_en": "Chicken Burger", "name_ru": "Чикен Бургер", "price": 24000},
            {"name": "Burger Chiz", "name_en": "Burger Chiz", "name_ru": "Бургер Чиз", "price": 26000},
            {"name": "Donarli Burger", "name_en": "Doner Burger", "name_ru": "Донарли Бургер", "price": 27000},
            {"name": "Burger Burger Chiz", "name_en": "Burger Burger Chiz", "name_ru": "Бургер Бургер Чиз", "price": 27000},
            {"name": "Dabl Burger", "name_en": "Double Burger", "name_ru": "Дабл Бургер", "price": 38000},
            {"name": "Dabl Burger Chiz", "name_en": "Double Burger Chiz", "name_ru": "Дабл Бургер Чиз", "price": 42000},
            {"name": "Smart Burger", "name_en": "Smart Burger", "name_ru": "Смарт Бургер", "price": 38000},
            {"name": "Kanada", "name_en": "Canada", "name_ru": "Канада", "price": 14000},
            {"name": "Dabl", "name_en": "Double", "name_ru": "Дабл", "price": 18000},
            {"name": "Karalevskiy", "name_en": "Royal", "name_ru": "Каралевский", "price": 26000},
            {"name": "Kichik", "name_en": "Small", "name_ru": "Кичик", "price": 10000},
        ]
        
        for p in burgers:
            session.add(Product(subcategory_id=burger_sub.id, name_uz=p["name"], name_en=p["name_en"], name_ru=p["name_ru"], price=p["price"], image_url=f"./product_images/{p['name_en'].lower().replace(' ', '_')}.jpg"))
        session.commit()
        print(f"   ✅ Added {len(burgers)} burgers")
        
        # ============ HOT-DOG PRODUCTS ============
        print(f"\n🌭 Adding Hot-dog products (subcategory_id={hotdog_sub.id})...")
        hotdogs = [
            {"name": "Sirli", "name_en": "Sirli", "name_ru": "Сирли", "price": 16000},
            {"name": "Halapino", "name_en": "Jalapeno", "name_ru": "Халапино", "price": 16000},
            {"name": "Longer", "name_en": "Longer", "name_ru": "Лонгер", "price": 18000},
            {"name": "Qazili", "name_en": "Qazili", "name_ru": "Казили", "price": 27000},
            {"name": "Smart", "name_en": "Smart", "name_ru": "Смарт", "price": 19000},
            {"name": "Achchiiq", "name_en": "Spicy", "name_ru": "Аччииk", "price": 15000},
            {"name": "Go'shtli", "name_en": "Meat", "name_ru": "Гоштли", "price": 25000},
            {"name": "Assorti", "name_en": "Assorti", "name_ru": "Ассорти", "price": 27000},
        ]
        
        for p in hotdogs:
            session.add(Product(subcategory_id=hotdog_sub.id, name_uz=p["name"], name_en=p["name_en"], name_ru=p["name_ru"], price=p["price"], image_url=f"./product_images/{p['name_en'].lower().replace(' ', '_')}.jpg"))
        session.commit()
        print(f"   ✅ Added {len(hotdogs)} hot-dogs")
        
        # ============ LAVASH PRODUCTS ============
        print(f"\n🌯 Adding Lavash products (subcategory_id={lavash_sub.id})...")
        lavashes = [
            {"name": "Katta", "name_en": "Large", "name_ru": "Катта", "price": 32000},
            {"name": "Kichik", "name_en": "Small", "name_ru": "Кичик", "price": 25000},
            {"name": "Sirli", "name_en": "Sirli", "name_ru": "Сирли", "price": 33000},
            {"name": "Tandir", "name_en": "Tandir", "name_ru": "Тандир", "price": 34000},
            {"name": "Halapino", "name_en": "Jalapeno", "name_ru": "Халапино", "price": 34000},
            {"name": "Achchiiq", "name_en": "Spicy", "name_ru": "Аччииk", "price": 35000},
            {"name": "Achchiiq Katta", "name_en": "Spicy Large", "name_ru": "Аччииk Катта", "price": 38000},
            {"name": "Toster", "name_en": "Toaster", "name_ru": "Тостер", "price": 26000},
            {"name": "Toster Chiz", "name_en": "Toaster Chiz", "name_ru": "Тостер Чиз", "price": 28000},
            {"name": "Lester", "name_en": "Lester", "name_ru": "Лестер", "price": 19000},
            {"name": "Lester Chiz", "name_en": "Lester Chiz", "name_ru": "Лестер Чиз", "price": 21000},
        ]
        
        for p in lavashes:
            session.add(Product(subcategory_id=lavash_sub.id, name_uz=p["name"], name_en=p["name_en"], name_ru=p["name_ru"], price=p["price"], image_url=f"./product_images/{p['name_en'].lower().replace(' ', '_')}.jpg"))
        session.commit()
        print(f"   ✅ Added {len(lavashes)} lavash items")
        
        # ============ CHICKEN PRODUCTS ============
        print(f"\n🍗 Adding Chicken products (subcategory_id={chicken_sub.id})...")
        chickens = [
            {"name": "Strips 12", "name_en": "Strips 12", "name_ru": "Стрипсы 12", "price": 12000},
            {"name": "Strips 16", "name_en": "Strips 16", "name_ru": "Стрипсы 16", "price": 16000},
            {"name": "Strips 20", "name_en": "Strips 20", "name_ru": "Стрипсы 20", "price": 20000},
            {"name": "Strips 32", "name_en": "Strips 32", "name_ru": "Стрипсы 32", "price": 32000},
            {"name": "Strips 0.5kg", "name_en": "Strips 0.5kg", "name_ru": "Стрипсы 0.5кг", "price": 60000},
            {"name": "Strips 1kg", "name_en": "Strips 1kg", "name_ru": "Стрипсы 1кг", "price": 110000},
            {"name": "Qanotcha 12", "name_en": "Wings 12", "name_ru": "Канотча 12", "price": 12000},
            {"name": "Qanotcha 16", "name_en": "Wings 16", "name_ru": "Канотча 16", "price": 16000},
            {"name": "Qanotcha 21", "name_en": "Wings 21", "name_ru": "Канотча 21", "price": 21000},
            {"name": "Qanotcha 25", "name_en": "Wings 25", "name_ru": "Канотча 25", "price": 25000},
            {"name": "Smart Strips 12", "name_en": "Smart Strips 12", "name_ru": "Смарт Стрипсы 12", "price": 12000},
            {"name": "Smart Strips 20", "name_en": "Smart Strips 20", "name_ru": "Смарт Стрипсы 20", "price": 20000},
            {"name": "Smart Strips 29", "name_en": "Smart Strips 29", "name_ru": "Смарт Стрипсы 29", "price": 29000},
            {"name": "Smart Strips 36", "name_en": "Smart Strips 36", "name_ru": "Смарт Стрипсы 36", "price": 36000},
            {"name": "Nuggets 8", "name_en": "Nuggets 8", "name_ru": "Наггетсы 8", "price": 8000},
            {"name": "Nuggets 15", "name_en": "Nuggets 15", "name_ru": "Наггетсы 15", "price": 15000},
            {"name": "Nuggets 27", "name_en": "Nuggets 27", "name_ru": "Наггетсы 27", "price": 27000},
            {"name": "Nuggets 38", "name_en": "Nuggets 38", "name_ru": "Наггетсы 38", "price": 38000},
            {"name": "File 10", "name_en": "Fillet 10", "name_ru": "Филе 10", "price": 10000},
            {"name": "File 16", "name_en": "Fillet 16", "name_ru": "Филе 16", "price": 16000},
            {"name": "File 22", "name_en": "Fillet 22", "name_ru": "Филе 22", "price": 22000},
            {"name": "File 32", "name_en": "Fillet 32", "name_ru": "Филе 32", "price": 32000},
            {"name": "Chicken Big", "name_en": "Chicken Big", "name_ru": "Чикен Биг", "price": 75000},
            {"name": "Sirni Dablcriski 11", "name_en": "Cheese Sticks 11", "name_ru": "Сирни Даблцриски 11", "price": 11000},
            {"name": "Sirni Dablcriski 18", "name_en": "Cheese Sticks 18", "name_ru": "Сирни Даблцриски 18", "price": 18000},
            {"name": "Sirni Dablcriski 26", "name_en": "Cheese Sticks 26", "name_ru": "Сирни Даблцриски 26", "price": 26000},
            {"name": "Sirni Dablcriski 33", "name_en": "Cheese Sticks 33", "name_ru": "Сирни Даблцриски 33", "price": 33000},
            {"name": "Sirni Shariklar 8", "name_en": "Cheese Balls 8", "name_ru": "Сирни Шариклар 8", "price": 8000},
            {"name": "Sirni Shariklar 15", "name_en": "Cheese Balls 15", "name_ru": "Сирни Шариклар 15", "price": 15000},
            {"name": "Sirni Shariklar 22", "name_en": "Cheese Balls 22", "name_ru": "Сирни Шариклар 22", "price": 22000},
            {"name": "Sirni Shariklar 29", "name_en": "Cheese Balls 29", "name_ru": "Сирни Шариклар 29", "price": 29000},
        ]
        
        for p in chickens:
            session.add(Product(subcategory_id=chicken_sub.id, name_uz=p["name"], name_en=p["name_en"], name_ru=p["name_ru"], price=p["price"], image_url=f"./product_images/{p['name_en'].lower().replace(' ', '_')}.jpg"))
        session.commit()
        print(f"   ✅ Added {len(chickens)} chicken items")
        
        # ============ COMBO PRODUCTS ============
        print(f"\n🍱 Adding Combo products (subcategory_id={combo_sub.id})...")
        combos = [
            {"name": "Lanchboks", "name_en": "Lunchbox", "name_ru": "Ланчбокс", "price": 40000},
            {"name": "Kombo Top", "name_en": "Combo Top", "name_ru": "Комбо Топ", "price": 47000},
            {"name": "Kombo Premo", "name_en": "Combo Premo", "name_ru": "Комбо Премо", "price": 53000},
            {"name": "Big Kombo", "name_en": "Big Combo", "name_ru": "Биг Комбо", "price": 57000},
            {"name": "Student Kombo", "name_en": "Student Combo", "name_ru": "Студент Комбо", "price": 45000},
            {"name": "Kombo Ikkilik", "name_en": "Combo Double", "name_ru": "Комбо Иккилик", "price": 47000},
            {"name": "Hot-dog Konbora", "name_en": "Hot-dog Konbora", "name_ru": "Хот-дог Конбора", "price": 42000},
            {"name": "Hot-dog Kombo", "name_en": "Hot-dog Combo", "name_ru": "Хот-дог Комбо", "price": 50000},
            {"name": "Lavash Kombo", "name_en": "Lavash Combo", "name_ru": "Лаваш Комбо", "price": 65000},
            {"name": "Burger Kombo", "name_en": "Burger Combo", "name_ru": "Бургер Комбо", "price": 65000},
            {"name": "Donar Burger Kombo", "name_en": "Doner Burger Combo", "name_ru": "Донар Бургер Комбо", "price": 62000},
            {"name": "Chicken Kombo", "name_en": "Chicken Combo", "name_ru": "Чикен Комбо", "price": 40000},
            {"name": "Pizza Kombo", "name_en": "Pizza Combo", "name_ru": "Пицца Комбо", "price": 40000},
            {"name": "Donar", "name_en": "Doner", "name_ru": "Донар", "price": 45000},
            {"name": "Fri", "name_en": "Fries", "name_ru": "Фри", "price": 15000},
        ]
        
        for p in combos:
            session.add(Product(subcategory_id=combo_sub.id, name_uz=p["name"], name_en=p["name_en"], name_ru=p["name_ru"], price=p["price"], image_url=f"./product_images/{p['name_en'].lower().replace(' ', '_')}.jpg"))
        session.commit()
        print(f"   ✅ Added {len(combos)} combo items")
        
        # ============ DRINK PRODUCTS ============
        print(f"\n🥤 Adding Soft Drink products (subcategory_id={soft_drinks_sub.id})...")
        soft_drinks = [
            {"name": "Coca Cola", "name_en": "Coca Cola", "name_ru": "Кока Кола", "price": 6000},
            {"name": "Fanta", "name_en": "Fanta", "name_ru": "Фанта", "price": 6000},
            {"name": "Sprite", "name_en": "Sprite", "name_ru": "Спрайт", "price": 6000},
            {"name": "Moxito", "name_en": "Mojito", "name_ru": "Мохито", "price": 12000},
            {"name": "Bliss", "name_en": "Bliss", "name_ru": "Блисс", "price": 6000},
        ]
        
        for p in soft_drinks:
            session.add(Product(subcategory_id=soft_drinks_sub.id, name_uz=p["name"], name_en=p["name_en"], name_ru=p["name_ru"], price=p["price"], image_url=f"./product_images/{p['name_en'].lower().replace(' ', '_')}.jpg"))
        session.commit()
        print(f"   ✅ Added {len(soft_drinks)} soft drinks")
        
        print(f"\n☕ Adding Hot Drink products (subcategory_id={hot_drinks_sub.id})...")
        hot_drinks = [
            {"name": "Kapuchino", "name_en": "Cappuccino", "name_ru": "Капучино", "price": 10000},
            {"name": "Qora", "name_en": "Black Coffee", "name_ru": "Черный", "price": 8000},
            {"name": "Malechiyo", "name_en": "Malechiyo", "name_ru": "Малечийо", "price": 12000},
            {"name": "Lemon Chay", "name_en": "Lemon Tea", "name_ru": "Лимон Чай", "price": 8000},
            {"name": "Choy", "name_en": "Tea", "name_ru": "Чой", "price": 5000},
        ]
        
        for p in hot_drinks:
            session.add(Product(subcategory_id=hot_drinks_sub.id, name_uz=p["name"], name_en=p["name_en"], name_ru=p["name_ru"], price=p["price"], image_url=f"./product_images/{p['name_en'].lower().replace(' ', '_')}.jpg"))
        session.commit()
        print(f"   ✅ Added {len(hot_drinks)} hot drinks")
        
        print("\n" + "=" * 50)
        print("✅ DATABASE POPULATED SUCCESSFULLY!")
        print("=" * 50)
        print(f"Categories: {session.query(Category).count()}")
        print(f"Subcategories: {session.query(SubCategory).count()}")
        print(f"Products: {session.query(Product).count()}")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    print("\n🚀 Starting complete menu population...\n")
    populate_database()