import requests
from bs4 import BeautifulSoup
import os
import hashlib

# بياناتك
TOKEN = "8663941354:AAGdGLN_9upnbXxmia7Yq1j1CZmpoW2edr0"
CHAT_ID = "7275028571"
URL = "https://services.aun.edu.eg/results/public/ar/exam-result?fbclid="

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        
        # استخراج النص بس عشان نتجاهل أي تغييرات في أكواد الموقع الداخلية
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text(strip=True)
        
        # عمل بصمة (Hash) للنص عشان نعرف لو اتغير
        current_hash = hashlib.md5(text_content.encode('utf-8')).hexdigest()
        
        old_hash = ""
        if os.path.exists("last_hash.txt"):
            with open("last_hash.txt", "r") as f:
                old_hash = f.read().strip()
        
        if current_hash != old_hash:
            if old_hash != "":
                # لو البصمة اتغيرت، ابعت رسالة
                msg = "🔔 يا علي، فيه تحديث جديد في موقع النتائج!\nادخل شيك على النتيجة دلوقتي:\n" + URL
                send_telegram_message(msg)
            
            # حفظ البصمة الجديدة للمرة الجاية
            with open("last_hash.txt", "w") as f:
                f.write(current_hash)

    except Exception as e:
        print("حدث خطأ:", e)

if __name__ == "__main__":
    main()

