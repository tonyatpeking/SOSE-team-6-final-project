import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Editor import *

from anvil.js.window import (
    Rete,
    ConnectionPlugin,
    document,
    VueRenderPlugin,
    AreaPlugin,
    ContextMenuPlugin,
    CommentPlugin,
    HistoryPlugin,
    ConnectionMasteryPlugin,
    InputControl,
    MapControl,
    TextAreaControl)

# socket types
number_socket = Rete.Socket('number-socket')
json_socket = Rete.Socket('json-socket')
geojson_socket = Rete.Socket('geojson-socket')
string_socket = Rete.Socket('string-socket')
bool_socket = Rete.Socket('bool-socket')
image_socket = Rete.Socket('image-socket')
audio_socket = Rete.Socket('number-socket')
video_socket = Rete.Socket('video-socket')
file_socket = Rete.Socket('file-socket')
trigger_socket = Rete.Socket('trigger-socket')
any_socket = Rete.Socket('any-socket')

all_sockets = [number_socket,
               json_socket,
               geojson_socket,
               string_socket,
               bool_socket,
               image_socket,
               audio_socket,
               video_socket,
               file_socket,
               trigger_socket,
               any_socket]

for socket in all_sockets:
    socket.combineWith(any_socket)

# socket combining
# A -> B one directional
# instead have explicit conversion nodes
# geojson_socket.combineWith(json_socket)


# control types
# see rete-controls.js

class BaseComponent():
    def __init__(self, editor, component_name):
        self._proxy = Rete.Component(component_name)
        self.editor = editor
        editor.register(self)

    def set_builder(self, builder):
        self._proxy.builder = builder

    def set_worker(self, worker):
        self._proxy.worker = worker

    def create_node(self, pos=[0, 0]):
        node_proxy = self._proxy.createNode()
        node_proxy.position = pos
        self.editor.add_node(node_proxy)
        return node_proxy

    def set_control_value(self, node_proxy, control_name, val):
        for n in self.editor._editor_proxy.nodes:
            if n.id == node_proxy.id:
                n.controls.get(control_name).setValue(val)

    def get_data_value(self, node_proxy, control_name, default_val):
        val = default_val
        if control_name in node_proxy.data.keys():
            val = node_proxy.data[control_name]
        return val

    def get_input_value(self, inputs, input_name, default_value):
        val = default_value
        if(len(inputs[input_name]) == 1):
            val = inputs[input_name][0]
        if(len(inputs[input_name]) > 1):
            val = inputs[input_name]
        return val


# components
class NumberComponent(BaseComponent):
    def __init__(self, editor):
        super().__init__(editor, 'NumberComponent')

        # self is captured
        def builder(node):
            node.addOutput(Rete.Output('num', 'number', number_socket))
            node.addControl(InputControl(
                self.editor._editor_proxy, 'num', 'number'))

        def worker(node, inputs, outputs):
            num = self.get_data_value(node, 'num', 0)
            outputs['num'] = num

        self.set_builder(builder)
        self.set_worker(worker)


number_component = NumberComponent(Editor.get_default_editor())

class AddComponent(BaseComponent):
    def __init__(self, editor):
        super().__init__(editor, 'AddComponent')

        # self is captured
        def builder(node):
            node.addInput(Rete.Input('numA', 'number', number_socket))
            node.addInput(Rete.Input('numB', 'number', number_socket))
            node.addOutput(Rete.Output('num', 'number', number_socket))
            node.addControl(InputControl(
                self.editor, 'numC', 'number', True))

        def worker(node, inputs, outputs):
            numA = self.get_input_value(inputs, 'numA', 0)
            numB = self.get_input_value(inputs, 'numB', 0)
            sum = float(numA) + float(numB)
            outputs['num'] = sum
            self.set_control_value(node, 'numC', sum)

        self.set_builder(builder)
        self.set_worker(worker)


add_component = AddComponent(Editor.get_default_editor())


class ToStringComponent(BaseComponent):
    def __init__(self, editor):
        super().__init__(editor, 'ToStringComponent')

        # self is captured
        def builder(node):
            node.addInput(Rete.Input('any', 'any', any_socket))
            node.addOutput(Rete.Output('string', 'string', string_socket))
            node.addControl(InputControl(
                self.editor, 'text', ''))

        def worker(node, inputs, outputs):
            text = self.get_data_value(node, 'text', '')
            input_val = self.get_input_value(inputs, 'any', '')
            if input_val:
                text = input_val
            
            text = str(text)
            outputs['string'] = text
            self.set_control_value(node, 'text', text)

        self.set_builder(builder)
        self.set_worker(worker)


tostring_component = ToStringComponent(Editor.get_default_editor())


class TextAreaComponent(BaseComponent):
    def __init__(self, editor):
        super().__init__(editor, 'TextAreaComponent')

        # self is captured
        def builder(node):
            node.addInput(Rete.Input('any', 'any', any_socket))
            node.addOutput(Rete.Output('string', 'string', string_socket))
            node.addControl(TextAreaControl(
                self.editor, 'text'))

        def worker(node, inputs, outputs):
            text = self.get_data_value(node, 'text', '')
            input_val = self.get_input_value(inputs, 'any', '')
            if input_val:
                text = input_val
            
            text = str(text)
            outputs['string'] = text
            self.set_control_value(node, 'text', text)

        self.set_builder(builder)
        self.set_worker(worker)


textarea_component = TextAreaComponent(Editor.get_default_editor())