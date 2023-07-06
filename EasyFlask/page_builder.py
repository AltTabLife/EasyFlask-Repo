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
            self.final_html_string = ''

    def build_pages(self, page_construct):
        #parse out page context, if there is none, return untouched
        pages = []

        if page_construct[0][0] != 'page':
            return page_construct 
        else:
            for i in page_construct:
                
                page = self.Page()
                for a in i[1]:
                    if a[0] == 'page_name':
                        page.page_name = a[1]
                    if a[0] == 'route_list':
                        page.route_list = a[1]
                    if a[0] == 'html':
                        page.html_construct = [a]
                pages.append(page)
                
        return pages            
                
                
        
