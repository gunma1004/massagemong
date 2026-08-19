import os
import re

# ==============================================================================
# 1. 영문 폴더명/파일명 -> 완벽한 한글 지역명 매핑 딕셔너리
# ==============================================================================
NAME_MAP = {
    # [서울]
    "seoul": "서울", "gangnam": "강남구", "seocho": "서초구", "songpa": "송파구", "gangdong": "강동구",
    "mapo": "마포구", "yongsan": "용산구", "seodaemun": "서대문구", "eunpyeong": "은평구",
    "jongno": "종로구", "junggu": "중구", "jungnang": "중랑구", "seongbuk": "성북구",
    "gangbuk": "강북구", "dobong": "도봉구", "nowon": "노원구", "seongdong": "성동구",
    "gwangjin": "광진구", "dongdaemun": "동대문구", "yeongdeungpo": "영등포구",
    "guro": "구로구", "geumcheon": "금천구", "yangcheon": "양천구", "gangse": "강서구",
    "gangseo": "강서구", "dongjak": "동작구", "gwanak": "관악구",

    # [인천]
    "incheon_bupyeong": "인천 부평구", "incheon_namdong": "인천 남동구", "incheon_yeonsu": "인천 연수구",
    "incheon_michuhol": "인천 미추홀구", "incheon_seogu": "인천 서구", "incheon_gyeyang": "인천 계양구",
    "incheon_junggu": "인천 중구", "incheon_donggu": "인천 동구",

    # [경기 시/구]
    "suwon": "수원시", "suwon_paldal": "수원 팔달구", "suwon_yeongtong": "수원 영통구", "suwon_jangan": "수원 장안구", "suwon_gwonseon": "수원 권선구",
    "seongnam": "성남시", "seongnam_bundang": "성남 분당구", "seongnam_sujeong": "성남 수정구", "seongnam_jungwon": "성남 중원구",
    "goyang": "고양시", "goyang_ilsandong": "고양 일산동구", "goyang_ilsanseo": "고양 일산서구", "goyang_deogyang": "고양 덕양구",
    "yongin": "용인시", "yongin_suji": "용인 수지구", "yongin_giheung": "용인 기흥구", "yongin_cheoin": "용인 처인구",
    "anyang": "안양시", "anyang_dongan": "안양 동안구", "anyang_manan": "안양 만안구",
    "ansan": "안산시", "ansan_danwon": "안산 단원구", "ansan_sangnok": "안산 상록구",
    "bucheon": "부천시", "hwaseong": "화성시", "pyeongtaek": "평택시", "siheung": "시흥시",
    "gimpo": "김포시", "paju": "파주시", "namyangju": "남양주시", "uijeongbu": "의정부시",
    "hanam": "하남시", "gwangmyeong": "광명시", "gunpo": "군포시", "guri": "구리시",
    "osan": "오산시", "gwangju_gyeonggi": "경기 광주시", "icheon": "이천시", "yangju": "양주시",
    "uiwang": "의왕시", "anseong": "안성시",

    # [세부 동 매핑]
    "bupyeong": "부평동", "sanggok": "산곡동", "cheongcheon": "청천동", "galsan": "갈산동", "sipjeong": "십정동", "bugae": "부개동", "samsan": "삼산동",
    "guwol": "구월동", "ganseok": "간석동", "mansu": "만수동", "nonhyeon_incheon": "논현동", "seochang": "서창동", "dorim": "도림동",
    "songdo": "송도동", "yeonsu": "연수동", "dongchun": "동춘동", "cheonghak": "청학동", "okryeon": "옥련동", "seonhak": "선학동",
    "juan": "주안동", "yonghyeon": "용현동", "hakik": "학익동", "dohwa": "도화동", "sungui": "숭의동", "gwangyo": "관교동",
    "cheongna": "청라동", "geomdan": "검단", "luwon": "루원시티", "gajeong": "가정동", "seoknam": "석남동", "yeonhui": "연희동", "dangha": "당하동", "majeon": "마전동",
    "gyeyang": "계양", "jakjeon": "작전동", "hyoseong": "효성동", "gyesan": "계산동", "seoun": "서운동",
    "yeongjong": "영종도", "unseo": "운서동", "jungsan": "중산동", "sinpo": "신포동", "dongincheon": "동인천",
    "songhyeon": "송현동", "songrim": "송림동", "manseok": "만석동", "hwasu": "화수동",
    "ingye": "인계동", "haenggung": "행궁동", "hwaseo": "화서동", "ji-dong": "지동", "maesan": "매산동",
    "gwanggyo": "광교", "yeongtong": "영통동", "mangpo": "망포동", "maetan": "매탄동", "woncheon": "원천동",
    "jeongja": "정자동", "jo-won": "조원동", "yuljeon": "율전동", "cheoncheon": "천천동", "yeonmu": "연무동",
    "gwonseon": "권선동", "gosaek": "고색동", "homaesil": "호매실동", "seriu": "세류동", "geumgok": "금곡동",
    "seohyeon": "서현동", "yatap": "야탑동", "pangyo": "판교", "baekhyeon": "백현동", "sunae": "수내동", "ime": "이매동", "gumi": "구미동", "unjoong": "운중동",
    "wirye": "위례", "sinheung": "신흥동", "taepyeong": "태평동", "sanseong": "산성동", "bokjeong": "복정동", "sujin": "수진동",
    "moran": "모란", "seongnam_dong": "성남동", "sangdaewon": "상대원동", "hagdaewon": "하대원동", "geumgwang": "금광동", "bank": "은행동",
    "baekseok": "백석동", "madu": "마두동", "janghang": "장항동", "jeongbalsan": "정발산동", "siksa": "식사동", "pungsan": "풍산동",
    "juyeop": "주엽동", "daehwa": "대화동", "tanhyun": "탄현동", "ilsan": "일산동", "songsan": "송산동", "deogi": "덕이동",
    "hwajeong": "화정동", "haengsin": "행신동", "samsong": "삼송", "wonheung": "원흥", "hyangdong": "향동", "deogeun": "덕은", "wondang": "원당",
    "pungdeokcheon": "풍덕천동", "jookjeon": "죽전동", "dongcheon": "동천동", "sanghyeon": "상현동", "shinbong": "신봉동", "sungbok": "성복동",
    "dongbaek": "동백동", "singal": "신갈동", "gugal": "구갈동", "bora": "보라동", "seonong": "서농동", "guseong": "구성", "mabuk": "마북동",
    "kimryangjang": "김량장동", "yeokbuk": "역북동", "samga": "삼가동", "pogok": "포곡", "mohan": "모현", "yangji": "양지",
    "pyeongchon": "평촌동", "beomgye": "범계", "indeogwon": "인덕원", "gwanyang": "관양동", "hogye": "호계동", "bisan": "비산동",
    "anyang_dong": "안양동", "seoksu": "석수동", "bakdal": "박달동",
    "gojan": "고잔동", "jungang": "중앙동", "chogi": "초지동", "wongok": "원곡동", "seonbu": "선부동", "daebu": "대부도",
    "bono": "본오동", "sadong": "사동", "wolpi": "월피동", "seongpo": "성포동", "il-dong": "일동", "i-dong": "이동",
    "jungdong": "중동", "sangdong": "상동", "sinjungdong": "신중동", "sosa": "소사동", "wonmi": "원미동", "ojeong": "오정동", "yeokgok": "역곡동", "gogang": "고강동",
    "dongtan": "동탄1", "dongtan2": "동탄2", "byeongjeom": "병점", "hyangnam": "향남", "bongdam": "봉담", "namyang": "남양", "saesol": "새솔동", "jinjoo": "진안동",
    "godeok": "고덕", "bijeon": "비전동", "songtan": "송탄", "anjeong": "안정리", "anseok": "안중", "poseung": "포승", "cheongbuk": "청북", "sejeong": "세교동",
    "baegot": "배곧동", "jeongwang": "정왕동", "eunhaeng": "은행동", "mokgam": "목감동", "daeya": "대야동", "sinhyeon": "신현동", "neunggok": "능곡동", "janghyeon": "장현동",
    "gurae": "구래동", "unyang": "운양동", "janggi": "장기동", "pungmu": "풍무동", "sau": "사우동", "masan": "마산동", "gochon": "고촌", "tongjin": "통진",
    "unjeong": "운정", "geumchon": "금촌동", "munsan": "문산", "gyoha": "교하", "yadang": "야당동", "dongpae": "동패동",
    "dasang": "다산동", "byeolnae": "별내동", "pyeongnae": "평내동", "hopyeong": "호평동", "jinjeop": "진접", "wabu": "와부", "onam": "오남", "hwado": "화도",
    "uijeongbu_dong": "의정부동", "howon": "호원동", "singok": "신곡동", "minrak": "민락동", "gosan": "고산동", "ganeung": "가능동", "geumo": "금오동",
    "misa": "미사", "wirye_hanam": "위례", "gamil": "감일", "deokpung": "덕풍동", "sinjang": "신장동", "pungcheon": "풍산동",
    "cheolsan": "철산동", "gwangmyeong_dong": "광명동", "soha": "소하동", "iljik": "일직동", "haan": "하안동",
    "sanbon": "산본동", "geumjeong": "금정동", "dang-dong": "당동", "daeyami": "대야미", "bugok": "부곡동",
    "sutaek": "수택동", "inmae": "인창동", "galmae": "갈매동", "gyomun": "교문동", "achasan": "아천동",
    "won-dong": "원동", "seggyo": "세교", "gweol": "궐동", "osandong": "오산동", "eunjeong": "은계동",
    "gyeongan": "경안동", "taejeon": "태전동", "opocheup": "오포", "sinhyun": "신현동", "neungpyeong": "능평동", "tanbeol": "탄벌동",
    "changjeon": "창전동", "jeungpo": "증포동", "bubal": "부발", "majung": "마장", "anheung": "안흥동",
    "okjeong": "옥정동", "goeup": "고읍동", "deokgye": "덕계동", "baekseok_yangju": "백석",
    "poil": "포일동", "naeson": "내손동", "gojeon": "고천동", "sam-dong": "삼동",
    "gongdo": "공도", "daedeok": "대덕", "anseong_dong": "안성동", "boggae": "보개"
}

def get_loc_name(rel_path):
    parts = rel_path.replace("\\", "/").split("/")
    if len(parts) == 2 and parts[1] == "index.html":
        folder = parts[0]
        return NAME_MAP.get(folder, folder)
    else:
        folder = parts[0]
        file_name = parts[-1].replace(".html", "")
        folder_kr = NAME_MAP.get(folder, folder)
        file_kr = NAME_MAP.get(file_name, file_name)
        return f"{folder_kr} {file_kr}" if folder_kr != file_kr else folder_kr

count = 0

for root, dirs, files in os.walk("."):
    for file in files:
        if not file.endswith(".html"):
            continue
        
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, ".").replace("\\", "/")
        
        if rel_path == "index.html":
            continue
        
        loc_name = get_loc_name(rel_path)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 1. 헤더 h1 태그 한글 지역명으로 치환
        new_h1 = f"<h1>{loc_name} 출장 마사지 <span>프리미엄 24시 방문 케어</span></h1>"
        content = re.sub(r'<h1>.*?</h1>', new_h1, content, flags=re.DOTALL)

        # 2. 히어로 배너 h2 태그 한글 지역명으로 치환
        new_h2 = f"<h2>{loc_name} 맞춤 프라이빗 힐링 서비스</h2>"
        content = re.sub(r'<div class="hero-banner">\s*<h2>.*?</h2>', f'<div class="hero-banner">\n        {new_h2}', content, flags=re.DOTALL)

        # 3. 네비바의 "📍 OO 메인" 한글 처리
        parts = rel_path.split("/")
        parent_folder = parts[0]
        parent_kr = NAME_MAP.get(parent_folder, parent_folder)
        content = re.sub(r'📍\s*[A-Za-z0-9_]+\s*메인', f'📍 {parent_kr} 메인', content)

        # 4. 섹션 타이틀 "OO 추천 테라피 매장 TOP 5" 한글 치환
        content = re.sub(r'<h2 class="section-title">.*?추천 테라피.*?</h2>', f'<h2 class="section-title">{loc_name} 추천 테라피 매장 TOP 5</h2>', content, flags=re.DOTALL)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        count += 1

print(f"🎉 총 {count}개 페이지의 상단 영문 헤더(Ansan 등)를 깔끔한 한글 지역명(안산시 등)으로 완벽하게 수정했습니다.")
