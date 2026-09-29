with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

font_block = """
<!-- Cairo Font -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
  * {
    font-family: 'Cairo', system-ui, sans-serif !important;
  }
  body, button, input, select, textarea, div, span, h3, h4, table, td, th {
    font-family: 'Cairo', sans-serif !important;
  }
  .card, .btn-action, button {
    font-weight: 800 !important;
  }
  .card div, .card strong {
    font-size: 1.05rem !important;
    font-weight: 800 !important;
  }
</style>
"""

if 'fonts.googleapis.com/css2?family=Cairo' not in text:
    text = text.replace('</head>', font_block + '\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("FONT_UPDATED_SUCCESSFULLY")
