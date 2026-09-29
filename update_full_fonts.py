with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# إدراج خط Cairo المباشر مع تنسيق شامل يشمل نافذة الإعدادات وكامل العناصر
global_font_style = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
  * {
    font-family: 'Cairo', system-ui, sans-serif !important;
  }
  body, button, input, select, textarea, table, th, td, div, span, h2, h3, h4, label {
    font-family: 'Cairo', sans-serif !important;
  }
  /* توضيح الخط في البطاقات والقوائم والأزرار */
  .card, .btn-action, button {
    font-weight: 800 !important;
  }
  /* توضيح وتكبير عناصر نافذة الإعدادات */
  #general-settings-modal * {
    font-family: 'Cairo', sans-serif !important;
  }
  #general-settings-modal input, 
  #general-settings-modal select, 
  #general-settings-modal table {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
  }
  #general-settings-modal button {
    font-weight: 800 !important;
    letter-spacing: 0.3px;
  }
</style>
"""

import re
if 'family=Cairo' in html:
    html = re.sub(r'<link[^>]*family=Cairo[^>]*>[\s\S]*?</style>', global_font_style, html)
else:
    html = html.replace('</head>', global_font_style + '\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("ALL_FONTS_AND_SETTINGS_UPDATED")
