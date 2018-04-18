from datetime import date
import operator
import vk_api
import cognitive_face as cf
import requests
import matplotlib.pyplot as plt
import numpy as np

face_api_key = "b67909c8a6c247bfbe245488bb231b09"
cf.Key.set(face_api_key)
face_api_url = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0'
cf.BaseUrl.set(face_api_url)

subscription_key = "b67909c8a6c247bfbe245488bb231b09"
assert subscription_key

vision_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v1.0/"
vision_analyze_url = vision_base_url + "analyze"

#image_url = "https://pp.userapi.com/c847122/v847122022/2451b/eA36MWEh_H4.jpg"

headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
params   = {'visualFeatures': 'Categories,Tags,Description'}
# data     = {'url': image_url}
# response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
# response.raise_for_status()
# analysis = response.json()
# image_caption = analysis["description"]["tags"]
# #print(image_caption)

class TagsStatistics:
    name_of_tag = ""
    count_0_10 = 0
    count_10_13 = 0
    count_13_18 = 0
    count_18_30 = 0
    count_30 = 0
    count_total = 0
    def __init__(self, name, c0, c10, c13, c18, c30, t):
        self.name_of_tag = name
        self.count_0_10 = c0
        self.count_10_13 = c10
        self.count_13_18 = c13
        self.count_18_30 = c18
        self.count_30 = c30
        self.count_total = t
    def print_tag(self):
        print("name: " + self.name_of_tag + " 0-10: " + str(self.count_0_10) + ", 10-13: " + str(self.count_10_13)
              + ", 13-18: " + str(self.count_13_18) + ", 18-30: " + str(self.count_18_30) + ", 30+: " + str(self.count_30))

def calculateAge(splited_date):
    day = int(splited_date[0])
    month = int(splited_date[1])
    year = int(splited_date[2])
    today = date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

def do_include(vk, id):
    result = vk.users.get(user_ids=id, fields="bdate")
    for i in result:
        if "bdate" not in i:
            #print("no bdate")
            return -1
        bdate= i["bdate"]
        splited_date = bdate.split(".")
        if len(splited_date) < 3:
            #print("no year")
            return -1
        #print("yes")
        #print(bdate)
        age = calculateAge(splited_date)
        #print(age)
    return age

def getLastPhotos(vk, id, count=1):
    result = vk.photos.getAll(owner_id=id, count=count)
    return result["items"]

map_0_10 = {}
map_10_13 = {}
map_13_18 = {}
map_18_30 = {}
map_30 = {}
main_map = {}
list_of_tags = []

def draw_changes(tg):
    # plt.title(tg)
    x = [0, 1, 2, 3, 4]
    freq = []

    cur_tag = list_of_tags[0]
    for tag in list_of_tags:
        if tag.name_of_tag == tag:
            cur_tag = tag
            break
    freq.append(cur_tag.count_0_10)
    freq.append(cur_tag.count_10_13)
    freq.append(cur_tag.count_13_18)
    freq.append(cur_tag.count_18_30)
    freq.append(cur_tag.count_30)
    #cur_tag.print_tag()

    # y = np.array(stat)
    # data1 = cur_tag.count_0_10
    # data2 = cur_tag.count_10_13
    # data3 = cur_tag.count_13_18
    # data4 = cur_tag.count_18_30
    # data5 = cur_tag.count_30
    # locs = np.arange(1, 2)
    # width = 0.27
    # plt.bar(locs, data1, width=width)
    # plt.bar(locs + width, data2, width=width, color='red')
    # plt.bar(locs + 2 * width, data3, width=width, color='green')
    # plt.bar(locs + 3 * width, data4, width=width, color='pink')
    # plt.bar(locs + 4 * width, data5, width=width, color='orange')
    #
    # plt.xticks(locs + width * 1.5, locs)

###
    width = 1

    fig, ax = plt.subplots()
    rect1 = ax.bar(1, cur_tag.count_0_10, width)
    rect2 = ax.bar(1 + width, cur_tag.count_10_13, width=width, color='red')
    rect3 = ax.bar(1 + 2 * width, cur_tag.count_13_18, width=width, color='green')
    rect4 = ax.bar(1 + 3 * width, cur_tag.count_18_30, width=width, color='pink')
    rect5 = ax.bar(1 + 4 * width, cur_tag.count_30, width=width, color='orange')

    ax.set_ylabel('Amount of tags in age range')
    ax.set_title('Tag: ' + tg)
    ax.set_xticks(np.add(x, (width / 2)))  # set the position of the x ticks
    ax.set_xticklabels(('0-10', '10-13', '13-18', '18-30', '30+'))
    ax.text(1, 1.05 * cur_tag.count_0_10,
            '%d' % int(cur_tag.count_0_10), ha='center', va='bottom')
    ax.text(2, 1.05 * cur_tag.count_10_13,
            '%d' % int(cur_tag.count_10_13), ha='center', va='bottom')
    ax.text(3, 1.05 * cur_tag.count_13_18,
            '%d' % int(cur_tag.count_13_18), ha='center', va='bottom')
    ax.text(4, 1.05 * cur_tag.count_18_30,
            '%d' % int(cur_tag.count_18_30), ha='center', va='bottom')
    ax.text(5, 1.05 * cur_tag.count_30,
            '%d' % int(cur_tag.count_30), ha='center', va='bottom')

    # def autolabel(rect):
    #     height = rect.get_height()
    #     ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
    #             '%d' % int(height),
    #             ha='center', va='bottom')
    #
    # autolabel(rect1)
    # autolabel(rect2)
    # autolabel(rect3)
    # autolabel(rect4)
    # autolabel(rect5)

    plt.show()





def cloudOfTags():
    sorted_x = sorted(main_map.items(), key=operator.itemgetter(1), reverse=True)
    print("Cloud of 50 most popular tags:")
    cnt = 0;
    for tag in sorted_x:
        print(tag)
        cnt = cnt + 1
        if cnt >= 50:
            break

def analyze():
    file = open('C:\\Users\\Nastya\\Desktop\\nst\\vkvk.txt', 'r')
    login = file.readline()
    password = file.readline()
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()

    #print("friends: ")
    friends_id = vk.friends.get()["items"]
    cnt_of_friends = 0
    for friend_id in friends_id:
        #print(friend_id)
        text_tags = ""
        age = do_include(vk, friend_id)
        if age == -1:
            #print("pass")
            continue
        if age >= 0 and age < 10:
            #print("my map is 0-10")
            map = map_0_10
        elif age >= 10 and age < 13:
            #print("my map is 10-13")
            map = map_10_13
        elif age >= 13 and age < 18:
            #print("my map is 13-18")
            map = map_13_18
        elif age >= 18 and age < 30:
            #print("my map is 18-30")
            map = map_18_30
        else:
            #print("my map is 30+")
            map = map_30
        photos = getLastPhotos(vk, friend_id, 8)
        for photo in photos:
            #print(photo["photo_604"])
            image_url = photo["photo_604"]
            data = {'url': image_url}

            #response = FaceApi.util.request(image_url, data, headers=headers, params=params)
            #print(response)
            # response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
            # response.raise_for_status()
            # analysis = response.json()

            response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
            response.raise_for_status()
            analysis = response.json()
            image_caption = analysis["description"]["tags"]
            #print(image_caption)


            for tag in image_caption:
                #print(tag)
                text_tags = text_tags + " " + str(tag)
                if not tag in main_map:
                    main_map[tag] = 1
                else:
                    main_map[tag] += 1

                if not tag in map:
                    map[tag] = 1
                else:
                    map[tag] += 1
        #print(map)
        cnt_of_friends = cnt_of_friends + 1
        if cnt_of_friends > 20:
            break
    #print("main map") #unsorted map of whole tags
    #print(main_map)

def statistics():
    for main_tag in main_map:
        cnt0 = 0
        cnt10 = 0
        cnt13 = 0
        cnt18 = 0
        cnt30 = 0
        if main_tag in map_0_10:
            cnt0 = cnt0 + map_0_10[main_tag]
        if main_tag in map_10_13:
            cnt10 = cnt10 + map_10_13[main_tag]
        if main_tag in map_13_18:
            cnt13 = cnt13 + map_13_18[main_tag]
        if main_tag in map_18_30:
            cnt18 = cnt18 + map_18_30[main_tag]
        if main_tag in map_30:
            cnt30 = cnt30 + map_30[main_tag]
        #print("tag: " + str(main_tag) + ", 18-30: " + str(cnt18) + ", 30+: " + str(cnt30))
        ts = TagsStatistics(main_tag, cnt0, cnt10, cnt13, cnt18, cnt30, main_map[main_tag])
        list_of_tags.append(ts)
    # for tag in list_of_tags:
    #     print("name: " + tag.name_of_tag + " 18-30: " + str(tag.count_18_30) + " total: " + str(tag.count_total))
    #photos = getLastPhotos(vk, 112394, 2)
    #bdate = do_include(vk, 112394)  # 2043939
    # for photo in photos:
    #     print(photo["photo_604"])

analyze()
statistics()
draw_changes("person")
    # vk = vk_session.get_api()
    # response = vk.wall.get(count=1)  # Используем метод wall.get
    #
    # if response['items']:
    #     print(response['items'][0])

    # response = vk.users.get(user_ids=id,
    #                         fields=["photo_50"])  # Используем метод wall.get

    #print(response)

#analyze(71930087)

# headers = {'Ocp-Apim-Subscription-Key': "0a085c1d6c034a4c95a4798712e7942c"}
# params = {
#     'returnFaceId': 'true',
#     'returnFaceLandmarks': 'false',
#     'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
# }
# response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
# print(response)
# print(response.json())