from database.models import User, Order, Category
from database.database import SessionLocal
from geopy.geocoders import Nominatim

def user_exists(user_id: int) -> bool:
    db = SessionLocal()
    try:
        exists = db.query(User).filter(User.id == user_id).first() is not None
        return exists
    finally:
        db.close()

def add_user(user_id: int, first_name: str, last_name: str | None, username: str | None):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.id == user_id).first()
    
    if not existing_user:
        user = User(id=user_id, first_name=first_name, last_name=last_name, username=username)
        db.add(user)
        db.commit()
    
    db.close()

def set_language_user(user_id: int, language: str):
    db = SessionLocal()
    user = db.query(User).filter_by(id=user_id).first()
    
    if user:
        user.language = language
        db.commit()
    db.close()

def get_user_language(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter_by(id=user_id).first()
    db.close()
    if user:
        return user.language if user else None

def set_user_state(user_id: int, state: str):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        user.state = state
        db.commit()
    
    db.close()

def get_user_state(user_id: int) -> str | None:
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    return user.state if user else None

def add_user_order_type(user_id: int, order_type: str):
    db = SessionLocal()
    existing_order = db.query(Order).filter(Order.user_id == user_id, Order.status == "basket").first()
    
    if existing_order:
        existing_order.order_type = order_type
        db.commit() 
        db.refresh(existing_order)
        return existing_order
    else:
        new_order = Order(
            user_id=user_id,
            order_type=order_type,
            status="basket"
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

def add_user_location(user_id: int, latitude: float, longitude: float):
    db = SessionLocal()
    order = db.query(Order).filter(Order.user_id == user_id, Order.status == "basket").first()
    
    if order:
        order.location_lat = latitude
        order.location_lon = longitude
        db.commit()  
        db.refresh(order) 
    else:
        print(f"No active 'basket' order found for user {user_id}")
    
    return order


def get_user_location(user_id: int) -> str | None:
    try:
        session = SessionLocal()
        order = session.query(Order)\
            .filter(Order.user_id == user_id)\
            .filter(Order.location_lat.isnot(None), Order.location_lon.isnot(None))\
            .order_by(Order.created_at.desc())\
            .first()

        if order:
            geolocator = Nominatim(user_agent="smart_food") 
            location = geolocator.reverse((order.location_lat, order.location_lon), exactly_one=True)
            if location and location.address:
                return location.address
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching user location: {e}")
        return None
    finally:
        session.close()



def get_category_name_all() -> str | None:
    try:
        db = SessionLocal()
        categories = db.query(Category).all()
        names = [category.name for category in categories]
        result = ", ".join(names)
        print(result)
        return result
    except Exception as e:
        print(f"Error fetching category names: {e}")
        return None
    finally:
        db.close()


