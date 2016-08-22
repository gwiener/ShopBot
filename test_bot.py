import threading
import time
from urllib.request import urlopen
import bot


thr = threading.Thread(target=bot.main, args=('rest', 'tagged.csv'), daemon=True)
thr.start()
time.sleep(5)
response = urlopen("http://localhost:8080/v1/tags", b"lightweight")
data = response.read().decode('utf-8')
print(data)
