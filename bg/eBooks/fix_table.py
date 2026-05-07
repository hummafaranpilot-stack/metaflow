import os

files = ['30-day-power-plan.html', 'prostate-health-guide.html']
for fn in files:
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    bad_str = '''        <table class="print-padding-table">
            <thead><tr><td><div class="print-margin-top"></div></td></tr></thead>
            <tbody>
                <tr><td class="print-content-cell">

        </div>'''
        
    good_str = '''        </div>
        <table class="print-padding-table">
            <thead><tr><td><div class="print-margin-top"></div></td></tr></thead>
            <tbody>
                <tr><td class="print-content-cell">
'''
    
    if bad_str in html:
        html = html.replace(bad_str, good_str)
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(html)
        print('Fixed ' + fn)
    else:
        print('Not found in ' + fn)
