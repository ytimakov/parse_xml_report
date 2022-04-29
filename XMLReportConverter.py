from xml.etree import ElementTree


def _get_text(t):
    if t:
        return t.strip()
    else:
        return ""


def _is_elem_multiple(element):
    if len(element) > 1:
        if element[0].tag == element[1].tag:
            return True
    return False


def _do_nothing(a):
    return


class XMLToPlainTabConverter:

    def __init__(self, parent):
        self._attributes = {}
        self._parent = parent
        self._row_number = 0

    @property
    def get_row_headers(self):
        if self._attributes == {}:
            self.enumerate_rows(_do_nothing, 1)
        return self._attributes.keys()

    @property
    def get_sample_data(self):
        if self._attributes == {}:
            self.enumerate_rows(_do_nothing, 1)
        return self._attributes

    def enumerate_rows(self, row_function=print, count=None):
        self._attributes = {}
        self._row_number = 0

        def _row_function():
            self._row_number += 1
            row_function(self._attributes)

        def add_elem(parent_path, element, show=False):
            path = parent_path + "/" + element.tag

            for key in self._attributes.keys():
                if key.find(path) == 0:
                    self._attributes[key] = ""

            text = _get_text(element.text)
            multiple_element = None
            if text:
                self._attributes[path] = text
            if element.attrib:
                for key, value in element.attrib.items():
                    self._attributes[path + "@" + key] = value
            for e in element:
                if _is_elem_multiple(e):
                    multiple_element = e
                else:
                    add_elem(path, e, False)
            if multiple_element:
                for e in multiple_element:
                    add_elem(path + "/" + multiple_element.tag, e, True)
            else:
                if count:
                    if self._row_number >= count:
                        return
                else:
                    if show:
                        _row_function()

        add_elem("", self._parent)
        if self._row_number == 0:
            _row_function()

    def to_text(self, file_name):
        file = open(file_name, "w")

        def row_function(values):
            if self._row_number == 1:
                str = "\t".join([(k.split("/"))[-1] for k in values.keys()]) + "\n"
                file.write(str)
            str = "\t".join(values.values()) + "\n"
            file.write(str)

        self.enumerate_rows(row_function)

        file.close()


def xml_to_text(from_xml_file_name, to_file_name):
    tree = ElementTree.parse(from_xml_file_name)
    root = tree.getroot()
    converter = XMLToPlainTabConverter(root)
    converter.to_text(to_file_name)



