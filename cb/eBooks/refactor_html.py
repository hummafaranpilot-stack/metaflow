import re
import os

files = ['d:/TrustedNutraProducts/VigorXPro/eBooks/30-day-power-plan.html', 'd:/TrustedNutraProducts/VigorXPro/eBooks/prostate-health-guide.html']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace all `<div class="page"` with `<div class="content-section"`
    content = content.replace('<div class="page"', '<div class="content-section"')
    
    # 2. Fix the cover page back to what it should be
    content = content.replace('<div class="content-section cover-page">', '<div class="page cover-page">')
    
    # 3. We need to wrap everything after the cover page in a print-margin table.
    # Find where the cover page ends. The cover page has a known structure.
    # It ends with `</div>` after `<div class="cover-footer">TrustedNutraProducts.com</div>`
    cover_footer_idx = content.find('<div class="cover-footer">TrustedNutraProducts.com</div>')
    if cover_footer_idx != -1:
        end_of_cover_page = content.find('</div>', cover_footer_idx) + 6
        
        # We also need to find the closing tag of `.ebook` to insert the footer of the table
        # Let's search from the back
        end_of_ebook = content.rfind('</div>\n</body>')
        if end_of_ebook == -1:
            end_of_ebook = content.rfind('</div>\n    </body>')
        if end_of_ebook == -1:
             end_of_ebook = content.rfind('</div>\n\n</body>')
             
        if end_of_ebook != -1:
            before = content[:end_of_cover_page]
            middle = content[end_of_cover_page:end_of_ebook]
            after = content[end_of_ebook:]
            
            table_wrapper_start = """
        <table class="print-padding-table">
            <thead><tr><td><div class="print-margin-top"></div></td></tr></thead>
            <tbody>
                <tr><td class="print-content-cell">
"""
            table_wrapper_end = """
                </td></tr>
            </tbody>
            <tfoot><tr><td><div class="print-margin-bottom"></div></td></tr></tfoot>
        </table>
"""
            content = before + table_wrapper_start + middle + table_wrapper_end + after
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Refactored {os.path.basename(filepath)}")
        else:
            print(f"Could not find end of ebook in {filepath}")
    else:
        print(f"Could not find cover footer in {filepath}")
