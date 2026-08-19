import os

# 1. Unsplash URL -> 교체할 내 이미지 경로 매핑
# (루트 폴더에 images 폴더를 만들고 아래 파일명으로 사진을 넣어두세요)
IMAGE_MAPPING = {
    # 히어로 배너 이미지
    "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=1200&q=80": "/images/main-banner.jpg",
    "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=1200&q=80": "/images/main-banner.jpg",
    
    # 1번 업체 (기쁨조 / 한국미인 등)
    "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80": "/images/vendor1.jpg",
    
    # 2번 업체
    "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80": "/images/vendor2.jpg",
    
    # 3번 업체
    "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=800&q=80": "/images/vendor3.jpg",
    
    # 4번 업체
    "https://images.unsplash.com/photo-1600334089648-b0d9d3028eb2?auto=format&fit=crop&w=800&q=80": "/images/vendor4.jpg",
    
    # 5번 업체
    "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=800&q=80": "/images/vendor5.jpg",
}

count = 0

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = content
            for old_url, new_url in IMAGE_MAPPING.items():
                if old_url in new_content:
                    new_content = new_content.replace(old_url, new_url)

            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count += 1
                print(f"✔ 수정 완료: {file_path}")

print(f"\n🎉 총 {count}개의 HTML 파일 이미지 경로가 성공적으로 변경되었습니다!")