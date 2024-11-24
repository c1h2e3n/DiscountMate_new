import csv
import os
import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

# Retrieve configuration values
config = configparser.ConfigParser()
config.read('configuration.ini')
#这部分代码用于读取名为 configuration.ini 的配置文件。配置文件中包含一些爬取过程的配置信息（比如延迟时间、忽略的类别等）。

# Folder path and other configurations
folderpath = "C:/Users/Administrator/Desktop"
#保存抓取数据的文件夹路径

delay = int(config.get('IGA', 'delayseconds'))
#从配置文件中读取的一个设置，表示每次请求之间的延迟时间（单位：秒）

category_ignore = str(config.get('IGA', 'ignoredcategories'))
#从配置文件中获取的需要忽略的产品类别

# Create a new CSV file for IGA
filename = "IGA.csv"
#filename 是保存抓取数据的文件名，默认为 IGA.csv。
filepath = os.path.join(folderpath, filename)
#filepath 是完整的文件路径，包含文件夹路径和文件名。
if os.path.exists(filepath):#如果 CSV 文件已经存在，则先删除旧文件。
    os.remove(filepath)

print("Saving to " + filepath)
#输出文件保存路径信息。

# Write the header 打开文件并写入表头。表头包括要抓取的产品信息字段，比如产品代码、类别、商品名称、价格等。
with open(filepath, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Product Code", "Category", "Item Name", "Best Price", "Best Unit Price", "Item Price", "Unit Price", "Price Was", "Special Text","Link"])

# Configure options for EdgeDriver
options = webdriver.EdgeOptions()
#使用 EdgeOptions 配置浏览器选项。
options.add_argument("--app=https://www.igashop.com.au")
#--app 参数将直接打开指定的网页（在这里是 IGA 的网站）
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#excludeSwitches 用于禁用浏览器的日志输出。

# Start EdgeDriver
print("Starting IGA...")
#输出启动浏览器的信息。
driver = webdriver.Edge(options=options)
#使用配置好的选项启动 Edge 浏览器。


# Navigate to the IGA website
url = "https://www.igashop.com.au"
driver.get(url)
#打开 IGA 网站。
time.sleep(delay)
#在加载页面后，等待一段时间（delay 秒）以确保页面完全加载。

# Function to close the dialogue box
"""这段代码的目的是定义一个函数，用来关闭页面上可能出现的对话框（通常是弹出框）。
如果页面上有弹出框并且该框包含一个“关闭”按钮，代码会点击该按钮来关闭对话框。
如果没有找到该按钮，代码会捕捉异常并输出一条信息。"""
def close_dialogue_box():
    try:
        # Attempt to find and click the close button of the dialogue box
        close_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/button")
        #driver.find_element(By.XPATH, "/html/body/div[3]/div/div/button")：这是 Selenium 的一个方法，用于查找页面中的 HTML 元素。这里使用了 XPATH 定位方式，指定路径为 /html/body/div[3]/div/div/button，这意味着它在 HTML 的结构中查找第三个 div 标签下的 button 元素，假设这个按钮是关闭对话框的按钮。
        close_button.click()
        #close_button.click()：如果找到了这个按钮，就会模拟点击这个按钮，从而关闭对话框。
    except:
        # If the button is not found, just pass
        print("Close button is not found")
        #except: 语句捕捉任何异常。如果在 try 块中找不到关闭按钮，或者找到了但无法点击，就会进入 except 块。
#print("Close button is not found")：如果没有找到按钮或者遇到其他问题，程序会打印一条信息，提示用户未能找到关闭按钮。

# Set Click & Collect location (if necessary)
# Close dialogue box if it appears
close_dialogue_box()
#调用函数 close_dialogue_box() 来执行关闭对话框的操作。这行代码会检查页面上是否有弹出框并尝试关闭它。

# Parse the page content
page_contents = bs(driver.page_source, "html.parser")
"""driver.page_source：这是 Selenium 提供的属性，用于获取当前网页的完整 HTML 源代码（页面的 HTML 文档内容）。
driver 是 Selenium 启动的浏览器驱动实例，page_source 通过这个实例获取网页内容。
bs(driver.page_source, "html.parser")：使用 BeautifulSoup 将获取到的页面源代码解析成一个 BeautifulSoup 对象，
"html.parser" 表示使用 Python 内置的 HTML 解析器。这会使得后续的 HTML 内容更容易被查找、分析和提取。"""
#print(page_contents)
categories = [
    {"name": "Specials", "link": "/specials"},
    # {"name": "Fruit and Vegetable", "link": "/categories/fruit-and-vegetable/vegetables/1"},
    # {"name": "Pantry", "link": "/categories/pantry"},
    # {"name": "Meat, Seafood and Deli", "link": "/categories/meat-seafood-deli"},
    # {"name": "Dairy, Eggs and Fridge", "link": "/categories/dairy-eggs-fridge"},
    # {"name": "Bakery", "link": "/categories/bakery"},
    # {"name": "Drinks", "link": "/categories/drinks"},
    # {"name": "Frozen", "link": "/categories/frozen"},
    # {"name": "Health and Beauty", "link": "/categories/health-and-beauty"},
    # {"name": "Pet", "link": "/categories/pet"},
    # {"name": "Baby", "link": "/categories/baby"},
    # {"name": "Liquor", "link": "/categories/liquor"},
    # {"name": "Household", "link": "/categories/household"},
    # {"name": "Other", "link": "/categories/other"},
    # {"name": "Front of House", "link": "/categories/front-of-house"}
]
#这一部分定义了一个字典列表，每个字典代表 IGA 网站上的一个商品类别。每个字典包含两个键值对：
#"name"：商品类别的名称，例如 "Specials"（特价商品）、"Fruit and Vegetable"（水果和蔬菜）等。
#"link"：商品类别的链接路径，通常是该类别在网站上的 URL 相对路径。比如 /categories/specials 是特价商品类别的链接路径。

#这段代码的目的是过滤掉不需要抓取的商品类别，并展示最终需要抓取的类别列表。
# Remove categories ignored in the config file
categories = [cat for cat in categories if cat["name"] not in category_ignore]

"""这行代码使用了列表推导式来过滤掉 categories 列表中那些在 category_ignore 中指定的类别。详细解释如下：
列表推导式：[cat for cat in categories if cat["name"] not in category_ignore]
cat：列表 categories 中的每一个元素（字典），代表一个商品类别。
cat["name"]：访问字典中的 "name" 键，获取当前类别的名称。
category_ignore：这是之前从配置文件中读取的一个变量，可能是一个包含多个类别名称的字符串。它列出了需要忽略的类别。
cat["name"] not in category_ignore：判断当前类别名称是否不在 category_ignore 中。如果当前类别名称不在 category_ignore 中，则会保留这个类别，否则会被过滤掉。
最终，经过这行代码处理后，categories 列表只会保留那些不在 category_ignore 中的类别。"""

# Show the user the categories to scrape
print("Categories to Scrape:")
#print("Categories to Scrape:")：打印一条提示信息，表示即将展示需要抓取的类别。
for category in categories:
    #for category in categories:：遍历 categories 列表中的每个类别（现在已经是去除了需要忽略的类别后的列表）。
    print(category["name"])
    #print(category["name"])：打印当前类别的名称，category["name"] 获取的是每个字典中 "name" 键对应的值，即类别的名称。

#这段代码的作用是遍历每个商品类别，依次访问每个类别的页面，加载页面内容并进行解析。具体解释如下：
# Iterate through each category and follow the link to get the products
for category in categories:
    #这行代码通过 for 循环遍历 categories 列表中的每个类别（每个类别是一个字典，包含 name 和 link）。
    #每次循环，category 变量会依次指向 categories 列表中的每个字典

    driver = webdriver.Edge(options=options)
    #每次循环都会重新初始化一个浏览器驱动 driver，这是因为每个类别的页面可能需要重新加载，并且每个类别的页面可能是独立的，因此每次都需要新建一个浏览器实例。
    #webdriver.Edge(options=options)：这里使用的是 Microsoft Edge 浏览器，并传入 options 来配置浏览器（比如禁用日志输出和指定打开的 URL 等）。
    # Get the link to the category's page
    category_link = url + category["link"]
    category_name = category["name"]
    """category_link = url + category["link"]：从 categories 列表中获取当前类别的 link，并将其与基础 URL (url) 拼接，得到该类别页面的完整链接。
    url 是 IGA 网站的基础 URL（例如 "https://www.igashop.com.au"）。
    category["link"] 是当前类别的相对路径（例如 /categories/specials）。
    拼接后得到的 category_link 就是该类别页面的完整 URL（例如 "https://www.igashop.com.au/categories/specials"）。
    category_name = category["name"]：获取当前类别的名称（例如 "Specials"），以便在后续的操作中显示当前正在加载的类别。"""

    print("Loading Category: " + category_name)
    #通过 print 输出当前正在加载的类别名称。这样可以帮助用户了解爬虫当前抓取的进度。

    # Follow the link to the category page
    driver.get(category_link)
    #driver.get(category_link)：使用 Selenium 的 get() 方法打开当前类别的页面。浏览器会导航到 category_link 指定的 URL。
    # 获取所有的 <script> 标签
    time.sleep(delay)
    #time.sleep(delay)：暂停执行一段时间，等待页面加载完成。delay 是从配置文件中读取的一个时间间隔，表示爬虫在加载页面后等待的秒数，防止过快的请求导致网站被封禁或数据没有完全加载。

    # Close dialogue box if it appears on the category page
    close_dialogue_box()
    #该函数（前面已经定义）用于关闭页面上可能出的对话框。如果有弹窗或者提示框，它会尝试找到关闭按钮并点击它。
#这里调用 close_dialogue_box() 函数，确保在加载类别页面时，如果有弹出的对话框，可以自动关闭，避免影响后续数据抓取。
    print(category_link)
    # Parse page content
    soup = bs(driver.page_source, "html.parser")
    #print(driver.page_source)
    #print(soup.prettify())
    #driver.page_source：获取当前页面的 HTML 源代码。
    #bs(driver.page_source, "html.parser")：使用 BeautifulSoup 解析页面源代码，生成一个 BeautifulSoup 对象（soup）。BeautifulSoup 提供了便捷的 API，用于提取和操作 HTML 文档中的元素。
    page_current=driver.page_source
    # Get the number of pages in this category
    #这段代码的目的是在爬取的网页中查找分页信息，并提取总页数。如果找不到分页信息或分页出现错误，代码会默认设定总页数为 1。
    try:
        pagination = soup.find("ul", class_="flex flex-row items-center gap-2 mb-4 mt-2 max-w-full rounded bg-white p-2")
        #page_contents 是通过 BeautifulSoup 解析的页面 HTML 内容（一个 BeautifulSoup 对象）。
        #find("ul", class_="flex flex-row items")：这行代码使用 BeautifulSoup 的 find 方法查找页面中第一个符合条件的 <ul> 元素，该元素的 class 属性为 "flex flex-row items"。
        #这通常是分页部分的容器，它包含了分页按钮（例如页码 1, 2, 3 等）。
        #class_="flex flex-row items" 是 CSS 类，通常在分页的 <ul> 元素中指定，指示该元素的样式。
        #如果找到了该 <ul> 元素，并且它包含分页信息，它会被赋值给 pagination 变量。如果没有找到该元素，pagination 会是 None。
        print(pagination)
        print("SDFGTYUIUHYGF")
        pages = pagination.find_all("li")
        #pagination.find_all("li")：如果找到了 pagination（即分页的 <ul> 元素），这行代码会进一步查找所有 <li> 元素。每个 <li> 元素通常代表一个分页项，例如数字页码或上一页/下一页按钮。
        #find_all("li") 会返回一个列表，包含所有的 <li> 元素。该列表会被赋值给 pages 变量。
        total_pages = int(pages[-2].text.strip())
        #pages[-2]：pages 列表中的倒数第二个元素通常表示总页数。在很多分页结构中，倒数第二个 <li> 元素包含的是总页数（如“10”页、数字“10”在 <li> 中）。
        #.text.strip()：获取该 <li> 元素的文本内容，并使用 .strip() 去除文本前后的空白字符（如空格、换行符等）。
        #int()：将文本内容转换为整数类型，赋值给 total_pages 变量，表示网站的总页数。
    except:
        total_pages = 1
        #try 块中的代码如果出现任何异常（例如找不到分页元素、pages[-2] 索引出错等），就会进入 except 块。
        #total_pages = 1：如果遇到错误（如没有分页信息），代码会默认设置总页数为 1。这通常用于避免程序中断，让爬虫继续运行。
    print(total_pages)
    #这段代码的目的是在每一页上抓取商品信息，并输出当前页数以及该页上的商品数量。它通过循环遍历从第 1 页到总页数 total_pages，逐页抓取数据。
    #for page in range(1, total_pages + 1):
    for page in range(1, 20):
        #range(1, total_pages + 1)：这是一个 Python range() 函数，表示从 1 开始到 total_pages（包括 total_pages）的整数序列，目的是遍历所有的分页页面。
        #1：表示从第一页开始。
        #total_pages + 1：range() 的结束值是 total_pages + 1，因为 range() 是不包含结束值的。所以如果总页数是 10，这样就会循环 1 到 10。
        products_page_link=category_link+"/"+str(page)
        print(products_page_link)
        driver.get(products_page_link)
        # driver.get(category_link)：使用 Selenium 的 get() 方法打开当前类别的页面。浏览器会导航到 category_link 指定的 URL。
        # 获取所有的 <script> 标签
        time.sleep(delay)
        # time.sleep(delay)：暂停执行一段时间，等待页面加载完成。delay 是从配置文件中读取的一个时间间隔，表示爬虫在加载页面后等待的秒数，防止过快的请求导致网站被封禁或数据没有完全加载。

        # Close dialogue box if it appears on the category page
        close_dialogue_box()
        soup = bs(driver.page_source, "html.parser")
        #driver.page_source：获取当前浏览器页面的 HTML 源代码。
        #bs(driver.page_source, "html.parser")：使用 BeautifulSoup 解析页面源代码，并将解析后的页面内容存储到 soup 变量中，供后续操作使用。

        # Find all products on the page
        products = soup.find_all("div", class_="overflow-hidden rounded border border-border/50 bg-white text-foreground relative h-auto w-full p-2 md:h-[412px] md:w-[245px] md:p-3 md:pt-8")
        """soup.find_all("div", class_="overflow-hidden rounded border")：查找页面中所有符合条件的 <div> 元素，这些 <div> 元素表示页面中的商品。具体的筛选条件是：
        class_="overflow-hidden rounded border"：该 class_ 属性值表示商品的外部样式（可能是商品卡片的容器）。根据这个 class，代码能够找到每个商品的容器。
        
        find_all() 会返回一个列表，包含所有匹配的 <div> 元素，每个 <div> 代表一个商品。该列表会赋值给 products 变量。"""
        print(products)
        print(category_name + ": Page " + str(page) + " of " + str(total_pages) + " | Products on this page: " + str(len(products)))
        """该行代码用于打印输出当前页面的信息，帮助用户了解爬虫抓取的进度。输出的内容包括：
        category_name：当前商品类别的名称（例如 "Specials"、"Pantry" 等）。
        str(page)：当前正在抓取的页数。
        str(total_pages)：总页数。
        len(products)：当前页面上找到的商品数量。len(products) 返回的是 products 列表中的元素个数，即当前页面上包含的商品数。"""

        # Iterate through each product and extract the product details
        for product in products:
            """products 是一个包含所有商品的列表，每个商品是一个 BeautifulSoup 对象。
            for product in products：这个循环会依次遍历 products 列表中的每一个商品（即每个 <div> 元素），并执行以下提取操作。"""
            name = product.find("span", class_="line-clamp-3")
            print(name)
            #product.find("div", class_="flex max-w-[85%]")：查找商品元素中的 <div> 标签，它的 class 属性为 "flex max-w-[85%]"。这个 <div> 元素通常包含商品的名称。
            #name 变量将存储该商品名称对应的 BeautifulSoup 元素。如果找到了符合条件的元素，name 将是该元素的 BeautifulSoup 对象，如果找不到该元素，则返回 None。
            itemprice = product.find("span", class_="font-bold leading-none")
            print(itemprice)
            price_was_pos = product.find("div", class_="relative inline-flex w-fit shrink-0 items-center rounded px-3 py-1 font-sans text-sm font-bold bg-secondary text-secondary-foreground").get_text()
            print(price_was_pos)
            #product.find("span", class_="font-bold leading-none")：查找商品元素中的 <span> 标签，class 为 "font-bold leading-none"，通常表示商品的价格。
            #itemprice 将存储该 <span> 元素。如果该元素存在，itemprice 就是包含价格的 BeautifulSoup 元素，若不存在则返回 None。
            unitprice1= product.find("div", class_="relative flex text-sm lg:top-0")
            unitprice2=product.find("div", class_="flex gap-0 md:flex-col md:text-right")
            print(unitprice1)
            print(unitprice2)
            #product.find("span", class_="leading-none")：查找商品元素中的 <span> 标签，class 为 "leading-none"，通常表示单位价格。这里的 leading-none 可能是用于显示价格的单位（如“每公斤”、“每件”等）。
            #unitprice 将存储该 span 元素。如果找到了该元素，unitprice 就是包含单位价格的 BeautifulSoup 对象，若没有找到，则返回 None。
            specialtext = product.find("div", class_="relative inline-flex w-fit shrink-0 items-center rounded px-3 py-1 font-sans text-sm font-bold bg-primary text-primary-foreground justify-center md:absolute md:inset-x-0 md:top-0 md:h-3 md:w-full md:rounded-b-none md:rounded-t-sm md:p-3 md:text-base")
            """product.find("div", class_="relative inline-flex w-fit shrink-0 items-center rounded px-3 py-1 font-sans text-sm font-bold bg-primary")：查找商品元素中的 <div> 标签，class 为 "relative inline-flex w-fit shrink-0 items-center rounded px-3 py-1 font-sans text-sm font-bold bg-primary"。这个 <div> 标签通常包含一些特价文本或优惠信息（例如“特价”或者“折扣”）。
specialtext 变量将存储该文本所在的 BeautifulSoup 元素。如果找到了该元素，specialtext 就是包含特价文本的 BeautifulSoup 对象，否则返回 None。"""
            print(specialtext)
            productLink_location = product.find("div", class_="flex max-w-[85%] md:max-w-full")
            print(productLink_location)
            print("FUHYGVHUIUJH")
            productLink=product.find("a")['href']
            print(productLink)
            print("GYUHBHJI")
            """product.find("a", class_="relative justify-center")：查找商品元素中的 <a> 标签，它的 class 为 "relative justify-center"，该 <a> 标签通常包含商品的详细页面链接。
["href"]：从 <a> 标签中提取 href 属性，即商品的链接。这个链接通常指向商品的详细页面。
productLink 变量存储提取到的商品链接。"""
            productcode = (productLink.split("/")[-1]).split("-")[-1]
            print(productcode)
            """productLink.split("/")：将 productLink（即商品的 URL）按照 / 进行分割，生成一个列表。例如，链接 "https://www.igashop.com.au/products/12345" 会被分割为 ["https:", "", "www.igashop.com.au", "products", "12345"]。
[-1]：提取分割后列表中的最后一个元素，通常是商品代码部分（例如 "12345"）。
productcode 变量存储从链接中提取到的商品代码。"""
            unitprice=" "
            # Extract product details
            if name and itemprice:#这行代码检查 name（商品名称）和 itemprice（商品价格）是否都有成功提取（即不是 None）。如果这两个字段都有内容，程序才会继续处理该商品。
                name = name.get_text(strip=True)#去除商品名称字符串的前后空白字符。
                itemprice = itemprice.get_text(strip=True)#去除商品价格字符串的前后空白字符。
                best_price = itemprice#假设商品的 itemprice（商品价格）是该商品的“最佳价格”。
                link = url + productLink#构建商品的完整链接。由于 productLink 是相对路径，url 是基网址，这行代码将两者合并为一个完整的 URL（例如：https://www.igashop.com.au/products/12345）。
                print(name,itemprice,link)
                # Unit Price and Was Price
                if unitprice1:
                    unitprice1 = unitprice1.get_text(strip=True)
                    #unitprice.text.strip().lower()：去除单位价格的前后空白字符并转换为小写字母，确保后续比较时大小写不影响处理。
                    unitprice=unitprice1
                    best_unitprice = unitprice
                elif unitprice2:
                    unitprice2 = unitprice2.get_text(strip=True)
                    # unitprice.text.strip().lower()：去除单位价格的前后空白字符并转换为小写字母，确保后续比较时大小写不影响处理。
                    unitprice = unitprice2
                    best_unitprice = unitprice
                else :
                    best_unitprice = None
                    price_was_pos = None
                print(best_unitprice)
                print(price_was_pos)
                """unitprice.find("was $")：查找字符串中是否包含“was $”标记。如果包含，表示该商品的单位价格之前可能有“原价”（如“原价 $2.99”）。
price_was = unitprice[price_was_pos + 4:].strip()：提取“原价”部分，price_was_pos + 4 跳过了“was $”的部分，提取后面的文本（即原始价格）。
unitprice = unitprice[:price_was_pos].strip()：提取并更新单位价格，只保留“原价”前面的部分。
if unitprice[0] == "|":：如果单位价格以 "|" 开头（可能是格式问题或多余的符号），将其设为 None。
best_unitprice = unitprice：将单位价格保存为 best_unitprice。
如果没有提取到单位价格，则将 best_unitprice 和 price_was 设置为 None。"""
                if price_was_pos:
                    price_was_pos = price_was_pos.replace('was', '').strip()
                    print(price_was_pos)
                # Special Text
                if specialtext:
                    specialtext = specialtext.text.strip()
                    if specialtext == "1/2":
                        specialtext = "50%"
                    print(specialtext)
                """specialtext.text.strip()：去除特价文本的前后空白字符。
如果特价文本为 "1/2"，则将其转换为 "50%"。这可能是一个格式问题，指示商品打折一半，代码将其标准化为常见的折扣形式。"""

                # Complex Promo

                """complexpromo.text.strip()：去除复杂促销文本的前后空白字符。
如果促销文本包含 "Pick any " 或 "Buy "，表示这是一个复杂的促销形式（例如“买一送一”或“买任意 3 件”）。
在 try 块中，首先去掉 "Pick any " 或 "Buy " 字样，然后解析促销文本：
complex_itemcount = int(complexpromo[:complexpromo.find(" for")])：提取促销中购买的商品数量（例如“买 3 件”）。
complex_cost = float(complexpromo[complexpromo.find("$") + 1:])：提取促销后的价格（例如“花费 5.99 美元”）。
best_price = "$" + str(round(complex_cost / complex_itemcount, 2))：计算单件商品的价格，将其设置为“最佳价格”。
如果在解析过程中出现错误（例如促销格式不符合预期），则将 best_price 设置为原始的商品价格 itemprice。"""

                # Write contents to file
                with open(filepath, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([productcode, category_name, name, best_price, best_unitprice, itemprice, unitprice, price_was_pos, specialtext,link])
                """with open(filepath, "a", newline="") as f:：打开 CSV 文件（路径由 filepath 变量提供）进行追加写入（"a"）。newline="" 用来避免写入多余的空行。
csv.writer(f)：创建一个 CSV 写入器，用于将数据写入文件。
writer.writerow([...])：将提取到的商品信息按列写入文件。每一列代表一个字段，按顺序存储商品信息：
productcode：商品代码。
category_name：商品所在类别。
name：商品名称。
best_price：最佳价格（可能是复杂促销价格或商品价格）。
best_unitprice：单位价格（可能是折扣后的价格）。
itemprice：商品原价。
unitprice：单位价格（可能包括“原价”信息）。
price_was：原价（如果有的话）。
specialtext：特价文本（例如“50%”）。
complexpromo：复杂促销文本（例如“买任意 3 件”）。
link：商品详情页面链接。"""
                # Reset variables
                name = None
                itemprice = None
                unitprice = None
                specialtext = None
                productLink = None
                productcode = None
                price_was_pos = None
                """在每次循环开始时，所有保存商品信息的变量被重置为 None。这是为了确保每次处理新的商品时，上一条数据不会影响到当前数据的提取。这个清理操作通常在每个页面循环或者商品数据处理完成后进行。"""
        # Get the link to the next page
        next_page_link = f"{category_link}?page={page + 1}"
        """next_page_link：生成当前类别页面的下一页 URL。
通过字符串格式化构建下一页的链接，category_link 是当前类别的基础链接，page + 1 表示当前页面的下一个页面。
假设当前页面是第 1 页，下一页的链接将是 category_link?page=2。"""

        # Restart browser every 50 pages
        if page % 50 == 0:
            print("Restarting Browser...")
            driver.close()
            driver = webdriver.Edge(options=options)
        """每爬取 50 页时，程序会关闭当前的浏览器实例，并创建一个新的浏览器实例。这通常是为了避免由于浏览器会话长时间运行导致的内存泄漏或性能下降。
driver.close()：关闭当前的浏览器窗口。
driver = webdriver.Edge(options=options)：重新启动浏览器，使用相同的配置选项 (options) 启动一个新的 Edge 浏览器实例。"""

        # Navigate to the next page
        if total_pages > 1 and page + 1 <= total_pages:
            driver.get(next_page_link)
            close_dialogue_box()  # Close the dialogue box on the next page
            """if total_pages > 1 and page + 1 <= total_pages:：判断是否存在下一页，即 page + 1 小于等于 total_pages（总页数）。
    driver.get(next_page_link)：如果有下一页，浏览器将导航到下一页。
    close_dialogue_box()：如果在新页面加载时弹出了对话框（例如欢迎信息、Cookie 同意框等），调用该函数来关闭对话框。"""

        time.sleep(delay)
        """time.sleep(delay)：每次切换页面后，程序会暂停 delay 秒，防止请求过于频繁，给网站服务器留出足够的时间响应请求。
delay 是从配置文件中读取的，通常以秒为单位。"""
    time.sleep(delay)
    driver.close()
driver.quit()
print("Finished")

"""time.sleep(delay)：在程序结束前，稍微等待一段时间。
driver.close()：关闭当前浏览器窗口，结束当前的浏览器会话。
driver.quit()：彻底关闭 WebDriver，并清理资源，退出浏览器。
print("Finished")：在控制台输出“Finished”提示，表示爬虫任务已经完成。"""