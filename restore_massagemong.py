import os
import re

for root, dirs, files in os.walk("."):
    for file in files:
        if not file.endswith(".html"):
            continue
        file_path = os.path.join(root, file)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # '스파루나'를 다시 '마사지몽'으로 일괄 교체
        content = content.replace("스파루나", "마사지몽")
        content = content.replace("SpaLuna", "MassageMong")
        content = content.replace("spaluna", "massagemong")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

print("✔ 마사지몽 명칭 일괄 복구 완료!")