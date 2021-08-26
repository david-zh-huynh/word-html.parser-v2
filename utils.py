from datetime import date

import requests
import json

meta_id = ""
long_desc_fk = ""

backend_url = "https://monkeybackend.ch/"
Username = "alain@marketingmonkeys.ch",
password = "kd8e54zj"


def login():
    credentials = {
        "email": Username,
        "password": password
    }
    x = requests.post(backend_url + "auth/login/", data=credentials)
    json_text = json.loads(x.text)
    tokens = json.loads(str(json_text['tokens']).replace('\'', '\"'))
    access_token = tokens['access']
    refresh_token = tokens['refresh']
    print(access_token + "    " + refresh_token)

    return access_token


def connect(access_token):
    my_headers = {'Authorization': 'Bearer ' + access_token}
    # content number
    print('Please enter Content Number of Article:')
    cont_number = input()
    api_article_nr = {"content_number": cont_number}

    # send content number to backend
    api_article_nr_send = requests.post(backend_url + 'api/blog_new/create-post-number/', data=api_article_nr,
                                        headers=my_headers)
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


def meta(meta_dict, access_token):
    connect_get = connect(access_token)
    meta_get = meta_dict

    meta_lang = int(input('Select Article Language:'
                          '\n1 for English, '
                          '\n2 for Deutsch '
                          '\nEnter: '))
    meta_global = ""
    meta_cat = ""
    if meta_lang == 1:
        meta_lang = "en"
        meta_global = "2"
        meta_cat = int(input('Select Category: '
                             '\n2 for Business & Strategy'
                             '\n3 for Web Development'
                             '\n4 for Marketing Automation'
                             '\n5 for SEO & SEA'
                             '\n6 for Digital Marketing'
                             '\nEnter: '
                             ))

    if meta_lang == 2:
        meta_lang = "de"
        meta_global = "1"
        meta_cat = int(input('Select Category: '
                             '\n1 for Business & Strategie'
                             '\n7 for Web Entwicklung'
                             '\n8 for Marketing Automation'
                             '\n9 for SEO & SEA'
                             '\n10 for Digital Marketing'
                             '\nEnter: '
                             ))
    else:
        print("invalid input: " + meta_lang,
              "please select Language a language again.")

    meta_author = input('Select Author: '
                        '\n1 for Thomas Roth'
                        '\n2 for Alain Habegger'
                        '\nEnter: ')

    meta_data = {
        "lang": meta_lang,
        "slug": meta_get['URL'],
        "seo_site_title": meta_get['Title'],
        "seo_meta_description": meta_get['Meta Description'],
        "title": meta_get['Headline'],
        "short_description": meta_get['Teaser'],
        "date": date.today(),
        "reading_time": meta_get['Reading Time'],
        "level": meta_get['Level'],
        "category": meta_cat,
        "image_featured_alt": meta_get['Headline'],
        "image_regular_alt": meta_get['Headline'],
        "image_regular_increased_alt": meta_get['Headline'],
        "image_main_alt": meta_get['Headline'],
        "author": meta_author,
        "global_texts": meta_global,
        "posts": connect_get
    }

    print(meta_data)
    my_headers = {'Authorization': 'Bearer ' + access_token}
    c = requests.post(backend_url + "api/blog_new/create-post-meta/", data=meta_data, headers=my_headers)
    print(c.text)
    if c.status_code == 201:
        meta_id_response = c
        meta_id_returned = meta_id_response.json()
        global meta_id
        meta_id = meta_id_returned['id']
        print('meta_id: ' + str(meta_id))
        return meta_id

    else:
        print('Meta Error: ' + str(c.status_code))


def long_desc(meta_identifier, access_token):
    meta_get_id = meta_identifier
    # print(meta_get)

    desc_data = {"long_description": meta_get_id}
    my_headers = {'Authorization': 'Bearer ' + access_token}
    ld = requests.post(backend_url + "api/blog_new/create-long-description/", data=desc_data, headers=my_headers)
    print(ld.text)
    print("long description status: " + str(ld.status_code))

    if ld.status_code == 201:
        long_desc_fk_response = ld
        long_desc_fk_returned = long_desc_fk_response.json()
        global long_desc_fk
        long_desc_fk = long_desc_fk_returned['id']
        print('long description FK: ' + str(long_desc_fk))
        return long_desc_fk


def h1(h1_entry, access_token):
    h1_title = h1_entry
    h1_data = {
        "title": h1_title,
        "h1":
            long_desc_fk
    }
    my_headers = {'Authorization': 'Bearer ' + access_token}
    h = requests.post(backend_url + "api/blog_new/create-post-title/", data=h1_data, headers=my_headers)
    print("h1 Status: ", str(h.status_code))


def img(image_entries_dict, access_token):
    img_dict = image_entries_dict
    for key, value in img_dict.items():
        key_sec = key['id']
        alt_value = str(value)
        img_data = {
            "position": key_sec,
            "image_alt": alt_value,
            "image_sections": long_desc_fk
        }
        my_headers = {'Authorization': 'Bearer ' + access_token}
        a = requests.post(backend_url + "api/blog_new/create-image-section/", data=img_data, headers=my_headers)
        print("Image Status: ", str(a.status_code))


def text(text_entries_dict, access_token):
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
        my_headers = {'Authorization': 'Bearer ' + access_token}
        z = requests.post(backend_url + "api/blog_new/create-paragraph/", data=text_data, headers=my_headers)
        print("id: ", str(key), "Text Status: ", str(z.status_code))
