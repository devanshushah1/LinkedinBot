from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import clipboard
from time import sleep
import time,datetime
from selenium.common.exceptions import NoSuchElementException
from .models import Profile , Message, Business, Facebook, Image, GIF, LinkedInPosts
from django.contrib.sites.shortcuts import get_current_site

#-------------------------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def scroll_page(driver,run_time=0,max_run_time=1, max_scroll_count=1):
    pre_scroll_height = driver.execute_script('return document.body.scrollHeight;')
    scroll_count = 0
    while max_scroll_count != scroll_count:
        iteration_start = time.time()
    # Scroll webpage, the 100 allows for a more 'aggressive' scroll
        driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')

        post_scroll_height = driver.execute_script('return document.body.scrollHeight;')
        scroll_count+=1

        scrolled = post_scroll_height != pre_scroll_height
        timed_out = run_time >= max_run_time

        if scrolled:
            run_time = 0
            pre_scroll_height = post_scroll_height
        elif not scrolled and not timed_out:
            run_time += time.time() - iteration_start
        elif not scrolled and timed_out:
            break
# Create your views here.
class linkedin(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        driver = webdriver.Chrome(executable_path=r"E:\Programming\INTERNSHIP\Web Scrapping\facebook_new\chromedriver.exe")
        url = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
        driver.get(url)
        time.sleep(3)
        my_id = request.POST.get('uid')
        login_email = driver.find_element_by_id('username')
        login_email.send_keys(my_id)

        my_password = request.POST.get('pass')
        password = driver.find_element_by_id('password')
        password.send_keys(my_password)
        login_submit = driver.find_element_by_tag_name('button')
        login_submit.click()
        search_term = request.POST.get('search')
        # search term = python
        count_of_url = 0
        page_number = 0
        while count_of_url < 2:
            page_number = page_number + 1
            page_number = str(page_number)

            if count_of_url < 1000:
                search_term_url='https://www.linkedin.com/search/results/people/?keywords='+ search_term + '&page='+ page_number
                driver.get(search_term_url)
                time.sleep(3)

            count_of_url = count_of_url + 1
            page_number = int(page_number)
            print("page number:",page_number)
            try:
                data=driver.find_element_by_class_name('reusable-search__entity-results-list')
                scroll_page(driver)

                profile_link=data.find_elements_by_tag_name('a')
                sleep(2)
                profile_links=[]
                for anchor in profile_link:
                    profile_links.append(anchor.get_attribute("href"))
                without_duplicate=[]
                for x in profile_links:
                    if x not in without_duplicate:
                        if '/in/' in x:
                            without_duplicate.append(x)
                print(without_duplicate)
                for link in without_duplicate:
                    pro=Profile()
                    print(link)
                    if Profile.objects.filter(link=link).count() !=0:
                        continue
                    else:
                        pro.link=link
                        driver.get(link)
                        time.sleep(3)
                        try:
                            name=driver.find_element_by_xpath("//div[@class='flex-1 mr5']/ul[@class='pv-top-card--list inline-flex align-items-center']/li")
                            name=name.text

                            f_name=name.split(" ")[0]
                            print("first name: ", f_name)

                            l_name=((name.split(" "))[1]).split("\n")[0]
                            print("last name: ", l_name)
                            names=f_name+" "+l_name
                            print("name:",names)
                            if "(" in l_name:
                                pro.name=f_name
                            else:
                                pro.name=names
                        except NoSuchElementException:
                            pass

                        try:
                            heading=driver.find_element_by_xpath("//div[@class='flex-1 mr5']/h2")
                            print("heading:",heading.text)
                            pro.heading=heading.text
                        except NoSuchElementException:
                            pass

                            sleep(3)
                            scroll_page(driver)

                            sleep(2)
                        try:
                            experience=driver.find_elements_by_class_name('experience-section')
                            sleep(2)
                            print(len(experience))
                            for anchor in experience:
                                s=anchor.find_element_by_tag_name('li')
                                position=s.text.split("\n")[0]
                                if position!="Company Name":
                                    print("position:",position)
                                    pro.position=position
                                else:
                                    pos=" "
                                    print("position:",pos)
                                    pro.position=pos


                                company=s.text.split("\n")[2]
                                if company!="Total Duration":
                                    print("company:",company)
                                    pro.company=company
                                else :
                                    com=s.text.split("\n")[1]
                                    print("company:",com)
                                    pro.company=com
                                    pro.message=Message()
                        except NoSuchElementException:
                            pass

                        pro.save()

            except NoSuchElementException:
                data=driver.find_element_by_class_name('search-no-results__image-container')
                driver.close()
                break

        return render(request,"index.html",{"data_saved":"All profiles data are saved in database"})

class connectbutton(TemplateView):
    template_name = 'index1.html'

    def post(self , request , *args , **kwargs):
        # firefox_options = webdriver.ChromeOptions()
        # firefox_options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path="E:\Programming\INTERNSHIP\Web Scrapping\facebook_new\chromedriver.exe")
        url = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
        driver.get(url)
        my_id = request.POST.get('uid')
        login_email = driver.find_element_by_id('username')
        login_email.send_keys(my_id)

        my_password = request.POST.get('pass')
        password = driver.find_element_by_id('password')
        password.send_keys(my_password)

        login_submit = driver.find_element_by_tag_name('button')
        login_submit.click()
        sleep(2)
        msg=Message()
        note=request.POST.get('addnote')
        print(note)
        if Message.objects.filter(text=note).count()!=0:
            pass
        else:
            msg.text=note
            msg.save()

        datas_from_db=Profile.objects.all()
        for obj in datas_from_db:
            print(obj.link)
            driver.get(obj.link)
            time.sleep(2)
            name=obj.name
            print(name)
            position=obj.position
            print(position)
            company=obj.company
            print(company)

            obj.message=msg
            try:
                obj.save()
            except ValueError:
                pass

            try:
                buttons = driver.find_elements_by_xpath('//button[contains(span,"Connect")]')
                for anchor in buttons:
                    print(anchor.text)
                    driver.execute_script("arguments[0].scrollIntoView(true);", anchor)
                    driver.execute_script("window.scrollBy(0,-100);")
                    driver.execute_script("arguments[0].click();", anchor)
                    # anchor.click()
                    sleep(2)

                    yes_or_no(driver, request , name, position, company, note)

                    sleep(10)
                    break

            except:
                more = driver.find_elements_by_xpath('//button[contains(span,"More")]')
                for anchor in more:
                    print(anchor.text)
                    driver.execute_script("arguments[0].scrollIntoView(true);", anchor)
                    driver.execute_script("window.scrollBy(0,-100);")
                    driver.execute_script("arguments[0].click();", anchor)
                    # anchor.click()
                    sleep(2)
                    c = driver.find_element_by_class_name('pv-s-profile-actions--connect')
                    print(c.text)
                    li_connect = c.find_element_by_xpath('//span[contains(text(),"Connect")]')
                    print(li_connect.text)
                    driver.execute_script("arguments[0].click();", li_connect)
                    # li_connect.click()

                    yes_or_no(driver, request, name , position, company,note)

                    sleep(10)
                    break

        return render(request,"index1.html",{"data_connected":"All people are connected"})

def linked_in_posts(request):
    if request.method == "POST":
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        option.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 2 
        })
        driver = webdriver.Chrome(chrome_options=option, executable_path=r"E:\Programming\INTERNSHIP\Web Scrapping\facebook_new\chromedriver.exe")
        url = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
        driver.get(url)
        time.sleep(3)
        my_id = request.POST.get('email')
        login_email = driver.find_element_by_id('username')
        login_email.send_keys(my_id)

        my_password = request.POST.get('password')
        password = driver.find_element_by_id('password')
        password.send_keys(my_password)
        login_submit = driver.find_element_by_tag_name('button')
        login_submit.click()
        sleep(3)
        profile_link = driver.find_element_by_xpath('//div[@data-control-name="identity_profile_photo"]')
        hover = ActionChains(driver).move_to_element(profile_link)
        hover.click().perform()
        sleep(5)
        print(driver.current_url)
        posts_url = str(driver.current_url) + 'detail/recent-activity/shares/'
        driver.get(posts_url)
        sleep(3)
        all_posts = driver.find_element_by_xpath("//div[@id='voyager-feed']").find_elements_by_xpath("./div")
        print(len(all_posts))
        for post in all_posts:
            print(1)
            LiPost = LinkedInPosts()
            date = post.find_element_by_xpath('.//span[contains(@class, "feed-shared-actor__sub-description")]/span/span[2]').text
            LiPost.posted_at = date
            text = post.find_element_by_xpath('.//div[contains(@class, "feed-shared-text")]/span/span').text
            LiPost.text = text
            menu = post.find_element_by_xpath('.//button[contains(@class, "feed-shared-control-menu")]')
            menu.click()
            sleep(4)
            flag = True
            copy_link = post.find_element_by_xpath('.//div[@class="artdeco-dropdown__content-inner"]/ul/li[3]/div')
            # driver.execute_script("arguments[0].scrollIntoView(true);", copy_link)
            # while flag:
            #     try:
            #         copy_link = post.find_element_by_xpath('.//div[@class="artdeco-dropdown__content-inner"]/ul/li[3]/div')
            #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #         flag = False
            #     except:
            #         flag = True
            copy_link.click()
            link = clipboard.paste()
            print(link)
            LiPost.post_link = link
            LiPost.save()
            print(2)
            sleep(3)
            print(date)
            print(text)
        return HttpResponse("Done")

    return render(request, 'linkedin_posts.html')

def linkedin_posts_delete(request):
    if request.method == "POST":
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        option.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 2 
        })
        driver = webdriver.Chrome(chrome_options=option, executable_path=r"E:\Programming\INTERNSHIP\Web Scrapping\facebook_new\chromedriver.exe")
        url = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
        driver.get(url)
        time.sleep(3)
        my_id = request.POST.get('email')
        login_email = driver.find_element_by_id('username')
        login_email.send_keys(my_id)

        my_password = request.POST.get('password')
        password = driver.find_element_by_id('password')
        password.send_keys(my_password)
        login_submit = driver.find_element_by_tag_name('button')
        login_submit.click()
        sleep(3)

        all_posts = LinkedInPosts.objects.all()
        for post in all_posts:
            driver.get(post.post_link)
            menu = driver.find_element_by_xpath('//button[contains(@class, "feed-shared-control-menu")]')
            menu.click()
            sleep(3)
            delete = driver.find_element_by_xpath('//div[@class="artdeco-dropdown__content-inner"]/ul/li[6]/div')
            delete.click()
            sleep(3)
            confirm = driver.find_element_by_xpath('//button[@data-control-name="deleteshares.delete"]')
            confirm.click()

        return HttpResponse('Done')
    else:
        return render(request, 'linked_posts_delete.html')

def yes_or_no(driver, request , name, position , company,note):
    yes = request.POST.get('y')
    if yes == 'y':
        if len(note)!=0:
            popup_button(driver, request ,name, position ,company, note)
        else:
            Done(driver, request)

    else:
        Done(driver, request)


def popup_button(driver,request,name,position,company,note):
    button_addnote = driver.find_element_by_xpath('//button[contains(span,"Add a note")]')
    print(button_addnote.text)
    print("this")
    driver.execute_script("arguments[0].scrollIntoView(true);", button_addnote)
    driver.execute_script("window.scrollBy(0,-100);")
    button_addnote.click()
    sleep(2)
    text_area = driver.find_element_by_xpath('//textarea')

    # msg=Message()

    print("text_a:",name)
    first_name=name.split(" ")[0]
    print("first_name:",first_name)
    last_name=name.split(" ")[1]
    print("last_name:",last_name)

    if '[[first_name]]' in note:
        n = note.replace('[[first_name]]', first_name)
        note=n
    if '[[last_name]]' in note:
        m=note.replace('[[last_name]]',last_name)
        note=m
    if '[[position]]' in note:
        p=note.replace('[[position]]',position)
        note=p
    if '[[company]]' in note:
        c=note.replace('[[company]]',company)
        note=c

    print(note)
    text_area.send_keys(note)
    Done(driver, request)

def Done(driver, request):
    button_done = driver.find_element_by_xpath('//button[contains(span,"Send")]')
    print(button_done.text)
    driver.execute_script("arguments[0].scrollIntoView(true);", button_done)
    driver.execute_script("window.scrollBy(0,-100);")
    driver.execute_script("arguments[0].click();", button_done)
    # button_done.click()
    sleep(2)


class userconnection(TemplateView):
    template_name = 'index2.html'

    def post(self,request, *args, **kwargs):
        driver = webdriver.Chrome(executable_path="./chromedriver.exe")
        url = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
        driver.get(url)
        time.sleep(3)
        my_id = request.POST.get('uid')
        login_email = driver.find_element_by_id('username')
        login_email.send_keys(my_id)

        my_password = request.POST.get('pass')
        password = driver.find_element_by_id('password')
        password.send_keys(my_password)

        login_submit = driver.find_element_by_tag_name('button')
        login_submit.click()
        sleep(2)
        connection_link=request.POST.get('connectionlink')
        print("profile_link:",connection_link)
        if Profile.objects.filter(link=connection_link).count()==0:
            pro=Profile()
        else:
            pro=Profile.objects.filter(link=connection_link).first()
        print(connection_link)
        pro.link=connection_link

        driver.get(connection_link)
        sleep(2)

        name = driver.find_element_by_xpath(
        "//div[@class='flex-1 mr5']/ul[@class='pv-top-card--list inline-flex align-items-center']/li")
        name = name.text
        f_name = name.split(" ")[0]
        print("first name: ", f_name)

        l_name = ((name.split(" "))[1]).split("\n")[0]
        print("last name: ", l_name)
        names = f_name + " " + l_name
        print("name:", names)
        if "(" in l_name:
            print(f_name)
            pro.name = f_name
        else:
            print(names)
            pro.name = names

        heading = driver.find_element_by_xpath("//div[@class='flex-1 mr5']/h2")
        print("heading:", heading.text)
        pro.heading = heading.text

        sleep(3)
        scroll_page(driver)

        sleep(5)
        experience = driver.find_elements_by_class_name('experience-section')
        sleep(2)
        print(len(experience))
        for anchor in experience:
            s = anchor.find_element_by_tag_name('li')
            position = s.text.split("\n")[0]
            if position != "Company Name":
                print("position:", position)
                pro.position = position
            else:
                pos = " "
                print("position:", pos)
                pro.position = pos
            company = s.text.split("\n")[2]
            if company != "Total Duration":
                print("company:", company)
                pro.company = company
            else:
                com = s.text.split("\n")[1]
                print("company:", com)
                pro.company = com

        pro.save()

        profile_data=driver.find_element_by_class_name('mr5')
        a_tag=profile_data.find_element_by_xpath('//a[contains(@href,"Connection")]')

        s=a_tag.get_attribute("href")
        print(s)

        count_of_url = 0
        page_number = 0
        count_of_element=0
        while count_of_url < 1000:
            page_number = page_number + 1
            page_number = str(page_number)
            if count_of_url<1000:
                driver.get(s+'&page='+page_number)
            count_of_url = count_of_url + 1
            page_number = int(page_number)
            print("page_number:",page_number)
            sleep(5)
            try:
                element_total=driver.find_element_by_class_name('pb2')
                e_total=element_total.text
                print("element_total:",e_total)
                data = driver.find_element_by_class_name('search-results-page')

                scroll_page(driver)
                sleep(2)
                data_of_one=data.find_elements_by_class_name('reusable-search__result-container')

                for anchor in data_of_one:
                    profile_link = anchor.find_element_by_class_name('app-aware-link')
                    p_link=profile_link.get_attribute("href")
                    if Profile.objects.filter(link=p_link).count()==0:
                        database=Profile()
                    else:
                        database=Profile.objects.filter(link=p_link).first()
                    print(p_link)
                    database.link=p_link

                    print("name:",anchor.text.split("\n")[0])
                    database.name=anchor.text.split("\n")[0]

                    print("heading:",anchor.text.split("\n")[3])
                    database.heading=anchor.text.split("\n")[3]

                    database.save()
                    database.mutual.add(pro)

                    count_of_element=count_of_element+1
                    count(count_of_element)

                    print("----------------------------------------------------------")

            except NoSuchElementException:

                data=driver.find_element_by_class_name('search-no-results__image-container')
                driver.close()
                break

        return render(request,"index2.html",{'count_of_elements':count_of_element , 'element_total':e_total})


def count(count_of_element):
    c=0
    c=c+count_of_element
    print("c:",c)
    return c

class yellow(TemplateView):
    template_name = 'bindex1.html'

    def post(self, request, *args, **kwargs):
        self.path = "///home/aman/pythonmate/Yelp"
        self.driver = webdriver.Chrome("./chromedriver.exe")
        name = request.POST.get('name')
        print('name:', name)
        location = request.POST.get('State')
        print('location:', location)
        sub_location = request.POST.get('SubState')
        print('sub_location:', sub_location)

        count_of_url = 0
        page_number = 0
        while count_of_url < 1000:
            page_number = page_number + 1
            page_number = str(page_number)

            if count_of_url < 1000:
                url = 'https://www.yellowpages.com/search?search_terms=' + name + '&geo_location_terms=' + location + '%2C+' + sub_location + '&page=' + page_number

                self.url = url
                self.driver.get(self.url)
                sleep(7)

            count_of_url = count_of_url + 1
            page_number = int(page_number)

            self.anchors = self.driver.find_elements_by_xpath(
                '//a[@class="business-name"]')
            pure_href = []

            for anchor in self.anchors:
                if not (anchor.text).isnumeric():
                    pure_href.append(anchor.get_attribute("href"))
            if pure_href != []:

                print("pure_href", pure_href)
                for href in pure_href:
                    yp = Business()
                    if "?" in href:
                        href=href.split("?")[0]
                    print(href)
                    if Business.objects.filter(source_url=href).count() != 0:
                        continue
                    else:
                        self.driver.get(href)
                        sleep(2)

                        date = datetime.datetime.now()
                        print("time:{:%d/%m/%y %H:%M:%S}".format(date))

                        yp.source_url=href

                        try:
                            self.name = self.driver.find_elements_by_xpath(
                                '//*[@id="main-header"]/article/div/h1')
                            self.name = self.name[0].text
                            print("name:  ", self.name)

                            yp.name = self.name
                        except:
                            self.name = self.driver.find_elements_by_xpath(
                                '//article[@class="business-card clearfix paid-listing"]/div[@class="sales-info"]/h1')
                            self.name = self.name.text
                            print("name: ", self.name)

                            yp.name = self.name

                        self.visit_site = self.driver.find_elements_by_xpath(
                            '//div[@class="business-card-footer"]/a[@class="primary-btn website-link"]')
                        for anchor in self.visit_site:
                            print("visit_site:", anchor.get_attribute("href"))
                            yp.visit_site = anchor.get_attribute("href")

                        self.email = self.driver.find_elements_by_xpath(
                            '//div[@class="business-card-footer"]/a[@class="email-business"]')
                        for anchor in self.email:
                            s = anchor.get_attribute("href").split(":")[1]
                            print("email:", s)
                            yp.email = s

                        self.number = self.driver.find_element_by_xpath('//div[@class="contact"]/p[@class="phone"]')
                        print("number: ", self.number.text)
                        yp.number = self.number.text

                        self.address = self.driver.find_elements_by_xpath(
                            '//div[@class="contact"]/h2[@class="address"]')
                        self.address_list = []
                        for i in self.address:
                            self.address_list.append(i.text)
                        self.address = " ".join(self.address_list)

                        print("full_address: ", self.address)
                        spliting_address = self.address.split()

                        self.city = self.address.split(",")[-2]
                        print("city:", self.city)

                        self.state = spliting_address[-2]
                        print("state:", self.state)

                        self.country = "United States"
                        print("country:", self.country)

                        self.zipcode = spliting_address[-1]
                        print("zipcode:", self.zipcode)

                        self.w_t_search = name
                        self.location = location
                        self.sub_location = sub_location
                        self.search_term = self.w_t_search + "," + self.location + "," + self.sub_location
                        print(self.search_term)

                        yp.address = self.address
                        yp.city = self.city
                        yp.state = self.state
                        yp.country = self.country
                        yp.zip = self.zipcode
                        yp.search_term = self.search_term

                        print("---------------------------------------------")

                        yp.save()

            elif pure_href == []:
                break
        return HttpResponse('Data Saved in Database')
    

def facebook(request):
    if request.method == "POST":
        e = request.POST.get('email')
        p = request.POST.get('password')

        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        option.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 2 
        })

        #logging in to the facebook website
        driver = webdriver.Chrome(chrome_options = option, executable_path=r'E:\Programming\INTERNSHIP\Web Scrapping\facebook_new\chromedriver.exe')
        facebook_login_url = 'https://www.facebook.com/?stype=lo&jlou=AfdmyGqkrTrtRiR6_va0yS9OpPGEeY0QfhdyH62wIh0mFtyGG6MSd2Ux4w7f8GrrLGB5DYXyT5fVNBW2mJlNysyNv6-L8plwzDI1R7ppxMeBng&smuh=10160&lh=Ac_J_6o9clpjnZUE4ds'
        driver.get(facebook_login_url)
        email = driver.find_element_by_xpath('//*[@id="email"]')
        email.send_keys(e)
        sleep(1)
        password = driver.find_element_by_xpath('//*[@id="pass"]')
        password.send_keys(p)
        sleep(1)
        login = driver.find_element_by_tag_name('button')
        login.click()
        sleep(2)
        profile_link = driver.find_elements_by_xpath('//li/div[@data-visualcompletion="ignore-dynamic"]/a')
        profile_link = profile_link[0].get_attribute("href")
        driver.get(profile_link)
        sleep(2)

        #applying filter to show only posts posted by user
        
        filters = driver.find_element_by_xpath('//div[@aria-label="Filters"]')
        driver.execute_script("arguments[0].click();", filters)
        sleep(2)
        posted_by = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div[2]/div[2]/div/div/div/div').send_keys('You')
        posted_by = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div[2]/div[2]/div/div/div/div').send_keys(Keys.RETURN)
        sleep(2)
        done = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[3]/div/div[1]/div[1]').send_keys(Keys.RETURN)

        #logic for scrolling to get desired number of posts
        scroll_pause_time = 2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 1

        def count_greater_than_required(driver, count):
            no_of_posts_loaded = len(driver.find_elements_by_xpath('//div[@data-pagelet="ProfileTimeline"]/div')) 
            if no_of_posts_loaded-3>count:
                return True
            else:
                return False

        count = int(request.POST.get('count'))

        count_of_posts_added_to_database = 0

        while True:
            # scroll one screen height each time
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1

            sleep(3)
            posts = driver.find_elements_by_xpath('//div[@data-pagelet="ProfileTimeline"]/div')
            required_posts = posts[:-2]
            # remaining_posts = count - count_of_posts_added_to_database
            # next_slice_count_for_posts = 2 if remaining_posts>2 else remaining_posts
            for post in required_posts[count_of_posts_added_to_database:count_of_posts_added_to_database+1]:
                if count != -1:
                    if count_of_posts_added_to_database == count:
                        break
                try:
                    date = post.find_element(By.XPATH, './/span/span/span[2]/span/a/span').text
                    post_link = str(post.find_element(By.XPATH, './/span/span/span[2]/span/a').get_attribute("href"))
                except:
                    date = post.find_element(By.XPATH, './/span/span/a').text
                text = post.find_element(By.XPATH, './/div[@data-ad-preview="message"]/div/div/span/div/div').text
                print(text)
                temp = post.find_elements_by_xpath('.//img')
                countxx = 0
                p = Facebook()
                p.date_time = date
                p.post_link = post_link
                p.header = text
                p.save()
                count_of_posts_added_to_database+=1

                for img in temp:                
                    if 'scontent' in str(img.get_attribute("src")):
                        imgx = Image()
                        imgx.url = str(img.get_attribute("src"))
                        imgx.post = p
                        imgx.save()
                    if 'giphy' in str(img.get_attribute("src")):
                        gifx = GIF()
                        gifx.url = str(img.get_attribute("src"))
                        gifx.post = p
                        gifx.save()
                print(countxx)
                # temp.pop(0)
                # temp.pop(-1)
                print(len(temp))
                print(date)                    

                
            if count != -1:
                if count_of_posts_added_to_database == count:
                    break
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break
        sleep(3)
                
        # required_posts = None

        # if count!=-1:
        #     required_posts = driver.find_elements_by_xpath('//div[@data-pagelet="ProfileTimeline"]/div')
        #     required_posts.pop(-1)
        #     required_posts.pop(-2)
        #     required_posts = required_posts[:count]
        # else :

        #     required_posts = driver.find_elements_by_xpath('//div[@data-pagelet="ProfileTimeline"]/div')
        #     required_posts.pop(-1)
        #     required_posts.pop(-2)

        # for post in required_posts:
        #     print(type(post))
        #     try:
        #         date = post.find_element(By.XPATH, './/span/span/span[2]/span/a/span').text
        #     except:
        #         date = post.find_element(By.XPATH, './/span/span/a').text
        #     p = Facebook()
        #     p.date_time = date
        #     p.save()
        #     print(date)
        
        return HttpResponse('Posts saved in database')
    else:
        return render(request, 'facebook_form.html')


def delete_facebook(request):
    if request.method == 'POST':
        e = request.POST.get('email')            
        p = request.POST.get('password')

        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        option.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 2 
        })

        #logging in to the facebook website
        driver = webdriver.Chrome(chrome_options = option, executable_path=r'E:\Programming\INTERNSHIP\Web Scrapping\facebook_new\chromedriver.exe')
        facebook_login_url = 'https://www.facebook.com/?stype=lo&jlou=AfdmyGqkrTrtRiR6_va0yS9OpPGEeY0QfhdyH62wIh0mFtyGG6MSd2Ux4w7f8GrrLGB5DYXyT5fVNBW2mJlNysyNv6-L8plwzDI1R7ppxMeBng&smuh=10160&lh=Ac_J_6o9clpjnZUE4ds'
        driver.get(facebook_login_url)
        email = driver.find_element_by_xpath('//*[@id="email"]')
        email.send_keys(e)
        sleep(1)
        password = driver.find_element_by_xpath('//*[@id="pass"]')
        password.send_keys(p)
        sleep(1)
        login = driver.find_element_by_tag_name('button')
        login.click()
        all_posts = Facebook.objects.all()
        for post in all_posts:
            print(post.post_link)
            print(type(post.post_link))
            driver.get(post.post_link)
            driver.get(post.post_link)
            print(driver.current_url)
            sleep(5)
            button = driver.find_elements_by_xpath('//div[@aria-haspopup="menu"]')[1]
            driver.execute_script("arguments[0].click();", button)
            sleep(5)
            
            options = driver.find_elements_by_xpath('//div[@data-pagelet="root"]/div/div/div/div/div/div[@role="menuitem"]')
            edit = None
            delete = None
            for option in options:
                option.find_element_by_xpath('.//span')
                if option.text == "Edit post" and edit==None:
                    edit = option
                    break            
                else:
                    continue
            
            print(delete)

            hover = ActionChains(driver).move_to_element(edit)
            hover.click().perform()
            write_text = ActionChains(driver)
            write_text.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
            sleep(2)
            write_text.send_keys("-")
            sleep(1)
            write_text.perform()
            sleep(2)
            try:
                remove_attachments = driver.find_element_by_xpath('//div[@aria-label="Remove Post Attachment"]')
                remove_attachments.click()
                sleep(3)
            except:
                pass
            save = driver.find_element_by_xpath('//div[@aria-label="Save"]')
            save.click()
            sleep(5)
            # button = driver.find_elements_by_xpath('//div[@aria-haspopup="menu"]')[1]
            driver.execute_script("arguments[0].click();", button)
            sleep(4)
            options = driver.find_elements_by_xpath('//div[@data-pagelet="root"]/div/div/div/div/div/div[@role="menuitem"]')
            print(options)
            for option in options:
                abc = option.find_element_by_xpath('.//span')
                print(abc.text)
                if abc.text == "Delete post" and delete == None:
                    delete = option
                    break
                else:
                    continue
            print(delete)
            sleep(6)
            hover = ActionChains(driver).move_to_element(delete)
            hover.click().perform()
                
                
            sleep(4)
            confirm = driver.find_elements_by_xpath('//div[@aria-label="Delete"]')[0]
            confirm.click()
            sleep(3)
            post.delete()

        return  ("All posts deleted.")
    else:
        return render(request, 'facebook_delete.html')

def main(request):
    current_site = get_current_site(request)
    admin = str(current_site) + '/admin'
    context = {'admin':admin}
    return render(request, 'main2.html', context)








