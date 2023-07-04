#Big shoutout to Anthon for providing the logic for translating the yaml parser when I was ready to just write my own. https://stackoverflow.com/questions/76552508/how-to-force-yaml-to-overlook-duplicate-keys/76553845#76553845

import ruamel.yaml
from ._internal import keys


class HTMLGenerator:
    def __init__(self, file_in):
        self.file_in = file_in
        self.closed_tag_array = keys.tag_lists().closed_tag_array

        class MyConstructor(ruamel.yaml.RoundTripConstructor):
            def construct_mapping(self, node, datatyp, deep=False):
                if not isinstance(node, ruamel.yaml.nodes.MappingNode):
                    raise ConstructorError(
                        None, None, f'expected a mapping node, but found {node.id!s}', node.start_mark,
                    )
                ret_val = datatyp
                for key_node, value_node in node.value:
                    # keys can be list -> deep
                    key = self.construct_object(key_node, deep=True)
                    assert isinstance(key, str)
                    value = self.construct_object(value_node, deep=deep)
                    ret_val.append((key, value))
                return ret_val

            def construct_yaml_map(self, node):
                data = []
                yield data
                self.construct_mapping(node, data, deep=True)

        self.MyConstructor = MyConstructor

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

    def generate_html(self):
        self.MyConstructor.add_constructor(
            'tag:yaml.org,2002:map', self.MyConstructor.construct_yaml_map
        )
        yaml = ruamel.yaml.YAML()
        yaml.Constructor = self.MyConstructor
        data = yaml.load(self.file_in)

        html_string = self.html(data)
        return html_string

