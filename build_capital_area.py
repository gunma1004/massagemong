import os

# 생성할 경기/인천 지역 구조 (영문폴더명: (한글명, [하위 대표 동/읍/면]))
NEW_REGIONS = {
    # [인천광역시]
    "incheon_bupyeong": ("인천 부평구", ["bupyeong", "sanggok", "cheongcheon", "galsan"]),
    "incheon_namdong": ("인천 남동구", ["guwol", "ganseok", "nonhyeon", "mansu"]),
    "incheon_yeonsu": ("인천 연수구", ["songdo", "yeonsu", "dongchun", "cheonghak"]),
    "incheon_michuhol": ("인천 미추홀구", ["juan", "yonghyeon", "dohwa", "sungui"]),
    "incheon_seogu": ("인천 서구", ["cheongna", "geomdan", "yeonhui", "gajeong"]),
    "incheon_gyeyang": ("인천 계양구", ["gyeyang", "galsan", "jakjeon", "hyoseong"]),
    "incheon_junggu": ("인천 중구", ["yeongjong", "unseo", "sinpo"]),
    
    # [경기도 주요 시/군]
    "suwon": ("수원시", ["ingye", "gwonseon", "yeongtong", "jangan", "paldal"]),
    "seongnam": ("성남시", ["bundang", "pangyo", "sujeong", "jungwon", "seohyeon", "yatap"]),
    "goyang": ("고양시", ["ilsan", "deogyang", "baekseok", "madu", "hwajeong"]),
    "yongin": ("용인시", ["suji", "giheung", "cheoin", "jookjeon", "dongbaek"]),
    "bucheon": ("부천시", ["jungdong", "sangdong", "wonmi", "sosa", "ojeong"]),
    "ansan": ("안산시", ["danwon", "sangnok", "gojan", "jungang"]),
    "anyang": ("안양시", ["pyeongchon", "beomgye", "manan", "dongan"]),
    "hwaseong": ("화성시", ["dongtan", "hyangnam", "bongdam", "byeongjeom"]),
    "pyeongtaek": ("평택시", ["godeok", "songtan", "anjeong", "bijeon"]),
    "siheung": ("시흥시", ["baegot", "jeongwang", "eunhaeng", "mokgam"]),
    "gimpo": ("김포시", ["gurae", "pungmu", "sau", "unyang"]),
    "paju": ("파주시", ["unjeong", "geumchon", "munsan", "gyoha"]),
    "uijeongbu": ("의정부시", ["uijeongbu_dong", "howon", "singok", "minrak"]),
    "namyangju": ("남양주시", ["dasang", "byeolnae", "pyeongnae", "jinjeop"]),
    "hanam": ("하남시", ["misa", "wirye", "deokpung", "sinjang"]),
    "gwangmyeong": ("광명시", ["cheolsan", "soha", "gwangmyeong_dong", "iljik"]),
    "gunpo": ("군포시", ["sanbon", "geumjeong", "dang-dong"]),
    "guri": ("구리시", ["sutaek", "inmae", "galmae", "gyomun"]),
    "gwangju_gyeonggi": ("경기 광주시", ["gyeongan", "taejeon", "opocheup"]),
    "icheon": ("이천시", ["changjeon", "jeungpo", "bubal"]),
    "osan": ("오산시", ["won-dong", "궐동", "세교"]),
    "anseong": ("안성시", ["daedeok", "gongdo"]),
    "uiwang": ("의왕시", ["poil", "naeson", "gojeon"]),
    "yangju": ("양주시", ["okjeong", "goeup", "deokgye"])
}

# 기본 템플릿 코드
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <meta name="robots" content="index, follow">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Noto Sans KR', -apple-system, sans-serif; }}
        body {{ background-color: #0f1117; color: #e1e3e8; line-height: 1.6; padding-bottom: 40px; }}
        a {{ text-decoration: none; color: inherit; }}
        header {{ background: #161821; padding: 18px 20px; text-align: center; border-bottom: 2px solid #e74c3c; position: sticky; top: 0; z-index: 100; }}
        header h1 {{ font-size: 1.35rem; color: #ffffff; font-weight: 700; }}
        header h1 span {{ color: #e74c3c; }}
        .hero-banner {{ background: linear-gradient(rgba(15, 17, 23, 0.75), rgba(15, 17, 23, 0.88)), url('/images/main-banner.jpg') center/cover; padding: 50px 20px; text-align: center; border-bottom: 1px solid #2a2d37; }}
        .hero-banner h2 {{ font-size: 1.6rem; color: #fff; margin-bottom: 10px; }}
        .hero-banner p {{ font-size: 0.95rem; color: #f1c40f; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px 15px; }}
        .nav-bar {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        .home-btn {{ background: #2a2d37; color: #fff; padding: 8px 15px; border-radius: 5px; font-size: 0.85rem; }}
        .section-title {{ font-size: 1.25rem; color: #ffffff; margin: 25px 0 18px 0; border-left: 4px solid #e74c3c; padding-left: 10px; font-weight: 700; }}
        .vendor-card {{ background: #161821; border: 1px solid #2a2d37; border-radius: 12px; overflow: hidden; margin-bottom: 25px; }}
        .vendor-img {{ width: 100%; height: 220px; object-fit: cover; }}
        .vendor-body {{ padding: 20px; }}
        .vendor-header {{ display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #2a2d37; padding-bottom: 12px; margin-bottom: 15px; flex-wrap: wrap; gap: 8px; }}
        .vendor-badge {{ background: #e74c3c; color: #fff; font-size: 0.8rem; font-weight: bold; padding: 4px 10px; border-radius: 4px; }}
        .vendor-title {{ font-size: 1.2rem; color: #ffffff; font-weight: bold; }}
        .vendor-tagline {{ color: #2ecc71; font-size: 0.88rem; font-weight: 600; width: 100%; margin-top: 4px; }}
        .vendor-info {{ margin-bottom: 18px; }}
        .info-row {{ display: flex; margin-bottom: 8px; font-size: 0.92rem; }}
        .info-label {{ width: 95px; color: #f1c40f; font-weight: bold; flex-shrink: 0; }}
        .info-content {{ color: #bbbfca; }}
        .vendor-call-btn {{ display: block; text-align: center; background: linear-gradient(135deg, #e74c3c, #c0392b); color: #ffffff; font-weight: bold; padding: 13px; border-radius: 8px; font-size: 1rem; }}
        footer {{ text-align: center; padding: 25px 20px; font-size: 0.8rem; color: #7f8c8d; border-top: 1px solid #2a2d37; margin-top: 20px; }}
    </style>
</head>
<body>
    <header>
        <h1>{header_title} <span>프리미엄 24시 방문 케어</span></h1>
    </header>
    <div class="hero-banner">
        <h2>{header_title} 맞춤 프라이빗 힐링 서비스</h2>
        <p>계신 곳 어디든 30분 내 신속 방문 테라피 안내</p>
    </div>
    <div class="container">
        <div class="nav-bar">
            <a href="../index.html" class="home-btn">🏠 전체 메인</a>
            <a href="index.html" class="home-btn">📍 {header_title} 메인</a>
        </div>
        <h2 class="section-title">{header_title} 추천 테라피 매장</h2>
        <div class="vendor-card">
            <img src="/images/vendor1.jpg" alt="{header_title} 테라피" class="vendor-img">
            <div class="vendor-body">
                <div class="vendor-header">
                    <div>
                        <span class="vendor-badge">추천 01</span>
                        <span class="vendor-title">마사지몽 프리미엄 케어</span>
                    </div>
                    <div class="vendor-tagline">★ {header_title} 전 지역 신속 배정</div>
                </div>
                <div class="vendor-info">
                    <div class="info-row">
                        <div class="info-label">제공 코스</div>
                        <div class="info-content">시그니처 타이, 프리미엄 아로마, 림프 순환 케어</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">매장 특징</div>
                        <div class="info-content">24시간 운영, 100% 후불제 시스템, 철저한 위생 관리</div>
                    </div>
                </div>
                <a href="tel:0507-1280-3338" class="vendor-call-btn">📞 전화 문의 : 0507-1280-3338</a>
            </div>
        </div>
    </div>
    <footer>
        <p>© {header_title} 프리미엄 테라피 안내. All rights reserved.</p>
    </footer>
</body>
</html>
"""

count = 0
for folder, (kr_name, sub_dongs) in NEW_REGIONS.items():
    os.makedirs(folder, exist_ok=True)
    
    # 1. 구/시 메인 index.html 생성
    index_path = os.path.join(folder, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE.format(
            title=f"{kr_name} 출장 마사지 & 24시 프리미엄 홈타이 | 마사지몽",
            desc=f"{kr_name} 전 지역 24시 출장 마사지 및 홈타이 추천. 아로마, 스웨디시 힐링 케어 안내.",
            keywords=f"{kr_name} 출장 마사지, {kr_name} 홈타이, 24시 테라피",
            header_title=kr_name
        ))
    count += 1

    # 2. 하위 동별 html 파일 생성
    for dong in sub_dongs:
        dong_path = os.path.join(folder, f"{dong}.html")
        with open(dong_path, "w", encoding="utf-8") as f:
            f.write(HTML_TEMPLATE.format(
                title=f"{kr_name} 출장 마사지 & 24시 홈타이 | 마사지몽",
                desc=f"{kr_name} 인근 24시간 신속 방문 힐링 테라피 안내.",
                keywords=f"{kr_name} 출장 마사지, {kr_name} 홈케어",
                header_title=f"{kr_name}"
            ))
        count += 1

print(f"🎉 경기/인천 지역 {len(NEW_REGIONS)}개 구역, 총 {count}개의 HTML 파일이 자동 생성되었습니다!")