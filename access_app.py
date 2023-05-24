#from user_page_module import build_user_page
l = [(1, 2), (4, 3), (5, 7), (9, 13)]
values = [1, 2, 5, 6, 8, 9, 0]

results = [all(member in values for member in tpl) for tpl in l]
print(results)  # Output: [True, False, True, False]
