import os
with open(r'd:\TrustedNutraProducts\VigorXPro\eBooks\30-day-power-plan.html', 'w', encoding='utf-8') as outfile:
    for part in ['30-day-part1.html', '30-day-part2.html', '30-day-part3.html']:
        with open(os.path.join(r'd:\TrustedNutraProducts\VigorXPro\eBooks', part), 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
print('Combined.')
