
import requests
import sys

def debug():
    s = requests.Session()
    # 1. Login
    login_url = 'http://127.0.0.1:8000/admin/login/'
    try:
        r = s.get(login_url)
        csrf_token = r.cookies['csrftoken']
        
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'csrfmiddlewaretoken': csrf_token,
            'next': '/admin/'
        }
        
        r = s.post(login_url, data=login_data, headers={'Referer': login_url})
        if r.status_code != 200:
            print(f"Login failed: {r.status_code}")
            return

        # 2. Access Cart Admin
        cart_url = 'http://127.0.0.1:8000/admin/food_store/cart/'
        print(f"Requesting {cart_url}...")
        r = s.get(cart_url)
        print(f"Status Code: {r.status_code}")
        if r.status_code == 500:
            print("Got 500 Error!")
            with open('error.html', 'w', encoding='utf-8') as f:
                f.write(r.text)
            print("Saved error.html")
        else:
            print("Request successful?")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    debug()
