from random import randint

from pyramid.httpexceptions import HTTPFound
from pyramid.location import lineage
from pyramid.view import view_config

from .resources import (
    Root,
    Item,
    User,
    Communities,
    Community,
    finduser,
    addgroup,
    adduser
    )
from pyramid.security import (
    remember,
    forget,
    authenticated_userid
    )
import datetime

class TutorialViews(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.parents = reversed(list(lineage(context)))
        self.logged_in = authenticated_userid(request)

    @view_config(renderer='templates/root.jinja2',
                 context=Root)
    def root(self):
        page_title = 'Blog'
        return dict(page_title=page_title)

    @view_config(renderer='templates/user.jinja2',
                 context=User)
    def user(self):
        page_title = 'List of items'
        return dict(page_title=page_title)

    @view_config(renderer='templates/group.jinja2',
                 context=Communities)
    def group(self):
        page_title = 'List of communities'
        return dict(page_title=page_title)

    @view_config(name='add_group',
                 context=Communities)
    def add_group(self):
        name = str(randint(0, 999999))
        title = self.request.POST['group_title']
        new_comm = Community(name, title)
        self.context[name]=new_comm
        url = self.request.resource_url(new_comm)
        return HTTPFound(location=self.request.referrer)

    @view_config(name='add_user_group',
                 context=Community)
    def add_user_group(self):
        user = self.request.POST['group_username']
        addgroup(self.context.name_rest,user)
        return HTTPFound(location='http://localhost:6543')



    #@view_config(name='add_item', context=User)
    @view_config(name='add_item', context=Community)
    @view_config(name='add_item', context=User)
    def add_item(self):
        if (self.context.__class__.__name__ == "Communities" or (self.context.__class__.__name__ == "User"
                                                                 and self.context.name_rest==self.logged_in)):
            title = self.request.POST['document_title']
            text = self.request.POST['document_text']
            now = datetime.datetime.now()
            name = str(randint(0, 999999))
            new_document = Item(name, self.context, title, text, now)
            self.context[name] = new_document
            print(name)
            # request.url}} / {{child.name_rest}

            # Redirect to the new document
            url = self.request.resource_url(new_document)
            return HTTPFound(location=self.request.referrer)
        else:
            return HTTPFound(location='http://localhost:6543')
        # Make a new Document


    @view_config(renderer='templates/updateform.jinja2',name='update', context=Item)
    def update(self):
        page_title = 'Update Item'
        return dict(page_title=page_title)

    @view_config(name='update_item', context=Item)
    def update_item(self):
        print(self.context.text)
        self.context.title = self.request.POST['document_title']
        self.context.text = self.request.POST['document_text']
        print(self.context.text)
        print(self.context)
        return HTTPFound(location='http://localhost:6543')

    @view_config(name='delete', context=Item)
    def delete(self):
        self.context.delete(self.context.name_rest)
        return HTTPFound(location='http://localhost:6543')

    @view_config(name='login', renderer='templates/login.jinja2')
    def login(self):
        request = self.request
        referrer = request.url
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            if (finduser(login,password) == True):
                headers = remember(request, login)
                return HTTPFound(location='/',
                                 headers=headers)
            message = 'Failed login'

        return dict(
            page_title='Login',
            message=message,
            url=request.application_url + '/login',
            login=login,
            password=password,
        )

    @view_config(name='signup', renderer='templates/signup.jinja2')
    def signup(self):
        request = self.request
        referrer = request.url
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            title = request.params['title']
            if finduser(login, password) == True:
                headers = remember(request, login)
                return HTTPFound(location='/',
                                 headers=headers)
            else:
                adduser(login,password,title)
                headers = remember(request, login)
                return HTTPFound(location='/',
                                 headers=headers)
            message = 'Failed login'

        return dict(
            page_title='Signup',
            message=message,
            url=request.application_url + '/signup',
            login=login,
            password=password,
        )

    @view_config(name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.resource_url(request.root)
        return HTTPFound(location=url,
                         headers=headers)






    @view_config(renderer='templates/document.jinja2',
                 context=Item)
    def document(self):
        page_title = 'Item'
        return dict(page_title=page_title)

    @view_config(renderer='templates/group-one.jinja2',
                 context=Community)
    def groupone(self):
        page_title = 'List of items of community'
        return dict(page_title=page_title)