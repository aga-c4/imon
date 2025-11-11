import requests

headers = {
        'Content-Type': 'application/json'
    }

# response = requests.get('https://222.252.97.177/b2b/.dev/php/getmetrics.php?token=7f108a1eea2d3688a958653bfef306f8b50f7cdb', headers=headers, verify=False)
response = requests.get('https://222.252.97.177/api/api/v1/metrics/getMetrics?token=e17bb043d66d5074c822fa0c2e26d405', headers=headers, verify=False)
if response.status_code == 200: 
    print(response.content)


