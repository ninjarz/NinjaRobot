from NinjaTools.NinjaNLP import *


tmp = NinjaNLP()
while True:
    print(tmp.parse('《三体》三部曲，又名“地球往事“三部曲，作者刘慈欣。该系列小说由《三体》、《黑暗森林》、《死神永生》三部小说组成, 于2006年至2010年由《科幻世界》杂志连载，出版。'))
    text = input()
    print(tmp.parse(text))
    

