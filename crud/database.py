import requests

BASE_URL = "http://127.0.0.1:8000"


class database:
    def __init__(self):
        self.base_url = BASE_URL

    def find_all_goods(self):
        try:
            response = requests.get(f"{self.base_url}/products/", timeout=5)
            if response.status_code == 200:
                products = response.json()
                return [(p['id'], p['name'], p['price']) for p in products]
            return []
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return []

    def find_goods_filter(self, id=None, name=None, from_price=None, to_price=None):
        all_goods = self.find_all_goods()
        result = []

        for item in all_goods:
            item_id, item_name, item_price = item

            if id and str(id).strip() != "":
                if str(item_id) != str(id).strip():
                    continue

            if name and str(name).strip() != "":
                if str(name).strip().lower() not in str(item_name).lower():
                    continue

            if from_price and str(from_price).strip() != "":
                try:
                    if float(item_price) < float(from_price):
                        continue
                except ValueError:
                    pass

            if to_price and str(to_price).strip() != "":
                try:
                    if float(item_price) > float(to_price):
                        continue
                except ValueError:
                    pass

            result.append(item)

        return result

    def insert_into_goods(self, name, price, code=""):
        try:
            data = {"name": name, "price": float(price), "code": code}
            response = requests.post(f"{self.base_url}/products/", json=data, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None

    def delete_goods(self, product_id):
        try:
            response = requests.delete(f"{self.base_url}/products/{product_id}", timeout=5)
            return response.status_code == 200
        except:
            return False

    def update_goods(self, product_id, name, price, code=""):
        try:
            data = {"name": name, "price": float(price), "code": code}
            response = requests.put(f"{self.base_url}/products/{product_id}", json=data, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def find_all_customers(self):
        try:
            response = requests.get(f"{self.base_url}/customers/", timeout=5)
            if response.status_code == 200:
                customers = response.json()
                return [(c['id'], c['username']) for c in customers]
            return []
        except:
            return []

    def find_customer_by_id(self, customer_id):
        try:
            response = requests.get(
                f"{self.base_url}/customers/{customer_id}", timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None

    def insert_into_customers(self, username, password):
        try:
            data = {"username": username, "password": password}
            response = requests.post(f"{self.base_url}/customers/", json=data, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def insert_into_factors(self, customer_id, items):
        try:
            data = {"customer_id": customer_id, "items": items}
            response = requests.post(f"{self.base_url}/factors/", json=data, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def find_all_factors(self):
        try:
            response = requests.get(f"{self.base_url}/factors/", timeout=5)
            if response.status_code == 200:
                return response.json()
            return []
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return []

    def find_factor_by_id(self, factor_id):
        try:
            response = requests.get(
                f"{self.base_url}/factors/{factor_id}", timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None

    def delete_factor(self, factor_id):
        try:
            response = requests.delete(
                f"{self.base_url}/factors/{factor_id}", timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return False