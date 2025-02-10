from flask import *
import boto3
from decimal import Decimal
import pymysql

# RDS 인스턴스 연결
connection = pymysql.connect(
    host='final-project.cnohqzdklodx.ap-northeast-2.rds.amazonaws.com',
    user='admin',
    password='admin1234',
    database='proj',
    port=3306
)


class UserDao:
    def __init__(self):
        pass

    def get_all_users(self):
        # 모든 요소 조회
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        return users
    
    # 사용자 조회 (id와 password로 확인)
    def get_user(self, id, password):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (id,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and user[2] == password:  # assuming 'userpass' is the 3rd column
            return user
        return None
    
    # 사용자 정보 ID로 조회 (마이페이지에서 사용)
    def get_user_by_id(self, user_id):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user
        
    def insert_user(self, user_name, id, password, answer, cart=[]):
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users (client_id, username, password, answer)
            VALUES (1, %s, %s, %s, %s, %s)
        """, (id, user_name, password, answer, str(cart)))
        connection.commit()
        cursor.close()
        return "Insert OK"

    def get_current_user(self):
        user_id = session.get('user_id')  # 세션에서 사용자 ID를 가져옴
        if user_id:
            return convert_decimal(self.get_user_by_id(user_id))  # 사용자 ID로 사용자 정보 조회
        return None

    def get_cart_by_id(self,user_id):
        cursor = connection.cursor()
        cursor.execute("SELECT cart FROM user WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()
        cursor.close()
        if cart:
            return cart[0]  # Assuming cart is stored as a string
        return []
    
    def update_cart(self,user_id,product_id, quantity):
        cursor = connection.cursor()
        cursor.execute("SELECT cart FROM user WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()
        
        if cart:
            cart = eval(cart[0])  # If cart is stored as a string, convert it back to a list
            item_found = False
            for idx, (item, qty) in enumerate(cart):
                if item == product_id:
                    cart[idx] = (item, quantity)
                    item_found = True
                    break
            
            if not item_found:
                cart.append((product_id, quantity))
            
            # Update the cart
            cursor.execute("UPDATE users SET cart = %s WHERE user_id = %s", (str(cart), user_id))
            connection.commit()
            cursor.close()
            return cart
        cursor.close()
        return []

    def remove_from_cart(self, user_id, product_id):
        cursor = connection.cursor()
        cursor.execute("SELECT cart FROM users WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()
        
        if cart:
            cart = eval(cart[0])  # Convert from string to list
            updated_cart = [item for item in cart if item[0] != product_id]
            
            cursor.execute("UPDATE users SET cart = %s WHERE user_id = %s", (str(updated_cart), user_id))
            connection.commit()
            cursor.close()
            return updated_cart
        cursor.close()
        return []

def convert_decimal(data):
    """DynamoDB에서 반환된 데이터를 JSON 직렬화 가능하게 변환"""
    if isinstance(data, list):
        return [convert_decimal(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_decimal(v) for k, v in data.items()}
    elif isinstance(data, Decimal):
        return float(data)  # 또는 str(data)
    else:
        return data