import concurrent.futures
import json
import logging
import os
import re
from collections import namedtuple
from io import BytesIO
from typing import List

import requests
from PIL import Image
from bs4 import BeautifulSoup as bs
from django.conf import settings
from fake_useragent import UserAgent

from apps.product.models import Product, ProductImage

logger = logging.getLogger('scrap_product_images')

PRODUCT_URLS = [
    'https://www.aarong.com/catalog/product/view/id/656192/s/yellow-half-silk-jamdani-saree/category/233/',
    'https://www.aarong.com/men/panjabi/black-brush-painted-and-printed-endi-silk-panjabi-15f220220047.html',
    'https://www.aarong.com/men/panjabi/grey-printed-and-wax-dyed-viscose-cotton-panjabi-15eg210360287.html',
    'https://www.aarong.com/men/panjabi/blue-grey-printed-and-embroidered-viscose-cotton--slim-fit-panjabi-15e220360145.html'

]

ImageObject = namedtuple('Image', ['path', 'width', 'height', 'size'])
ImageUrlObject = namedtuple('ImageUrl', ['url', 'position'])


def scrap_product_images(url: str) -> List:
    cookies = {
        'Location_Cookie': 'bang',
        'user_allowed_save_cookie': "{\"1\":1}"
    }
    ua = UserAgent(cache=True)
    headers = {'user-agent': ua.random}

    cookies_jar = requests.cookies.RequestsCookieJar()
    for key, val in cookies.items():
        cookies_jar.set(key, val, domain="aarong.com", path='/')
    session = requests.Session()
    session.keep_alive = False

    page = session.get(url, headers=headers, cookies=cookies_jar,
                       allow_redirects=False)
    soup = bs(page.content, 'html.parser')
    image_data_pattern = re.compile(r'("data":.*])', re.MULTILINE | re.DOTALL)
    script_pattern = re.compile(r'("mage\/gallery\/gallery":.*)',
                                re.MULTILINE | re.DOTALL)

    script = soup.find("script", text=script_pattern)
    images = []
    if script:
        match = image_data_pattern.search(script.text)
        if match:
            # remove "data": from the start
            image_data_str = match.group(0)[7:]
            images = json.loads(image_data_str)
            images = sorted(images, key=lambda x: int(x['position']))
            images = list(map(lambda x: ImageUrlObject(
                url=x['full'].split('?')[0], position=x['position']), images))
    return images


def download_image_from_url_and_save_to_disk(product_id: int, image_url: str) -> ImageObject:
    image_name = image_url.split('/')[-1]
    image_db_uri = f"catalog/product/{product_id}"
    image_base_path = os.path.join(settings.MEDIA_ROOT, image_db_uri)
    # check directory exists or not
    if not os.path.exists(image_base_path):
        # create directory
        try:
            os.makedirs(image_base_path)
        except FileExistsError:
            pass
    image = requests.get(image_url)

    output_path = os.path.join(
        image_base_path, image_name
    )
    size = int(image.headers['content-length']) / 1000  # convert to KB
    im = Image.open(BytesIO(image.content))
    im.save(output_path)
    width, height = im.width, im.height

    # relative path
    image_path = f"{image_db_uri}/{image_name}"

    return ImageObject(path=image_path, width=width, height=height, size=size)


def download(image_urls: List[ImageUrlObject], product: Product) -> List[ProductImage]:
    product_image_object_list: List[ProductImage] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {
            executor.submit(download_image_from_url_and_save_to_disk, product.id, image_url.url): image_url
            for image_url in image_urls
        }
        for future in concurrent.futures.as_completed(
                future_to_url
        ):
            image_url_obj: ImageUrlObject = future_to_url[future]
            try:
                data = future.result()
                product_image_object_list.append(ProductImage(
                    scrap_url=image_url_obj.url,
                    product=product,
                    height=data.height,
                    width=data.width,
                    image=data.path,
                    position=image_url_obj.position,
                ))
            except Exception as exc:
                logger.error("%r generated an exception: %s" %
                             (image_url_obj.url, exc))
            else:
                logger.info('%r image is %d KB' % (data.path, data.size))

    return product_image_object_list


def run():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(scrap_product_images, url): url for url in PRODUCT_URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                images = future.result()
                product, created = Product.objects.get_or_create(scrap_url=url)

                if created:
                    product_image_object_list = download(images, product)
                    # bulk create
                    product.images.bulk_create(
                        product_image_object_list,
                        batch_size=100,
                        ignore_conflicts=True)

                    logger.info(f"Product:[{product.id}] total {len(product_image_object_list)} image downloaded")
                else:
                    logger.warning(f"Product:[{product.id}] images already downloaded")
            except Exception as exc:
                logger.warning('%r generated an exception: %s' % (url, exc))
            else:
                logger.info('%r total image is %d' % (url, len(images)))
