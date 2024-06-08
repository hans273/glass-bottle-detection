import requests

url = 'https://qr-reward-redeemer-server.onrender.com/earist/api/rewards'



def addReward(body):
    
    x = requests.post(f"{url}/addReward", json = body)

    print('RESPONSE', x.text)