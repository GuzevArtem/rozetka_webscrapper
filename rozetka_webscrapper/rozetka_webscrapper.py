import requests
import datetime

import model
import settings

import files.file_writer as fw

from bs4 import BeautifulSoup

from driver import Driver

def decode_str(unicodestr):
    #encoded = unicodestr.encode()
    #decoded = encoded.decode('unicode-escape')
    return unicodestr

def parse_comment(comment):
    parsed_comment = model.comment.Comment()

    comment_author = comment.find(class_="comment__author")

    if comment_author:
        comment_date = comment.find(class_="comment__date")
        if comment_date:
            parsed_comment.date = decode_str(comment_date.get_text())
        comment_date.decompose()
        parsed_comment.author = decode_str(comment_author.get_text())

    

    comment_link = comment.find(class_="comment__link")
    if comment_link:
        parsed_comment.url = comment_link.get("href")

    comment_vars_list = comment.find(class_="comment__vars-list") #sellers

    #parse vars_list
    parsed_comment_vars_list = []
    if comment_vars_list:
        comment_vars_lists = comment_vars_list.find_all(class_="comment__vars-item")
        if comment_vars_lists:
            for item in comment_vars_lists:
                res = {}
                label = item.find(class_="comment__vars-label")
                value = item.find(class_="comment__vars-value")
                if label:
                    res["label"] = decode_str(label.get_text())
                if value:
                    res["value"] = decode_str(value.get_text())
                if res:
                    parsed_comment_vars_list.append(res)

    parsed_comment.vars_list = parsed_comment_vars_list
    
    #parse rating
    comment_rating = comment.find("rz-comment-rating") #may be Empty
    #has 5 items
    #each star has fill(#0) or fiil(#1)
    # svg path (tag) fill
    if comment_rating:
        stars = comment_rating.find_all("svg")
        stars_count = 0;
        for star in stars:
            path = star.find("path")
            if path:
                fill = path.get("fill")
                if fill == "url(#1)":
                    stars_count += 1

    parsed_comment.rating = stars_count

    #parse essentials
    comment_text = comment.find(class_="comment__text")
    if comment_text:
        parsed_comment.text = decode_str(comment_text.get_text())

    comment_essentials_list = comment.find_all(class_="comment__essentials-item") #has label and optional <dd> with text
    parsed_essentials_list = []
    if comment_essentials_list:
        for essential in comment_essentials_list:
            res = {}
            essential_label = essential.find("dt", class_="comment__essentials-label")
            essential_data = essential.find("dd")
            if essential_label:
                res["label"] = decode_str(essential_label.get_text())
            if essential_data:
                res["data"] = decode_str(essential_data.get_text())
            parsed_essentials_list.append(res)

    parsed_comment.essentials_list = parsed_essentials_list;

    #parse attached photos
    parsed_photos_urls = []

    comment_attached_photos_urls = comment.find(class_="product-comments__photos-list")
    if comment_attached_photos_urls:
        photos_list = comment_attached_photos_urls.find_all(class_="product-comments__photos-item")
        if photos_list:
            for photo in photos_list:
                img = photo.find("img")
                if img:
                    url = img.get("src")
                    parsed_photos_urls.append(url)

    parsed_comment.attached_photos_urls = parsed_photos_urls
    return parsed_comment

def parse_item_page_for_comments(page):
    soup = BeautifulSoup(page.text, 'html.parser')

    # get the comments
    comments = soup.find('comment-list')
    #print(comments)
    
    parsed_comments = []
    # find all instances of that class (should return 25 as shown in the github main page)
    if comments:
        comments_list = comments.find_all("li", class_="product-comments__list-item")
        comments_count = 0
        if comments_list:
            for comment in comments_list:
                parsed_comments.append(parse_comment(comment))
                comments_count += 1
                if comments_count >= settings.COMMENTS_PER_PAGE_LIMIT :
                    break
    return parsed_comments

def parse_item_page(url):
    parsed_item = model.item.Item()
    page = requests.get(url+'comments/')
    parsed_item.url = url
    soup = BeautifulSoup(page.text, 'html.parser')
    title = soup.find(class_="product__title")
    if title:
        parsed_item.name = decode_str(title.get_text())

    if page.reason == 'OK':
        print('parse item:', parsed_item.name)
        parsed_item.comments = parse_item_page_for_comments(page)
    else:
        parsed_item.error = page.reason
    return parsed_item

def parse_specific_items_group(url):
    driver = Driver.get()
    driver.get(url)  
    html = driver.page_source

    parsed_group = model.group.Group()
    parsed_group.url = url
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("h1", class_="catalog-heading")
    if title:
        parsed_group.name = decode_str(title.get_text())

    print('parse group:', parsed_group.name)
    parsed_items = []
    if html != "":
        #parse items in group
        item_wrappers = soup.find_all("div", class_="goods-tile")
        if item_wrappers:
            items_count = 0
            for item_wrapper in item_wrappers:
                item_link_holder = item_wrapper.find("a", class_="goods-tile__picture")
                item_href = item_link_holder.get("href")
                if item_href:
                    parsed_item = parse_item_page(item_href)
                    parsed_items.append(parsed_item)
                items_count += 1
                if items_count >= settings.ITEMS_PER_GROUP_LIMIT:
                    break
        parsed_group.items = parsed_items
    else:
        parsed_group.error = "error"
    return parsed_group

def parse_category(url):
    driver = Driver.get()
    driver.get(url)  
    html = driver.page_source

    parsed_category = model.category.Category()

    parsed_category.url = url
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("h1", class_="portal__heading")
    if title:
        parsed_category.name = decode_str(title.get_text())

    print('parse category:', parsed_category.name)
    parsed_groups = []
    if html != "":
        #parse groups in category
        group_wrappers = soup.find_all("div", class_="tile-cats")
        if group_wrappers:
            groups_count = 0

            for group_wrapper in group_wrappers:
                group_link_holder = group_wrapper.find("a", class_="tile-cats__picture")
                group_href = group_link_holder.get("href")
                if group_href:
                    parsed_group = parse_specific_items_group(group_href)
                    parsed_groups.append(parsed_group)
                groups_count += 1
                if groups_count >= settings.GROUPS_PER_CATEGORY_LIMIT:
                    break
        parsed_category.groups = parsed_groups
    else:
        parsed_item.error = "error"
    return parsed_category

def parse_root():
    url = 'https://rozetka.com.ua/'

    driver = Driver.get()
    driver.get(url)
    html = driver.page_source

    parsed_categories = []

    categories_count = 0

    soup = BeautifulSoup(html, 'html.parser')
    link_holders = soup.find_all("a", class_="menu-categories__link")
    if link_holders:
        for link_holder in link_holders:
            link = link_holder.get("href")
            category = parse_category(link)
            if category:
                parsed_categories.append(category)
            categories_count += 1
            if categories_count >= settings.CATEGORIES_LIMIT:
                break
    return parsed_categories

def scrap_rozetka_web_site():
    time_start = datetime.datetime.now()
    print("Parsing started at:", time_start)

    parsed_site_data = parse_root()

    time_end = datetime.datetime.now()
    print("Parsing ended at:", time_end)
    print("Parsing took:", time_end - time_start)

#### testing of correct json parsing
#    for parsed_category in parsed_site_data :
#        reparsed = model.category.Category.fromJson(parsed_category.toJson())
#        #print(reparsed)
#        #print(isinstance(reparsed, model.category.Category))
#        for g in reparsed.groups:
#            #print(g)
#            #print(isinstance(g, model.group.Group))
#            for i in g.items:
#                #print(i)
#                #print(isinstance(i, model.item.Item))
#                for c in i.comments:
#                    #print(c)
#                    #print(isinstance(c, model.item.Comment))

    Driver.close()
    print("End of parsing!")
    Driver.quit()

    print("Saving to file!")
    fw.write_plain_iterable(
        (settings.RESULT_FOLDER_NAME + "/" + settings.RESULT_FILE_NAME_PREFIX + "_" + str(datetime.datetime.now()).replace(" ", "_").replace(":","").replace(".", "") + ".json").replace("/+", "/"),
        parsed_site_data,
        lambda o : o.toJson(),
        encoding='utf-8'
        )
    return parsed_site_data


#top category 'https://rozetka.com.ua/computers-notebooks/c80253/'
#parsed_category = parse_category('https://rozetka.com.ua/computers-notebooks/c80253/')
#print(parsed_category)

#specific category 'https://rozetka.com.ua/notebooks/c80004/'
#parsed_group = parse_specific_items_group('https://rozetka.com.ua/notebooks/c80004/')
#print(parsed_group)

#specific item 'https://rozetka.com.ua/asus_90nr0351_m02460/p238731799/'
#parsed_item = parse_item_page_for_comments('https://rozetka.com.ua/asus_90nr0351_m02460/p238731799/')
#print(parsed_item)

#full parser
#get all categories by selector
#.menu-categories .menu-categories_type_main
#for each category scrap sub-categories by selector
#.tile-cats
#for each category scrap available items by
#.goods-tile
#then get
#.goods-tile__heading -> href property
#add /comments to href property
#get all divs by selector
#.comment
#parse comment
