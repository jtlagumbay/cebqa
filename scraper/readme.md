# Superbalita article scraper
  
### Setting up Chrome Driver
1. Check Google Chrome Version.
    + `Google Chrome > Kebab Menu Bar > Help > About Google Chrome`
  
2. Find the ChromeDriver URL download here: https://googlechromelabs.github.io/chrome-for-testing/#stable

3. Download ChromeDriver thru terminal. Navigate first to your desired directory. Replace the urll below with the one you found in step 2.
   + `curl -O https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.100/mac-arm64/chromedriver-mac-arm64.zip`
  
4. Unzip ChromeDriver file:
   + `unzip chromedriver_mac64.zip`
  
5. Make ChromeDriver executable
   + `cd chromedriver_mac64.zip`
   + `chmod +x chromedriver`

6. Move local bin
   + `sudo mv chromedriver /usr/local/bin/`
  
7. Verify Installation
   + `chromedriver --version`


