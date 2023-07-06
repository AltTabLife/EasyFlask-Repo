#Create class for each page with jinja extensions/inclusions in tow

class PageBuilder:
    def __init__(self):
        pass
    class Page:
        def __init__(self):
            self.page_name = ''
            self.route_list = []
            self.jinja_construct = False #Denotes if a jinja construct is present for further processing
            self.html_construct = [] #Raw html constructor to be added/modified with jinja in the next extension

    def build_pages(self, page_construct):
        #parse out page context, if there is none, return untouched

        first_page = self.Page()
        if page_construct[0][0] != 'page':
            return page_construct 
        else:
            for a in page_construct[0][1]:
                if a[0] == 'page_name':
                    first_page.page_name = a[1]
                if a[0] == 'route_list':
                    first_page.route_list = a[1]
                if a[0] == 'html':
                    first_page.html_construct = [a]
        return first_page            
                
                
        
