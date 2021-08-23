import requests
from datetime import date

meta_id = ""
long_desc_fk = ""


def connect():
    # input_id_dict = {}

    # content number
    print('Please enter Content Number of Article:')
    cont_number = input()
    api_article_nr = {"content_number": cont_number}

    # send content number to backend
    api_article_nr_send = requests.post('https://monkeybackend.ch/api/blog_new/create-post-number/',
                                        data=api_article_nr)
    print("Create post number: ", api_article_nr_send.status_code)

    # if valid status code from api
    if api_article_nr_send.status_code == 201:
        article_nr_response = api_article_nr_send
        article_id_returned = article_nr_response.json()
        article_id = article_id_returned['id']
        # insert meta
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
    c = requests.post("https://monkeybackend.ch/api/blog_new/create-post-meta/", data=meta_data)

    if c.status_code == 201:
        meta_id_response = c
        meta_id_returned = meta_id_response.json()
        global meta_id
        meta_id = meta_id_returned['id']
        print('meta_id: ' + str(meta_id))
        return meta_id

    else:
        print('Error: ' + str(c.status_code))


def long_desc():
    meta_get_id = meta_id
    # print(meta_get)

    desc_data = {"long_description": meta_get_id}
    ld = requests.post("https://monkeybackend.ch/api/blog_new/create-long-description", data=desc_data)
    print("long description status: " + str(ld.status_code))

    if ld.status_code == 201:
        long_desc_fk_response = ld
        long_desc_fk_returned = long_desc_fk_response.json()
        global long_desc_fk
        long_desc_fk = long_desc_fk_returned['id']
        print('long description FK: ' + str(long_desc_fk))
        return long_desc_fk


def h1(h1_entry):
    h1_title = h1_entry
    h1_data = {
        "title": h1_title,
        "h1":
            long_desc_fk
    }
    h = requests.post("https://monkeybackend.ch/api/blog_new/create-post-title/", data=h1_data)
    print("Status: ", str(h.status_code))


def text(text_entries_dict):
    text_dict = text_entries_dict
    for key, value in text_dict.items():

        text_data = {
            "position": key,
            "text": [
                value
            ],
            "paragraphs":
                long_desc_fk
        }

        z = requests.post("https://www.monkeybackend.ch/api/blog_new/create-paragraph", data=text_data)
        print("id: ", str(key), "Status: ", str(z.status_code))


def img(image_entries_dict):
    img_dict = image_entries_dict
    for key, value in img_dict.items():
        key_sec = key['id']
        alt_value = str(value)
        img_data = {
            "position": key_sec,
            "image_alt": alt_value,
            "image_sections": long_desc_fk
        }

        #print(str(img_data))

        a = requests.post("https://www.monkeybackend.ch/api/blog_new/create-image-section/", data=img_data)
        print("Status: ", str(a.status_code))
