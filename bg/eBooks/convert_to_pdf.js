const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  console.log('Launching browser...');
  const browser = await puppeteer.launch({headless: 'new'});
  const page = await browser.newPage();
  
  // Guide Conversion
  const guidePath = 'file://' + path.resolve(__dirname, 'prostate-health-guide.html');
  console.log('Loading guide:', guidePath);
  await page.goto(guidePath, {waitUntil: 'networkidle0'});
  await page.evaluate(() => {
    // Slight tweak to ensure print media is forced if needed
    window.matchMedia('print');
  });
  await page.pdf({
    path: path.join(__dirname, 'prosta guide.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' }
  });
  console.log('Converted prostate health guide to PDF.');

  // 30 Day Plan Conversion
  const planPath = 'file://' + path.resolve(__dirname, '30-day-power-plan.html');
  console.log('Loading 30 day plan:', planPath);
  await page.goto(planPath, {waitUntil: 'networkidle0'});
  await page.pdf({
    path: path.join(__dirname, '30 days plan.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' }
  });
  console.log('Converted 30 day power plan to PDF.');

  await browser.close();
  console.log('Done.');
})().catch(err => {
  console.error(err);
  process.exit(1);
});
