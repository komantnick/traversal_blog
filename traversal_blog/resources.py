import datetime
from random import randint
# Done outside bootstrap to persist from request to request

class User(dict):
    def __init__(self,name,passwd,parent,title):
        self.__name__= name
        self.name_rest = name
        self.password = passwd
        self.__parent__ = parent
        self.title = title


class Root(User):
    pass

root = Root('', None,None, 'My Site')

class Item(dict):
    def __init__(self, name, parent, title,text,datetime):
        self.__name__ = name
        self.name_rest = name
        self.__parent__ = parent
        self.title = title
        self.text=text
        self.datetime=datetime


    def delete(self,name_rest,rootz=root):
        for child in rootz.values():
            if (child.name_rest==name_rest):
                del(rootz[name_rest])
                rz=root
                return rz
            else:
                self.delete(name_rest, child)


class Community(dict):
    def __init__(self, name, title):
        self.__name__ = name
        self.name_rest=name
        #self.__parent__ = parent
        self.title = title

class Communities(dict):
    def __init__(self, name, parent,title):
        self.__name__ = name
        self.name_rest = name
        self.__parent__ = parent
        self.title = title







def bootstrap(request):
    if not root.values():
        user1=User('komantnick','komantnick',root,'Nikita Sayapin')
        root['komantnick']=user1
        user2 = User('komantnick2','komantnick2', root, 'Pavel Petrov')
        root['komantnick2'] = user2
        item1=Item('item1',user1,'doc1','Ne doc',datetime.datetime.now())
        user1['item1']=item1
        group1=Communities("group",user1,"Groups of user")
        user1['group'] = group1
        group2 = Communities("group", user2, "Groups of user")
        user2['group'] = group2
        comm=Community("comm","Grz-group")
        #user1['comm'] = comm
        item2 = Item('item2', comm, 'doc1', 'Ne doc', datetime.datetime.now())
        item5 = Item('item5', comm, '7', 'Ne docz', datetime.datetime.now())
        comm['item2'] = item2
        group1['comm']=comm
        group2['comm'] = comm
        comm['item5']=item5

    return root

def finduser(value,passwd):
    for child in root.values():
        if (child.name_rest==value and child.password==passwd):
            return True
    return False


# def addgroup(classname,value):
#     for child in root.values():
#         if (child.name_rest==value):
#             print(child)
#             print(classname)
#             child[child.name_rest][context.name_rest]=context
#             return True
#     return False

def sendchild(name):
    for child in root.values():
        if (child["group"][name].name_rest==name):
            return child["group"][name]


        # if (child[''.name_rest==name_rest):
        #     return child
        # else:
        #     sendchild(name_rest, child)


def addgroup(name,user):
    print(name)
    obj=sendchild(name)
    print("X",obj.name_rest)
    for child in root.values():
        if (child.name_rest==user):
            child["group"][name]=obj




def adduser(value,passwd,title):
    valuez=User(value,passwd,root,title)
    root[value]=valuez
    titlegroup="group"
    valuez[titlegroup]= Communities(titlegroup, valuez, "Groups of user")
