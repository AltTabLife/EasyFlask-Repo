#Big shoutout to Anthon for providing the logic for translating the yaml parser when I was ready to just write my own. https://stackoverflow.com/questions/76552508/how-to-force-yaml-to-overlook-duplicate-keys/76553845#76553845

import ruamel.yaml

def parse_yamlish(file_in):
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

    MyConstructor.add_constructor(
        'tag:yaml.org,2002:map', MyConstructor.construct_yaml_map
    )

    yaml = ruamel.yaml.YAML()
    yaml.Constructor = MyConstructor
    data = yaml.load(file_in)
    return data