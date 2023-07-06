
from ._internal import keys


class HTMLGenerator:
    def __init__(self):
        self.closed_tag_array = keys.tag_lists().closed_tag_array

    def attr(self, data):
        ret_val = ''
        if not isinstance(data, list):
            return ret_val
        for key, value in data:
            if key == 'attributes':
                for k1, v1 in value:
                    ret_val += f' {k1}="{v1}"'
        return ret_val

    def content(self, data):
        ret_val = ''
        print(data[0])
        if data[0][0] == 'text':
            ret_val += f'{data[0][1]}'

        return ret_val

    def html(self, data, level=0, html_string=''):
        indent = '  ' * level
        if isinstance(data, list):
            for elem in data:
                if elem[0] == 'attributes':
                    continue

                if elem[1] is None or len(elem[1]) == 1 and elem[1][0] == 'attributes':
                    html_string += f'{indent}<{elem[0]}{self.attr(elem[1])}>\n'
                    continue

                if elem[0] == 'content':
                    #print(f'Content Found {elem[1][0]}')
                    html_string += f'{indent}{self.content(elem[1])}\n'
                    continue

                html_string += f'{indent}<{elem[0]}{self.attr(elem[1])}>\n'
                html_string = self.html(elem[1], level + 1, html_string)

                if elem[0] in self.closed_tag_array:
                    html_string += f'{indent}</{elem[0]}>\n'

        elif isinstance(data, str):
            html_string += f'{indent}{data}\n'

        else:
            print('type', type(data))
            # raise NotImplementedError

        return html_string

    def generate_html(self, html_construct):
        html_string = self.html(html_construct)
        return html_string

        