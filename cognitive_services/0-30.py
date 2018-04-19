from datetime import date
import operator
import vk_api
import requests
import matplotlib.pyplot as plt
import numpy as np

subscription_key = "b67909c8a6c247bfbe245488bb231b09"
assert subscription_key
vision_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v1.0/"
vision_analyze_url = vision_base_url + "analyze"
headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
params   = {'visualFeatures': 'Categories,Tags,Description'}

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

def doInclude(vk, id):
    result = vk.users.get(user_ids=id, fields="bdate")
    age = -1
    for i in result:
        if "bdate" not in i:
            return -1
        bdate= i["bdate"]
        splited_date = bdate.split(".")
        if len(splited_date) < 3:
            return -1
        age = calculateAge(splited_date)
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

def drawTagStats(tag_to_draw):
    x = [0, 1, 2, 3, 4]
    freq = []
    file = open('./tags.txt', 'r')
    amounts = ""
    for line in file:
        if str(line) == str(tag_to_draw + "\n"):
            total_cnt = file.readline()
            amounts = total_cnt.split(',')
            break
    if amounts == "":
        print("There is no such tag: " + str(tag_to_draw))
        return
    for a in amounts:
        freq.append(a)
    width = 1

    fig, ax = plt.subplots()
    ax.bar(1, int(amounts[0]), width)
    ax.bar(1 + width, int(amounts[1]), width=width, color='red')
    ax.bar(1 + 2 * width, int(amounts[2]), width=width, color='green')
    ax.bar(1 + 3 * width, int(amounts[3]), width=width, color='pink')
    ax.bar(1 + 4 * width, int(amounts[4]), width=width, color='orange')

    ax.set_ylabel('Amount of tags in age range')
    ax.set_title('Tag: ' + tag_to_draw)
    ax.set_xticks(np.add(x, (width / 2)))
    ax.set_xticklabels(('0-10', '10-13', '13-18', '18-30', '30+'))
    ax.text(1, 1.05 * int(amounts[0]),
            '%d' % int(amounts[0]), ha='center', va='bottom')
    ax.text(2, 1.05 * int(amounts[1]),
            '%d' % int(amounts[1]), ha='center', va='bottom')
    ax.text(3, 1.05 * int(amounts[2]),
            '%d' % int(amounts[2]), ha='center', va='bottom')
    ax.text(4, 1.05 * int(amounts[3]),
            '%d' % int(amounts[3]), ha='center', va='bottom')
    ax.text(5, 1.05 * int(amounts[4]),
            '%d' % int(amounts[4]), ha='center', va='bottom')
    plt.show()

def cloudOfTagsInRange(map):
    if len(map) == 0:
        print("No tags")
        return
    sorted_x = sorted(map.items(), key=operator.itemgetter(1), reverse=True)
    cnt = 0
    for tag in sorted_x:
        print(tag)
        cnt = cnt + 1
        if cnt >= 10:
            break

def cloudOfTagsTotal():
    sorted_x = sorted(main_map.items(), key=operator.itemgetter(1), reverse=True)
    print("10 most popular tags:")
    cnt = 0
    for tag in sorted_x:
        print(tag)
        cnt = cnt + 1
        if cnt >= 10:
            break
    return sorted_x[0][0]

def analyze(id):
    file = open('C:\\Users\\Nastya\\Desktop\\nst\\vkvk.txt', 'r')
    data_file = open('./data_file.txt', 'w')
    login = file.readline()
    password = file.readline()
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()

    friends_id = vk.friends.get(user_id=id)["items"]
    cnt_of_friends = 0
    for friend_id in friends_id:
        if cnt_of_friends % 5 == 0:
            print("Already " + str(cnt_of_friends) + " friends")
        cnt_of_friends = cnt_of_friends + 1
        age = doInclude(vk, friend_id)
        if age == -1:
            #print("pass")
            continue
        # data_file.write(str(friend_id) + "\n")
        # data_file.write(str(age) + "\n")
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
        photos = getLastPhotos(vk, friend_id, 25)
        for photo in photos:
            try:
                image_url = photo["photo_604"]
                # print(image_url)
                data = {'url': image_url}
                response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
                response.raise_for_status()
                analysis = response.json()
                image_caption = analysis["description"]["tags"]

                for tag in image_caption:
                    if not tag in main_map:
                        main_map[tag] = 1
                    else:
                        main_map[tag] += 1

                    if not tag in map:
                        map[tag] = 1
                    else:
                        map[tag] += 1
            except Exception as err:
                print(err)
                continue
        #print(map)
        # if cnt_of_friends > 15:
        #     break
    data_file.write("0-10\n")
    writeStatsOfRange(map_0_10, data_file)
    data_file.write("10-13\n")
    writeStatsOfRange(map_10_13, data_file)
    data_file.write("13-18\n")
    writeStatsOfRange(map_13_18, data_file)
    data_file.write("18-30\n")
    writeStatsOfRange(map_18_30, data_file)
    data_file.write("30+\n")
    writeStatsOfRange(map_30, data_file)
    data_file.write("total\n")
    writeStatsOfRange(main_map, data_file)

    print("10 most popular tags in range 0-10:")
    cloudOfTagsInRange(map_0_10)
    print("10 most popular tags in range 10-13:")
    cloudOfTagsInRange(map_10_13)
    print("10 most popular tags in range 13-18:")
    cloudOfTagsInRange(map_13_18)
    print("10 most popular tags in range 18-30:")
    cloudOfTagsInRange(map_18_30)
    print("10 most popular tags in range 30+:")
    cloudOfTagsInRange(map_30)
    file.close()
    data_file.close()

def writeStatsOfRange(map, file):
    if len(map) == 0:
        file.write("null\n")
        return
    sorted_x = sorted(map.items(), key=operator.itemgetter(1), reverse=True)
    for tag in sorted_x:
        file.write(tag[0])
        file.write(':')
        file.write(str(tag[1]))
        file.write(',')
    file.write("\n")

def statistics():
    tags_file = open('./tags.txt', 'w')
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
        ts = TagsStatistics(main_tag, cnt0, cnt10, cnt13, cnt18, cnt30, main_map[main_tag])
        writeTag(ts, tags_file)
    tags_file.close()

def writeTag(tag, file):
    file.write(tag.name_of_tag)
    file.write("\n")
    file.write(str(tag.count_0_10) + "," + str(tag.count_10_13) + "," + str(tag.count_13_18)
               + "," + str(tag.count_18_30) + "," + str(tag.count_30) + "\n")

analyze(21937508)
statistics()
popular=cloudOfTagsTotal()
drawTagStats(str(popular))
