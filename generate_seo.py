import os

domain = "https://seoul-homecare.shop"

# 1. robots.txt 생성
robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml\n"
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)
print("✅ robots.txt 생성 완료!")

# 2. sitemap.xml 생성
sitemap_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    f'  <url><loc>{domain}/</loc><priority>1.0</priority></url>'
]

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            rel_dir = os.path.relpath(root, ".").replace("\\", "/")
            path = file if rel_dir == "." else f"{rel_dir}/{file}"
            priority = "1.0" if path == "index.html" else ("0.9" if "index.html" in path else "0.8")
            sitemap_lines.append(f'  <url><loc>{domain}/{path}</loc><priority>{priority}</priority></url>')

sitemap_lines.append('</urlset>')

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap_lines))

print("✅ sitemap.xml 생성 완료!")