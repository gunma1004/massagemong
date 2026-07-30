import os
import re

# 영문 폴더명 매핑 (대소문자 및 일부 오탈자 포함)
GU_MAP = {
    "dobong": "도봉구",
    "dongdaemun": "동대문구",
    "dongjak": "동작구",
    "eunpyeong": "은평구",
    "gangbuk": "강북구",
    "gangse": "강서구",
    "gangseo": "강서구",
    "geumcheon": "금천구",
    "guro": "구로구",
    "gwangjin": "광진구",
    "jongno": "종로구",
    "junggu": "중구",
    "jungnang": "중랑구",
    "mapo": "마포구",
    "nowon": "노원구",
    "seodaemun": "서대문구",
    "seongbuk": "성북구",
    "seongdong": "성동구",
    "yangcheon": "양천구",
    "yeongdeungpo": "영등포구",
    "yongsan": "용산구"
}

def update_all_html_files():
    current_dir = os.getcwd()
    print(f"📂 작업 대상 경로: {current_dir}\n")
    
    updated_count = 0
    
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.lower().endswith('.html'):
                file_path = os.path.join(root, file)
                norm_path = os.path.normpath(file_path)
                path_parts = [p.lower() for p in norm_path.split(os.sep)]
                
                # 1. 폴더 경로에서 구 이름 감지
                gu_name = None
                for key, val in GU_MAP.items():
                    if key in path_parts:
                        gu_name = val
                        break

                # 파일 읽기
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='euc-kr', errors='ignore') as f:
                            content = f.read()
                    except Exception:
                        continue

                # 2. 폴더명으로 못 찾았으면 본문 내부에서 '00구' 자동 추출
                if not gu_name:
                    match = re.search(r'([가-힗]{2,4}구)', content)
                    if match:
                        gu_name = match.group(1)
                    else:
                        gu_name = "서울"

                # --- SEO 키워드 교체 ---
                
                # <title> 교체
                content = re.sub(
                    r'<title>(.*?)</title>',
                    f'<title>{gu_name} 출장 마사지 & 24시 프리미엄 홈케어 안내</title>',
                    content, flags=re.IGNORECASE | re.DOTALL
                )
                
                # <meta description> 교체
                content = re.sub(
                    r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*>/?',
                    f'<meta name="description" content="서울 {gu_name} 출장 마사지 및 24시 방문 테라피 전문 추천 안내. 프라이빗 아로마, 스웨디시, 홈케어 코스.">',
                    content, flags=re.IGNORECASE | re.DOTALL
                )
                
                # <h1> 메인 타이틀 교체
                content = re.sub(
                    r'<h1>(.*?)</h1>',
                    f'<h1>{gu_name} 출장 마사지 <span>프리미엄 24시 방문 케어</span></h1>',
                    content, flags=re.IGNORECASE | re.DOTALL
                )

                # 파일 저장
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    rel_path = os.path.relpath(file_path, current_dir)
                    print(f"✅ [교체 완료] {rel_path}")
                    updated_count += 1
                except Exception as e:
                    print(f"❌ [오류] {file_path}: {e}")

    print(f"\n🎉 총 {updated_count}개 HTML 파일의 SEO 키워드 일괄 교체가 완료되었습니다!")

if __name__ == "__main__":
    update_all_html_files()