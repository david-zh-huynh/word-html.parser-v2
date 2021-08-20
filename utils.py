import requests
from datetime import date


def connect():
    # input_id_dict = {}

    # content number
    print('Please enter Content Number of Article:')
    cont_number = input()
    api_article_nr = {"content_number": cont_number}

    # send content number to backend
    api_article_nr_send = requests.post('https://monkeybackend.ch/api/blog_new/create-post-number/', data=api_article_nr)
    print(api_article_nr_send.status_code)

    # if valid status code from api
    if api_article_nr_send.status_code == 201:
        article_nr_response = api_article_nr_send
        article_id_returned = article_nr_response.json()
        article_id = article_id_returned['id']
        # insert meta
        print(article_id_returned)
        print("id: ", str(article_id))
        # save id as variable
        return article_id
    else:
        print("Error code: " + str(api_article_nr_send.status_code))


def meta(meta_dict):
    connect_get = connect()
    meta_get = meta_dict

    meta_data = {
        "lang": "en",
        "slug": [meta_get['URL']],
        "seo_site_title": [meta_get['Title']],
        "seo_meta_description": [meta_get['Meta Description']],
        "title": [meta_get['Headline']],
        "short_description": [meta_get['Teaser']],
        "date": [date.today()],
        "reading_time": ([meta_get['Reading Time']]),
        "level": [meta_get['Level']],
        "category": 5,
        "image_featured_alt": [meta_get['Headline']],
        "image_regular_alt": [meta_get['Headline']],
        "image_regular_increased_alt": [meta_get['Headline']],
        "image_main_alt": [meta_get['Headline']],
        "author": 2,
        "global_texts": 2,
        "posts": connect_get
    }
    x = requests.post("https://monkeybackend.ch/api/blog_new/create-post-meta/", data=meta_data)
    print(str(x.status_code) + " Return: " + x.text)

    if x.status_code == 201:
        meta_id_response = x
        meta_id_returned = meta_id_response.json()
        meta_id = meta_id_returned['id']
        print('meta_id: ' + str(meta_id))
        return meta_id
    else:
        print('Error: ' + str(x.status_code))

def text(text_entries_dict):
    text_dict = text_entries_dict

    text_data = {}