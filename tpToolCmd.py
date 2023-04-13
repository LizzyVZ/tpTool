import os
import re
import json

folder_path = input("请输入目标文件夹路径: ")

json_files = []
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):
        with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as json_file:
            json_content = json.load(json_file)
            json_files.append({'file_name': file_name, 'content': json_content})

print(f"已经读取了 {len(json_files)} 个 JSON 文件。")

# 获取命名规则
while True:
    index = input("请输入序号（仅限数字）：")
    area = input("请输入地区（仅限数字、英文和中文）：")
    sub_area = input("请输入子区（仅限数字、英文和中文）：")

    tail_start = input("请输入尾号的起始数字：")
    if not (re.match(r"^\d+$", tail_start) and len(tail_start) <= 5):
        print("尾号的起始数字必须为不超过5位的数字，请重新输入！")
        continue

    # 对输入进行验证
    if not (re.match(r"^\d+$", index) and len(index) <= 5):
        print("序号必须为不超过5位的数字，请重新输入！")
        continue
    elif not (re.match(r"^[\u4e00-\u9fa5a-zA-Z0-9]+$", area) and len(area) <= 10):
        print("地区必须为不超过10位的数字、英文或中文，请重新输入！")
        continue
    elif not (re.match(r"^[\u4e00-\u9fa5a-zA-Z0-9]+$", sub_area) and len(sub_area) <= 10):
        print("子区必须为不超过10位的数字、英文或中文，请重新输入！")
        continue
    else:
        break

# 进行批量重命名和修改JSON文件中的"name"键对应的值
for i, json_file in enumerate(json_files):
    file_name = json_file['file_name']
    json_content = json_file['content']

    tail = str(int(tail_start) + i).zfill(3)
    new_name = f"{index}_{area}_{sub_area}_{tail}.json"

    # 修改JSON文件中的"name"键对应的值
    if 'name' in json_content:
        json_content['name'] = new_name

    with open(os.path.join(folder_path, file_name), 'w', encoding='utf-8') as json_file:
        json.dump(json_content, json_file, indent=4, ensure_ascii=False)

    os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_name))

print(f"已经成功重命名了 {len(json_files)} 个 JSON 文件。")


######################################################################################
######################################################################################
######################################################################################
