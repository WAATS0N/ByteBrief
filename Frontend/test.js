const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    let logs = [];
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.on('console', msg => {
        logs.push('LOG: ' + msg.text());
    });
    page.on('pageerror', err => {
        logs.push('EXCEPTION: ' + err.toString());
    });

    try {
        await page.goto('http://localhost:3000/categories', { waitUntil: 'domcontentloaded', timeout: 10000 });
        await new Promise(r => setTimeout(r, 4000));
    } catch (e) {
        logs.push("GOTO ERROR: " + e.toString());
    }

    fs.writeFileSync('error_log.txt', logs.join('\n'));
    await browser.close();
})();
