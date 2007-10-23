from hwtest.report import Report


class DataReport(Report):

    def register_dumps(self):
        for (dt, dh) in [(bool, self.dumps_bool),
                         (int, self.dumps_int),
                         (long, self.dumps_int),
                         (float, self.dumps_float),
                         (str, self.dumps_str),
                         (unicode, self.dumps_unicode),
                         (list, self.dumps_list),
                         (tuple, self.dumps_list),
                         (dict, self.dumps_dict),
                         (type(None), self.dumps_none)]:
            self._manager.handle_dumps(dt, dh)

    def register_loads(self):
        for (lt, lh) in [("bool", self.loads_bool),
                         ("int", self.loads_int),
                         ("long", self.loads_int),
                         ("float", self.loads_float),
                         ("str", self.loads_str),
                         ("unicode", self.loads_str),
                         ("property", self.loads_property),
                         ("properties", self.loads_properties),
                         (type(None), self.loads_none)]:
            self._manager.handle_loads(lt, lh)

    def _dumps_text(self, obj, parent, type):
        parent.setAttribute("type", type)
        text_node = self._create_text_node(obj, parent)

    def dumps_bool(self, obj, parent):
        self._dumps_text(str(obj), parent, "bool")

    def dumps_int(self, obj, parent):
        self._dumps_text(str(obj), parent, "int")

    def dumps_float(self, obj, parent):
        self._dumps_text(str(obj), parent, "float")

    def dumps_str(self, obj, parent):
        self._dumps_text(obj, parent, "str")

    def dumps_unicode(self, obj, parent):
        self._dumps_text(obj, parent, "unicode")

    def dumps_list(self, obj, parent):
        parent.setAttribute("type", "list")
        for val in obj:
            # HACK: lists are supposedly expressed as properties
            property = self._create_element("property", parent)
            self._manager.call_dumps(val, property)
        
    def dumps_dict(self, obj, parent):
        for key in sorted(obj.keys()):
            val = obj[key]
            if self._manager.dumps_table.has_key(key):
                # Custom dumps handler
                element = self._create_element(key, parent)
                self._manager.dumps_table[key](val, element)
            elif type(val) == dict:
                # <key type="">val</key>
                element = self._create_element(key, parent)
                self._manager.call_dumps(val, element)
            else:
                # <property name="key" type="">val</property>
                property = self._create_element("property", parent)
                property.setAttribute("name", key)
                self._manager.call_dumps(val, property)

    def dumps_none(self, obj, parent):
        self._create_element("none", parent)

    def loads_bool(self, node):
        return bool(node.data)

    def loads_int(self, node):
        return int(node.data)

    def loads_float(self, node):
        return float(node.data)

    def loads_str(self, node):
        return str(node.data.strip())

    def loads_property(self, node):
        type = node.getAttribute("type")
        if type == "list":
            # HACK: see above in dumps_list
            ret = []
            for property in node.getElementsByTagName("property"):
                value = self._manager.call_loads(property)
                ret.append(value)
        else:
            child = node.firstChild
            ret = self._manager.loads_table[type](child)
        return ret

    def loads_properties(self, node):
        properties = {}
        for property in node.getElementsByTagName("property"):
            key = property.getAttribute("name")
            value = self._manager.call_loads(property)
            properties[key] = value

        return properties

    def loads_none(self, node):
        return None
