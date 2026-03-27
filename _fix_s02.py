with open(r'c:\Users\admin\Downloads\ML\Lab01_3B1B\drivex\scenes\part01\p01_s02_genai_boom.py', encoding='utf-8') as f:
    content = f.read()

old_bubble = 'PIBubble(pi, "Foundation Model\nlà gì vậy?",\n                          position=UP + RIGHT, font_size=18)'
new_bubble = 'PIBubble(pi, "What is a\nFoundation Model?",\n                          position=UP + RIGHT, font_size=18)'
content = content.replace(old_bubble, new_bubble)

old_arr1 = 'arr_train = Arrow(\n            data_col.get_right(), model_grp.get_left(),'
new_arr1 = 'arr_train = Arrow(\n            data_col.get_right(), model_box.get_left(),'
content = content.replace(old_arr1, new_arr1)

old_arr2 = 'arr_adapt = Arrow(\n            model_grp.get_right(), task_col.get_left(),'
new_arr2 = 'arr_adapt = Arrow(\n            model_box.get_right(), task_col.get_left(),'
content = content.replace(old_arr2, new_arr2)

with open(r'c:\Users\admin\Downloads\ML\Lab01_3B1B\drivex\scenes\part01\p01_s02_genai_boom.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
