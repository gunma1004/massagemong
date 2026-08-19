import os
import re
import random

# ==========================================
# 1. 영문 폴더/파일명 -> 한글 매핑 딕셔너리
# ==========================================
NAME_MAP = {
    # 25개 구
    "gangnam": "강남구", "seocho": "서초구", "songpa": "송파구", "gangdong": "강동구",
    "mapo": "마포구", "yongsan": "용산구", "seodaemun": "서대문구", "eunpyeong": "은평구",
    "jongno": "종로구", "junggu": "중구", "jungnang": "중랑구", "seongbuk": "성북구",
    "gangbuk": "강북구", "dobong": "도봉구", "nowon": "노원구", "seongdong": "성동구",
    "gwangjin": "광진구", "dongdaemun": "동대문구", "yeongdeungpo": "영등포구",
    "guro": "구로구", "geumcheon": "금천구", "yangcheon": "양천구", "gangse": "강서구",
    "gangseo": "강서구", "dongjak": "동작구", "gwanak": "관악구",

    # 주요 동 리스트 (필요 시 자유롭게 추가 가능)
    "yeoksam": "역삼동", "nonhyeon": "논현동", "apgujeong": "압구정동", "cheongdam": "청담동", "samseong": "삼성동",
    "seocho_dong": "서초동", "banpo": "반포동", "bangbae": "방배동", "yangjae": "양재동", "jamwon": "잠원동",
    "jamsil": "잠실동", "garak": "가락동", "munjeong": "문정동", "bangi": "방이동", "ogeum": "오금동",
    "gongneung": "공릉동", "sanggye": "상계동", "junggye": "중계동", "hagye": "하계동", "wolgye": "월계동",
    "hongdae": "홍대", "hapjeong": "합정동", "sinchon": "신촌", "yeonnam": "연남동", "mangwon": "망원동",
    "yeouido": "여의도", "dangsan": "당산동", "mullae": "문래동", "sillim": "신림동", "bongcheon": "봉천동",
    "noryangjin": "노량진", "sangdo": "상도동", "sadang": "사당동", "heukseok": "흑석동", "sindaebang": "신대방동",
    "cheonho": "천호동", "gil": "길동", "amsa": "암사동", "myeongil": "명일동", "seongnae": "성내동",
    "mokdong": "목동", "sinjeong": "신정동", "hwagok": "화곡동", "magok": "마곡동", "guro_dong": "구로동",
    "sindorim": "신도림", "gasan": "가산동", "doksan": "독산동", "itaewon": "이태원", "hannam": "한남동",
    "hyehwa": "혜화동", "myeongdong": "명동", "hoehyeon": "회현동", "sindang": "신당동"
}

def get_korean_name(name):
    clean_name = name.replace(".html", "").lower()
    return NAME_MAP.get(clean_name, clean_name.capitalize())

# ==========================================
# 2. 하위 페이지 전용 랜덤 타이틀 템플릿 (30종)
# ==========================================
TITLE_TEMPLATES = [
    "{loc} 출장 마사지 & 24시 프리미엄 홈타이 안내 | 마사지몽",
    "{loc} 출장 마사지 추천 1위 · 24시 방문 홈케어 | 마사지몽",
    "{loc} 24시 출장 마사지 | 아로마·스웨디시 힐링 케어 - 마사지몽",
    "[{loc} 출장마사지] 프라이빗 1:1 방문 테라피 전문 | 마사지몽",
    "{loc} 출장 마사지 24시간 신속 방문 홈타이 | 마사지몽",
    "{loc} 전지역 출장 마사지 · 호텔식 프리미엄 바디 테라피 | 마사지몽",
    "{loc} 24시 출장 마사지 & 아로마 힐링 홈케어 | 마사지몽",
    "{loc} 출장 마사지 전문점 · 30분 내 도착 보장 안내 | 마사지몽",
    "{loc} 출장 마사지 완벽 가이드 | 타이 & 스웨디시 - 마사지몽",
    "{loc} 프라이빗 24시 출장 마사지 케어 추천 리스트 | 마사지몽",
    "{loc} 출장 마사지 No.1 힐링 솔루션 | 마사지몽",
    "{loc} 24시 출장 타이 마사지 및 아로마 테라피 안내 | 마사지몽",
    "{loc} 출장 마사지 | 야간·새벽 신속 방문 1:1 케어 - 마사지몽",
    "{loc} 프리미엄 24시 출장 마사지 & 홈타이 예약 | 마사지몽",
    "{loc} 출장 마사지 추천 매장 TOP 5 비교 안내 | 마사지몽",
    "꿈결 같은 힐링 {loc} 출장 마사지 & 방문 스파 | 마사지몽",
    "{loc} 출장 마사지 · 100% 후불제 안심 홈케어 서비스 | 마사지몽",
    "{loc} 24시간 언제나 빠른 출장 마사지 매칭 플랫폼 | 마사지몽",
    "{loc} 출장 마사지 | 피로회복 딥티슈 & 림프 순환 - 마사지몽",
    "{loc} 전문 테라피스트 출장 마사지 24시 예약 | 마사지몽",
    "{loc} 출장 마사지 & 감성 스웨디시 방문 테라피 | 마사지몽",
    "{loc} 24시 출장 홈타이 · 힐링 아로마 케어 안내 | 마사지몽",
    "{loc} 출장 마사지 신속 배정 · 고객 만족 1위 - 마사지몽",
    "{loc} 프라이빗 룸케어 출장 마사지 안내 가이드 | 마사지몽",
    "{loc} 출장 마사지 · 24시간 전지역 신속 케어 출동 | 마사지몽",
    "{loc} 출장 마사지 잘하는 곳 추천 & 코스 안내 | 마사지몽",
    "{loc} 24시 1:1 맞춤 출장 마사지 테라피 | 마사지몽",
    "{loc} 감성 아로마 출장 마사지 & 24시 홈타이 | 마사지몽",
    "{loc} 출장 마사지 믿을 수 있는 제휴 매장 안내 | 마사지몽",
    "{loc} 24시 출장 마사지 · 정찰제 안심 힐링 케어 | 마사지몽"
]

# ==========================================
# 3. 하위 페이지 전용 랜덤 설명(Description) 템플릿 (30종)
# ==========================================
DESC_TEMPLATES = [
    "{loc} 전지역 24시 출장 마사지 및 홈타이 전문 안내. 아로마, 스웨디시, 타이 코스를 30분 내 프라이빗하게 이용해보세요.",
    "피로에 지친 하루, {loc} 출장 마사지 마사지몽에서 24시간 신속 방문 테라피와 1:1 맞춤형 힐링 케어를 제공합니다.",
    "{loc} 인근 24시간 출장 마사지 추천. 검증된 전문 테라피스트의 프라이빗 아로마 및 딥티슈 힐링 코스 안내.",
    "{loc} 출장 마사지 100% 후불제 시스템. 타이, 아로마, 림프케어 24시간 신속 방문 서비스로 피로를 날려보세요.",
    "꿈결 같은 휴식을 선사하는 {loc} 24시 출장 마사지. 전문 관리사의 호텔식 테라피를 계신 곳에서 편안히 받아보세요.",
    "{loc} 출장 마사지 & 홈케어 완벽 안내. 자택 및 오피스텔 어디든 30분 내 도착하는 프리미엄 방문 서비스.",
    "{loc} 24시 출장 타이 및 스웨디시 전문점. 깨끗하고 안전한 힐링 케어 프로그램을 지금 확인해보세요.",
    "믿고 이용하는 {loc} 출장 마사지 플랫폼 마사지몽. 철저한 위생 관리와 맞춤 테라피로 최상의 만족을 드립니다.",
    "{loc} 전 구역 24시간 출장 마사지 빠른 배정. 아로마 오일 케어부터 건식 타이까지 취향별 코스 완비.",
    "{loc} 직장인 피로회복을 위한 24시 출장 마사지. 전화 한 통으로 신속하게 방문하는 프리미엄 홈타이 안내.",
    "{loc} 출장 마사지 예약 안내. 고급 천연 오일을 사용한 부드러운 스웨디시와 힐링 림프 케어 제공.",
    "야근 후 늦은 새벽에도 이용 가능한 {loc} 24시 출장 마사지. 빠르고 프라이빗한 맞춤형 케어를 약속합니다.",
    "{loc} 출장 마사지 검증 TOP 5 매장 소개. 합리적인 정찰제 가격과 최고의 테라피 퀄리티를 만나보세요.",
    "{loc} 출장 마사지 & 24시 홈테라피. 숙련된 테라피스트가 선사하는 수준 높은 바디 릴렉싱 프로그램.",
    "{loc} 지역 어디서나 20~30분 내 방문하는 출장 마사지. 내 집에서 편안하게 즐기는 프리미엄 스파 케어.",
    "{loc} 출장 마사지 전문 가이드. 타이, 아로마, 스페셜 콤보 코스 등 다양한 힐링 패키지 안내.",
    "{loc} 24시간 운영되는 믿을 수 있는 출장 마사지. 프라이빗한 공간에서 누리는 극상의 힐링 타임.",
    "{loc} 출장 마사지 마사지몽 추천 제휴점 안내. 정직한 가격과 친절한 서비스로 고객 감동을 실현합니다.",
    "지친 몸과 마음에 활력을 주는 {loc} 24시 출장 마사지. 맞춤 테라피스트 배정으로 신속한 방문 지원.",
    "{loc} 출장 마사지 및 홈타이 실시간 안내. 언제 어디서나 편안하게 이용하는 1:1 방문 바디 케어.",
    "{loc} 24시 출장 마사지 서비스. 꼼꼼한 압 조절과 부드러운 아로마 릴렉싱으로 피로를 완벽하게 해소하세요.",
    "{loc} 출장 마사지 신속 매칭. 번거로운 이동 없이 자택에서 즐기는 최고급 호텔식 바디 테라피.",
    "{loc} 지역 맞춤 24시 출장 마사지 코스 안내. 건식 타이부터 습식 오일 테라피까지 완벽 준비.",
    "{loc} 출장 마사지 대표 브랜드 마사지몽. 서울 전 지역 신속 네트워크로 가장 빠른 방문을 약속합니다.",
    "{loc} 24시간 출장 마사지 및 림프 순환 케어. 전문 관리사의 세심한 손길로 전신 피로를 풀어보세요.",
    "{loc} 출장 마사지 안심 예약 센터. 선입금 없는 안전한 현장 결제 시스템으로 편안하게 이용하세요.",
    "{loc} 전역 24시 출장 홈타이 안내. 고객 만족을 최우선으로 하는 친절하고 품격 있는 바디 힐링.",
    "{loc} 출장 마사지 특별 코스. 뭉친 근육을 시원하게 풀어주는 딥티슈 & 전신 스트레칭 프로그램.",
    "{loc} 24시간 1:1 맞춤 출장 마사지. 바쁜 현대인을 위한 가장 빠르고 안락한 홈케어 솔루션.",
    "{loc} 출장 마사지 추천 코스 완벽 정리. 마사지몽에서 지금 바로 가까운 전문 테라피를 만나보세요."
]

# ==========================================
# 4. 하위 페이지 전용 랜덤 키워드 템플릿 (30종)
# ==========================================
KEYWORD_TEMPLATES = [
    "{loc} 출장 마사지, {loc} 출장, {loc} 홈타이, {loc} 24시 마사지, {loc} 방문 테라피",
    "{loc} 출장 마사지, {loc} 스웨디시, {loc} 아로마 테라피, {loc} 24시 홈케어",
    "{loc} 홈타이, {loc} 출장마사지, {loc} 24시간 마사지, {loc} 1인샵 테라피",
    "{loc} 출장 마사지 추천, {loc} 방문 마사지, {loc} 타이 마사지, {loc} 힐링 테라피",
    "{loc} 24시 출장 마사지, {loc} 홈타이 예약, {loc} 아로마 케어, {loc} 림프 마사지",
    "{loc} 출장 마사지 가격, {loc} 출장 안마, {loc} 스웨디시 홈케어, {loc} 24시 테라피",
    "{loc} 출장 마사지 후기, {loc} 홈타이 추천, {loc} 24시 출장, {loc} 방문 홈케어",
    "{loc} 출장 마사지 빠른곳, {loc} 24시 타이, {loc} 아로마 마사지, {loc} 스파 테라피",
    "{loc} 출장 마사지 24시, {loc} 홈타이 전문, {loc} 호텔식 테라피, {loc} 1:1 바디케어",
    "{loc} 출장 마사지, {loc} 24시 홈타이, {loc} 방문 테라피스트, {loc} 전신 마사지",
    "{loc} 홈케어 출장, {loc} 출장 마사지 예약, {loc} 24시간 방문, {loc} 감성 테라피",
    "{loc} 출장 마사지 코스, {loc} 타이 홈타이, {loc} 아로마 릴렉싱, {loc} 24시 케어",
    "{loc} 출장 마사지, {loc} 24시 스웨디시, {loc} 방문 타이, {loc} 피로회복 마사지",
    "{loc} 홈타이 24시, {loc} 출장 마사지 후불제, {loc} 힐링 홈케어, {loc} 바디 테라피",
    "{loc} 출장 마사지 안내, {loc} 홈케어 마사지, {loc} 24시 아로마, {loc} 스웨디시",
    "{loc} 방문 출장 마사지, {loc} 24시 홈타이 추천, {loc} 딥티슈 테라피, {loc} 힐링",
    "{loc} 출장 마사지 순위, {loc} 타이 마사지 출장, {loc} 24시간 홈케어, {loc} 스파",
    "{loc} 24시 출장 안마, {loc} 출장 마사지 업체, {loc} 홈타이 빠른도착, {loc} 테라피",
    "{loc} 출장 마사지 할인, {loc} 24시 방문 케어, {loc} 아로마 스웨디시, {loc} 홈타이",
    "{loc} 프리미엄 출장 마사지, {loc} 24시 홈타이, {loc} 1:1 방문 테라피, {loc} 마사지몽",
    "{loc} 출장 마사지, {loc} 24시 방문 마사지, {loc} 감성 아로마, {loc} 림프 순환",
    "{loc} 홈타이 출장, {loc} 출장 마사지 잘하는곳, {loc} 24시 홈케어 플랫폼",
    "{loc} 출장 마사지, {loc} 타이 출장, {loc} 스웨디시 방문, {loc} 24시간 테라피",
    "{loc} 24시 출장 마사지 추천, {loc} 홈케어 아로마, {loc} 1인 테라피, {loc} 출장",
    "{loc} 출장 마사지, {loc} 24시 출장 홈타이, {loc} 방문 릴렉싱, {loc} 바디 케어",
    "{loc} 홈타이 예약, {loc} 출장 마사지 24시, {loc} 스웨디시 테라피, {loc} 안마",
    "{loc} 출장 마사지, {loc} 24시간 방문 스파, {loc} 아로마 오일 케어, {loc} 홈케어",
    "{loc} 출장 마사지 전문, {loc} 24시 홈타이 도착, {loc} 프리미엄 테라피",
    "{loc} 방문 출장 마사지, {loc} 24시 아로마 힐링, {loc} 스웨디시 홈케어",
    "{loc} 출장 마사지, {loc} 홈타이 출장 24시, {loc} 1:1 맞춤 방문 바디 테라피"
]

# ==========================================
# 5. 파일 순회 및 일괄 치환 실행
# ==========================================
count = 0

for root, dirs, files in os.walk("."):
    for file in files:
        if not file.endswith(".html"):
            continue
        
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, ".").replace("\\", "/")
        path_parts = rel_path.split("/")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # ----------------------------------------------------
        # 1) 메인 루트 페이지 (index.html) -> '출장마사지' 키워드 철저 제외
        # ----------------------------------------------------
        if rel_path == "index.html":
            new_title = "마사지몽 | 서울 24시 프리미엄 힐링 테라피 & 홈케어 예약 플랫폼"
            new_desc = "꿈결 같은 일상의 쉼표 마사지몽! 서울 전 지역 24시 프리미엄 바디케어 & 힐링 테라피 전문 플랫폼. 아로마, 스웨디시, 타이 1:1 맞춤 케어 코스 안내."
            new_keywords = "마사지몽, 서울 테라피, 서울 홈케어, 강남 스파, 서초 테라피, 송파 힐링케어, 24시 바디케어, 프리미엄 스웨디시"
            new_og_title = "마사지몽 | 서울 24시 프리미엄 바디 테라피 & 힐링 케어"
            new_h1 = "마사지몽 <span>24시 프리미엄 홈케어 & 테라피 안내</span>"

        # ----------------------------------------------------
        # 2) 하위 페이지 (구/동 페이지) -> 30가지 템플릿 중 랜덤 조합
        # ----------------------------------------------------
        else:
            # 구 이름 및 동 이름 추출
            if len(path_parts) == 2 and path_parts[1] == "index.html":
                # 구 메인 (예: nowon/index.html)
                loc_name = get_korean_name(path_parts[0])
            else:
                # 동 세부 (예: nowon/gongneung.html)
                gu_name = get_korean_name(path_parts[0]) if len(path_parts) > 1 else ""
                dong_name = get_korean_name(path_parts[-1])
                loc_name = f"{gu_name} {dong_name}" if gu_name else dong_name

            # 30가지 템플릿에서 각각 무작위 선택
            t_sample = random.choice(TITLE_TEMPLATES)
            d_sample = random.choice(DESC_TEMPLATES)
            k_sample = random.choice(KEYWORD_TEMPLATES)

            new_title = t_sample.format(loc=loc_name)
            new_desc = d_sample.format(loc=loc_name)
            new_keywords = k_sample.format(loc=loc_name)
            new_og_title = f"{loc_name} 출장 마사지 & 24시 프리미엄 홈케어 | 마사지몽"
            new_h1 = f"{loc_name} 출장 마사지 <span>프리미엄 24시 방문 케어</span>"

        # ----------------------------------------------------
        # 정규표현식을 이용한 태그별 완벽 치환
        # ----------------------------------------------------
        # 1. <title>
        content = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', content, flags=re.DOTALL)
        
        # 2. <meta name="description">
        content = re.sub(r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>', 
                         f'<meta name="description" content="{new_desc}">', content, flags=re.DOTALL)
        
        # 3. <meta name="keywords">
        if '<meta name="keywords"' in content or "<meta name='keywords'" in content:
            content = re.sub(r'<meta\s+name=["\']keywords["\']\s+content=["\'].*?["\']\s*/?>', 
                             f'<meta name="keywords" content="{new_keywords}">', content, flags=re.DOTALL)
        else:
            # keywords 태그가 없으면 description 뒤에 자동 삽입
            content = re.sub(r'(<meta\s+name=["\']description["\'].*?>)', 
                             rf'\1\n    <meta name="keywords" content="{new_keywords}">', content, flags=re.DOTALL)
        
        # 4. Open Graph <meta property="og:title">
        if 'property="og:title"' in content or "property='og:title'" in content:
            content = re.sub(r'<meta\s+property=["\']og:title["\']\s+content=["\'].*?["\']\s*/?>', 
                             f'<meta property="og:title" content="{new_og_title}">', content, flags=re.DOTALL)

        # 5. 헤더 <h1> 텍스트도 동적으로 깔끔하게 동기화
        content = re.sub(r'<h1>.*?</h1>', f'<h1>{new_h1}</h1>', content, flags=re.DOTALL)

        # 파일 저장
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        count += 1
        print(f"✔ [{loc_name if rel_path != 'index.html' else '메인'}] -> {new_title}")

print(f"\n🎉 작업 완료! 총 {count}개 페이지의 메타태그와 타이틀이 30개 패턴으로 자연스럽게 랜덤 분산 적용되었습니다.")