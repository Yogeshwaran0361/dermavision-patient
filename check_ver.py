import requests, re, time

t = int(time.time())
url = f'https://dermavision-patient-tau.vercel.app/?v={t}'
headers = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}

res = requests.get(url, headers=headers)
print('HTML Status:', res.status_code)
print('HTML Length:', len(res.text))

match = re.search(r'src="(/assets/[^"]+)"', res.text)
if match:
    js_path = match.group(1)
    js_url = f'https://dermavision-patient-tau.vercel.app{js_path}?v={t}'
    print('JS URL:', js_url)
    js_res = requests.get(js_url, headers=headers)
    print('JS Status:', js_res.status_code)
    print('JS Content-Type:', js_res.headers.get('content-type'))
    print('JS Length:', len(js_res.text))
    print('JS First 100 chars:', js_res.text[:100])
