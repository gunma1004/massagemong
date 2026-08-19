import os
from datetime import datetime

# 💡 운영하실 도메인 주소로 입력하세요 (끝에 / 제외)
domain = "https://massagemong.massagemong-kr.workers.dev"
today = datetime.today().strftime('%Y-%m-%d')

# 1. robots.txt 생성
robots_content = f"""User-agent: *
Allow: /

Sitemap: {domain}/sitemap.xml
"""

with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content.strip() + "\n")
print("✅ robots.txt 생성 완료!")

# 2. sitemap.xml 생성
sitemap_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    f'  <url>\n    <loc>{domain}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>'
]

# 디렉터리 순회하며 HTML 파일 탐색
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            rel_dir = os.path.relpath(root, ".").replace("\\", "/")
            path = file if rel_dir == "." else f"{rel_dir}/{file}"
            
            # 루트 index.html은 이미 domain/ 으로 등록했으므로 건너뜀 (중복 방지)
            if path == "index.html":
                continue
            
            # 각 구별 메인 index.html은 0.9, 동별 세부 페이지는 0.8 우선순위 부여
            if file == "index.html":
                priority = "0.9"
                freq = "weekly"
            else:
                priority = "0.8"
                freq = "weekly"

            sitemap_lines.append(
                f'  <url>\n'
                f'    <loc>{domain}/{path}</loc>\n'
                f'    <lastmod>{today}</lastmod>\n'
                f'    <changefreq>{freq}</changefreq>\n'
                f'    <priority>{priority}</priority>\n'
                f'  </url>'
            )

sitemap_lines.append('</urlset>')

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap_lines))

print(f"✅ sitemap.xml 생성 완료! (기준일자: {today})")