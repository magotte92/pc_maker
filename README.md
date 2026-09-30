# pc_maker

A Python 3 console app to build your dream PC.

Requires Python 3.12 or newer (3.12 is still in security support and is what this repo is verified with; CI also runs 3.13).

```bash
python -m pip install -r requirements-dev.txt
python pc_builder.py
```

`init_browser()` targets Selenium 4. If `chromedriver` or `chromedriver.exe` sits next to `pc_builder.py`, that binary is used. Otherwise Selenium Manager downloads a driver that matches the installed Chrome or Chromium. The old bundled `chromedriver.exe` (32-bit, ChromeDriver 2.39 era, 2018) has been removed.
