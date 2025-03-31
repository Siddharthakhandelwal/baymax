import requests
def page_change(pg):
    url="https://baymax-ui.vercel.app/api/page-tracking"
    data ={
        "page": pg,
    }
    response = requests.post(url, json=data)
    print(response.text)

page_change(10)