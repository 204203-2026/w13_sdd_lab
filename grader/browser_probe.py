"""Optional CI-only browser exercise. Unavailable browser/CDN means TODO."""
import socket
import subprocess
import sys
import time
import httpx
from playwright.sync_api import sync_playwright

with socket.socket() as listener:
    listener.bind(('127.0.0.1', 0))
    port = listener.getsockname()[1]
server = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'app.main:app', '--port', str(port)],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    url = f'http://127.0.0.1:{port}'
    for attempt in range(50):
        try:
            if httpx.get(url + '/').status_code == 200:
                break
        except httpx.HTTPError:
            pass
        time.sleep(0.1)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_function('!!window.Vue', timeout=10000)
        title = page.get_by_test_id('note-title')
        title.fill('browser note')
        page.get_by_test_id('note-form').evaluate('(form) => form.requestSubmit()')
        page.get_by_test_id('note-item').wait_for()
        assert page.get_by_test_id('note-item').count() == 1
        page.get_by_test_id('note-delete').click()
        page.wait_for_function('document.querySelectorAll(\'[data-testid="note-item"]\').length === 0')
        title.fill(' ')
        page.get_by_test_id('note-form').evaluate('(form) => form.requestSubmit()')
        page.get_by_test_id('note-error').wait_for(state='visible')
        assert page.get_by_test_id('note-item').count() == 0
        browser.close()
finally:
    server.terminate()
    server.wait(timeout=10)
