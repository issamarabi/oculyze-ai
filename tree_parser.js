const puppeteer = require('puppeteer');
const fs = require('fs');
const readline = require('readline');
const path = require('path');

async function processURLs(urls) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const outputFolder = 'task6_files';

  // Ensure the folder exists
  if (!fs.existsSync(outputFolder)) {
    fs.mkdirSync(outputFolder);
  }

  for (let index = 0; index < urls.length; index++) {
    const url = urls[index];
    const page = await browser.newPage();
    
    try {
      await page.goto(url);
      const snapshot = await page.accessibility.snapshot();
      const jsonSnapshot = JSON.stringify(snapshot, null, 2);
      const filename = path.join(outputFolder, `accessibility-tree-${index + 1}.json`);
      fs.writeFileSync(filename, jsonSnapshot);
      console.log(`Accessibility tree for ${url} saved to '${filename}'`);
    } catch (error) {
      console.error(`An error occurred while processing ${url}: ${error}`);
    }
    
    await page.close();
  }

  await browser.close();
}

const file = process.argv[2];
if (!file) {
  console.log("Please provide a text file with URLs as a command-line argument.");
  process.exit(1);
}

const urls = [];
const readInterface = readline.createInterface({
  input: fs.createReadStream(file),
  output: process.stdout,
  console: false,
});

readInterface.on('line', (url) => {
  urls.push(url);
});

readInterface.on('close', () => {
  processURLs(urls);
});
