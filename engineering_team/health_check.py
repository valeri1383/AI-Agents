
import requests

def health_check():
    response = requests.get('http://localhost:5000/health')
    print('Health Check Status:', response.status_code)

if __name__ == '__main__':
    health_check()
