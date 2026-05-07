import re
with open(r'd:\TrustedNutraProducts\VigorXPro\eBooks\prostate-health-guide.html', 'r', encoding='utf-8') as f:
    html = f.read()

chapters = [
    'Welcome to Better Prostate Health',
    'Understanding Your Prostate &amp; Bladder',
    '10 Warning Signs Men Should Never Ignore',
    'Power Foods for Prostate Health',
    'Environmental Toxins Destroying Your Prostate',
    'Lifestyle Habits That Make a Difference',
    'How VigorXPro Supports Your Health',
    'Real Questions, Real Answers',
    'Your Action Plan',
    'Final Thoughts from TrustedNutraProducts'
]
for i, title in enumerate(chapters, 1):
    html = html.replace(f'<span class="toc-label">{title}</span>', f'<a href="#chapter-{i}" class="toc-label">{title}</a>')

for i in range(1, 11):
    html = re.sub(f'(<!-- ========== CHAPTER {i}.*?========== -->\\s*<div class="page">\\s*)<div class="chapter-header">', f'\\g<1><div class="chapter-header" id="chapter-{i}">', html, count=1)

with open(r'd:\TrustedNutraProducts\VigorXPro\eBooks\prostate-health-guide.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated guide HTML with TOC anchors.")
