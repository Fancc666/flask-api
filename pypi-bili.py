from bilibili_api import search, sync

def a():
    print(sync(search.search("奥利给")))

a()
print("hello")