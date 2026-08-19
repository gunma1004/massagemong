import os
import re

# ==============================================================================
# 수도권 전체 구/동 상세 매핑 데이터
# ==============================================================================
FULL_REGIONS_HTML = """
        <!-- 수도권 전 지역 (서울·인천·경기) 통합 네비게이션 -->
        <div class="area-box" style="margin-top:35px; background:#161821; border:1px solid #2a2d37; border-radius:12px; padding:20px;">
            <h3 style="font-size:1.2rem; color:#f1c40f; margin-bottom:15px; border-bottom:1px solid #2a2d37; padding-bottom:10px;">📍 수도권 전 지역 세부 바로가기 (서울 · 인천 · 경기)</h3>

            <!-- 1. 서울특별시 -->
            <div style="font-weight:bold; color:#e74c3c; margin:15px 0 8px 0; font-size:1.05rem;">[ 서울특별시 전지역 & 25개 자치구 ]</div>
            <div class="gu-grid">
                <a href="/seoul/index.html" class="gu-item" style="border-color:#e74c3c; color:#f1c40f; font-weight:bold;">★ 서울 전지역</a>
                <a href="/gangnam/index.html" class="gu-item">강남구</a>
                <a href="/seocho/index.html" class="gu-item">서초구</a>
                <a href="/songpa/index.html" class="gu-item">송파구</a>
                <a href="/gangdong/index.html" class="gu-item">강동구</a>
                <a href="/mapo/index.html" class="gu-item">마포구</a>
                <a href="/yongsan/index.html" class="gu-item">용산구</a>
                <a href="/seodaemun/index.html" class="gu-item">서대문구</a>
                <a href="/eunpyeong/index.html" class="gu-item">은평구</a>
                <a href="/jongno/index.html" class="gu-item">종로구</a>
                <a href="/junggu/index.html" class="gu-item">중구</a>
                <a href="/jungnang/index.html" class="gu-item">중랑구</a>
                <a href="/seongbuk/index.html" class="gu-item">성북구</a>
                <a href="/gangbuk/index.html" class="gu-item">강북구</a>
                <a href="/dobong/index.html" class="gu-item">도봉구</a>
                <a href="/nowon/index.html" class="gu-item">노원구</a>
                <a href="/seongdong/index.html" class="gu-item">성동구</a>
                <a href="/gwangjin/index.html" class="gu-item">광진구</a>
                <a href="/dongdaemun/index.html" class="gu-item">동대문구</a>
                <a href="/yeongdeungpo/index.html" class="gu-item">영등포구</a>
                <a href="/guro/index.html" class="gu-item">구로구</a>
                <a href="/geumcheon/index.html" class="gu-item">금천구</a>
                <a href="/yangcheon/index.html" class="gu-item">양천구</a>
                <a href="/gangse/index.html" class="gu-item">강서구</a>
                <a href="/dongjak/index.html" class="gu-item">동작구</a>
                <a href="/gwanak/index.html" class="gu-item">관악구</a>
            </div>

            <!-- 2. 인천광역시 -->
            <div style="font-weight:bold; color:#3498db; margin:20px 0 8px 0; font-size:1.05rem;">[ 인천광역시 8개 구/군 & 세부 동 ]</div>
            <div class="gu-grid">
                <a href="/incheon_bupyeong/index.html" class="gu-item">인천 부평구</a>
                <a href="/incheon_namdong/index.html" class="gu-item">인천 남동구</a>
                <a href="/incheon_yeonsu/index.html" class="gu-item">인천 연수구(송도)</a>
                <a href="/incheon_michuhol/index.html" class="gu-item">인천 미추홀구</a>
                <a href="/incheon_seogu/index.html" class="gu-item">인천 서구(청라/검단)</a>
                <a href="/incheon_gyeyang/index.html" class="gu-item">인천 계양구</a>
                <a href="/incheon_junggu/index.html" class="gu-item">인천 중구(영종도)</a>
                <a href="/incheon_donggu/index.html" class="gu-item">인천 동구</a>
            </div>

            <!-- 3. 경기도 주요 시/구 -->
            <div style="font-weight:bold; color:#2ecc71; margin:20px 0 8px 0; font-size:1.05rem;">[ 경기도 주요 시·구 & 세부 동 ]</div>
            <div class="gu-grid">
                <a href="/suwon/index.html" class="gu-item">수원시 전체</a>
                <a href="/suwon_paldal/index.html" class="gu-item">수원 팔달구(인계동)</a>
                <a href="/suwon_yeongtong/index.html" class="gu-item">수원 영통구(광교)</a>
                <a href="/suwon_jangan/index.html" class="gu-item">수원 장안구</a>
                <a href="/suwon_gwonseon/index.html" class="gu-item">수원 권선구</a>
                
                <a href="/seongnam/index.html" class="gu-item">성남시 전체</a>
                <a href="/seongnam_bundang/index.html" class="gu-item">성남 분당구(판교)</a>
                <a href="/seongnam_sujeong/index.html" class="gu-item">성남 수정구(위례)</a>
                <a href="/seongnam_jungwon/index.html" class="gu-item">성남 중원구(모란)</a>
                
                <a href="/goyang/index.html" class="gu-item">고양시 전체</a>
                <a href="/goyang_ilsandong/index.html" class="gu-item">고양 일산동구</a>
                <a href="/goyang_ilsanseo/index.html" class="gu-item">고양 일산서구</a>
                <a href="/goyang_deogyang/index.html" class="gu-item">고양 덕양구(삼송)</a>
                
                <a href="/yongin/index.html" class="gu-item">용인시 전체</a>
                <a href="/yongin_suji/index.html" class="gu-item">용인 수지구(죽전)</a>
                <a href="/yongin_giheung/index.html" class="gu-item">용인 기흥구(동백)</a>
                <a href="/yongin_cheoin/index.html" class="gu-item">용인 처인구(역북)</a>
                
                <a href="/bucheon/index.html" class="gu-item">부천시(중동/상동)</a>
                <a href="/hwaseong/index.html" class="gu-item">화성시(동탄1·2/병점)</a>
                <a href="/pyeongtaek/index.html" class="gu-item">평택시(고덕/비전동)</a>
                <a href="/siheung/index.html" class="gu-item">시흥시(배곧/정왕동)</a>
                <a href="/gimpo/index.html" class="gu-item">김포시(구래/운양동)</a>
                <a href="/paju/index.html" class="gu-item">파주시(운정/야당동)</a>
                <a href="/namyangju/index.html" class="gu-item">남양주시(다산/별내)</a>
                <a href="/uijeongbu/index.html" class="gu-item">의정부시(민락동)</a>
                <a href="/hanam/index.html" class="gu-item">하남시(미사/감일)</a>
                <a href="/gwangmyeong/index.html" class="gu-item">광명시(철산/일직)</a>
                <a href="/anyang/index.html" class="gu-item">안양시(평촌/범계)</a>
                <a href="/ansan/index.html" class="gu-item">안산시(중앙동/고잔동)</a>
                <a href="/gunpo/index.html" class="gu-item">군포시(산본동)</a>
                <a href="/guri/index.html" class="gu-item">구리시(수택동)</a>
                <a href="/osan/index.html" class="gu-item">오산시(세교)</a>
                <a href="/gwangju_gyeonggi/index.html" class="gu-item">경기 광주시</a>
                <a href="/icheon/index.html" class="gu-item">이천시</a>
                <a href="/yangju/index.html" class="gu-item">양주시(옥정)</a>
                <a href="/uiwang/index.html" class="gu-item">의왕시</a>
                <a href="/anseong/index.html" class="gu-item">안성시</a>
            </div>
        </div>
"""

# 메인 index.html 과 seoul/index.html 에 삽입/치환
target_files = ["index.html", "seoul/index.html"]

for rel_path in target_files:
    if not os.path.exists(rel_path):
        continue
    
    with open(rel_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 기존 수도권 안내/자치구 영역이 있으면 교체, 없으면 푸터 바로 앞에 삽입
    if '<div class="area-box">' in content:
        content = re.sub(r'<div class="area-box">.*?</div>\s*</div>(?=\s*<footer>)', FULL_REGIONS_HTML.strip() + "\n    </div>", content, flags=re.DOTALL)
    elif '<div class="gu-grid">' in content:
        content = re.sub(r'<h2 class="section-title">.*?서울시 25개 자치구.*?</h2>\s*<div class="gu-grid">.*?</div>', FULL_REGIONS_HTML.strip(), content, flags=re.DOTALL)
    else:
        content = re.sub(r'(</div>\s*<footer>)', rf'{FULL_REGIONS_HTML}\n    \1', content, flags=re.DOTALL)

    with open(rel_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✔ [{rel_path}] 서울/경기/인천 전체 구·동 통합 네비게이션 적용 완료!")

