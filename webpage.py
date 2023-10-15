from selenium import webdriver
import urllib.request
import os
import json
import time
from selenium.webdriver.common.by import By


# link = "https://www.myntra.com/sweatshirts/allen+solly/allen-solly-mock-collar-front-open-sweatshirt/24572040/buy"


def get_data(link):
    try:
        driver = webdriver.Chrome()

        driver.get(link)
        metadata = dict()
        metadata["title"] = driver.find_element(By.CLASS_NAME, "pdp-title").get_attribute("innerHTML")
        metadata["name"] = driver.find_element(By.CLASS_NAME, "pdp-name").get_attribute("innerHTML")
        metadata["price"] = (
            driver.find_element(By.CLASS_NAME, "pdp-price")
            .find_element(By.XPATH, "./strong")
            .get_attribute("innerHTML")
        )

        # print(metadata)

        metadata["specifications"] = dict()

        # try:
        # driver.find_element(By.CLASS_NAME, "index-showMoreText").click()

        for index_row in driver.find_element(By.CLASS_NAME, "index-tableContainer").find_elements(
            By.CLASS_NAME, "index-row"
        ):
            metadata["specifications"][
                index_row.find_element(By.CLASS_NAME, "index-rowKey").get_attribute("innerHTML")
            ] = index_row.find_element(By.CLASS_NAME, "index-rowValue").get_attribute("innerHTML")
            metadata["productId"] = driver.find_element(By.CLASS_NAME, "supplier-styleId").get_attribute("innerHTML")

        # except:
        #     print("no further info")

        itr = 1

        for image_tags in driver.find_elements(By.CLASS_NAME, "image-grid-image"):
            image_path = os.path.join("data", metadata["productId"], "images", str(itr) + ".jpg")

            # make the dir if doesnot exist
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            urllib.request.urlretrieve(image_tags.get_attribute("style").split('url("')[1].split('")')[0], image_path)
            itr += 1

        metadata["url"] = link

        # write the meta data to json
        with open(os.path.join("data", metadata["productId"], "meta.json"), "w") as f:
            json.dump(metadata, f, indent=4)

        with open("success_links.txt", "a") as f:
            f.write(link + "\n")

    except:
        # append to the text failed links
        with open("failed_links.txt", "a") as f:
            f.write(link + "\n")


# use parallel processing to speed up the process
from multiprocessing import Pool
import time

links = []
for i in range(600000, 601000):

    # add more zeros in the range to get more data
    i = str(i).zfill(5)
    
    links.append(
        f"https://www.myntra.com/shirts/park+avenue/park-avenue-slim-fit-checked-pure-cotton-casual-shirt/22{i}/buy"
    )

start = time.time()

num_cores = os.cpu_count()

with Pool(num_cores) as p:
    p.map(get_data, links)

print(f"Time taken: {time.time() - start}")
