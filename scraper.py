import pathlib
import requests
import sys
import time
from PIL import Image
from io import BytesIO
from selenium import webdriver

url = "https://pixabay.com/photos/search/" + sys.argv[1] if len(
    sys.argv) > 1 else "https://pixabay.com/photos/search/beautiful"
result_folder = "./images/"
selector = "div.item"
driver = webdriver.Chrome(executable_path=r'chromedriver.exe')

driver.get(url)

# Let the page load
driver.execute_script("$('html').css('scroll-behavior','smooth')")
driver.execute_script("window.scrollTo(0,10000);")

# =================================================================================================
# ==================================TO SIMULATE REDIRECTION=======================================
# =================================================================================================

add_script = """$("#content > div > div:nth-child(2) > div > div.flex_grid.credits.search_results > div:nth-child(13) > a > img").each(function() {
  // first copy the attributes to remove
  // if we don't do this it causes problems
  // iterating over the array we're removing
  // elements from
  var attributes = $.map(this.attributes, function(item) {
    return item.name;
  });

  // now use jQuery to remove the attributes
  var img = $(this);
  $.each(attributes, function(i, item) {
    img.removeAttr(item);
  });
});
$("#content > div > div:nth-child(2) > div > div.flex_grid.credits.search_results > div:nth-child(13) > a > img").attr('src','http://httpbin.org/redirect/5')

"""
driver.execute_script(add_script)

# =================================================================================================
# =================================================================================================
# =================================================================================================
time.sleep(5)
image_elements = driver.find_elements_by_css_selector(
    "#content div.media_list div div div.flex_grid.credits.search_results div a img")
pathlib.Path(result_folder).mkdir(parents=True, exist_ok=True)
i = 1
for image_element in image_elements:
    image_url = image_element.get_attribute("src").split("?")[0]
    image_object = requests.get(image_url)
    image_name = image_url.split("/")[-1]
    if requests.get(image_url, allow_redirects=False).status_code > 299 and requests.get(image_url,
                                                                                         allow_redirects=False).status_code < 400:
        print('===================================================================')
        print(i, image_url)
        print('===================================================================')
        driver.execute_script('return window.stop')
        driver.quit()
        break
    else:

        image = Image.open(BytesIO(image_object.content))
        image.save(result_folder + image_name + "." + image.format, image.format)
        print(i, image_name)
        i += 1
print('=====TASK COMPLETED=====')
driver.quit()
