from ._anvil_designer import MainpageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil
import anvil.js
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
    MapControl)

from ..BasicComponents import *
from ..ApiComponents import *
from ..Editor import *

editor = None


def print_js_attributes(js_object):
    for key in js_object.keys():
        print(key)


# class NumComponent():
#     def __init__(self):
#         self._proxy = Rete.Component('MapNode')
#         self._proxy.builder = cls.builder
#         self._proxy.worker = NumComponent.worker

#     @staticmethod
#     def builder(node):
#         out = Rete.Output('num', 'Number', number_socket)
#         out1 = Rete.Output('num1', 'Json', json_socket)
#         global editor
#         control1 = InputControl(editor, 'num', 'number')
#         node.addOutput(out)
#         node.addOutput(out1)
        # node.addControl(control1)

        # # wow, all of the following work
        # node.addControl(InputControl(editor, 'button', 'button'))
        # node.addControl(InputControl(editor, 'checkbox', 'checkbox'))
        # node.addControl(InputControl(editor, 'color', 'color'))
        # node.addControl(InputControl(editor, 'date', 'date'))
        # node.addControl(InputControl(
        #     editor, 'datetime-local', 'datetime-local'))
        # node.addControl(InputControl(editor, 'email', 'email'))
        # node.addControl(InputControl(editor, 'file', 'file'))
        # node.addControl(InputControl(editor, 'hidden', 'hidden'))
        # node.addControl(InputControl(editor, 'image', 'image'))
        # node.addControl(InputControl(editor, 'month', 'month'))
        # node.addControl(InputControl(editor, 'number', 'number'))
        # node.addControl(InputControl(editor, 'password', 'password'))
        # node.addControl(InputControl(editor, 'radio', 'radio'))
        # node.addControl(InputControl(editor, 'range', 'range'))
        # node.addControl(InputControl(editor, 'reset', 'reset'))
        # node.addControl(InputControl(editor, 'search', 'search'))
        # node.addControl(InputControl(editor, 'submit', 'submit'))
        # node.addControl(InputControl(editor, 'tel', 'tel'))
        # node.addControl(InputControl(editor, 'text', 'text'))
        # node.addControl(InputControl(editor, 'time', 'time'))
        # node.addControl(InputControl(editor, 'url', 'url'))
        #node.addControl(MapControl(editor, 'map'))

    # @staticmethod
    # def worker(node, inputs, outputs):
    #     print('work start')
    #     #outputs['num'] = node.data.num
    #     global editor
    #     print(editor.toJSON())
    #     for n in editor.nodes:
    #         if n.id == node.id:
    #             n.controls.get('map').updateMap()
    #     # editor.nodes.find(lambda n: n.id == node.id).controls.get(
    #     #     'map').updateMap()
    #     print('work done')


class Mainpage(MainpageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        global editor
        editor.view.resize()
        pass

    def timer_1_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        # editor.view.resize()

    def form_show(self, **event_args):
        """This method is called when the HTML panel is shown on the screen"""
        editor = Editor.get_default_editor()
        editor.attach_default_editor(self.rete_xy_panel)

        num_node = number_component.create_node([1200, 10])
        add_node = add_component.create_node([1900, 10])
        editor.connect_nodes(num_node, 'num', add_node, 'numA')

        tostring_node = tostring_component.create_node([0, -300])
        ip_node = myIp_component.create_node([-1500, 0])
        geojson_node = ipToGeojson_component.create_node([-1000, 0])
        editor.connect_nodes(ip_node, 'ip', geojson_node, 'ip')
        map_node = map_component.create_node([-200, 0])
        editor.connect_nodes(geojson_node, 'geojson', map_node, 'geojson')

        weather_node = weather_component.create_node([-1000, 600])
        editor.connect_nodes(ip_node, 'ip', weather_node, 'ip')

        editor.zoom([add_node,ip_node,weather_node])
        editor.trigger_process()

        # #elt = document.getElementById('rete')
        # elt = js.get_dom_node(self.rete_xy_panel)
        # div = document.createElement("div")
        # elt.firstChild.prepend(div)
        # global editor
        # editor = Rete.NodeEditor('demo@0.1.0', div)
        # editor.use(ConnectionPlugin.default)
        # editor.use(VueRenderPlugin.default)
        # editor.use(AreaPlugin, {
        #     'background': False,
        #     'snap': False,
        #     'scaleExtent': {'min': 0.1, 'max': 1},
        #     'translateExtent': {'width': 5000, 'height': 5000}
        # })
        # editor.use(ContextMenuPlugin.default)
        # editor.use(CommentPlugin.default)
        # editor.use(HistoryPlugin)
        # editor.use(ConnectionMasteryPlugin.default)

        # numComponent = NumComponent()
        # testComp = Rete.Component('test')
        # editor.register(numComponent._proxy)
        # editor.register(testComp)

        # engine = Rete.Engine('demo@0.1.0')
        # engine.register(numComponent._proxy)
        # engine.register(testComp)

        # testComp1 = numComponent._proxy.createNode()

        # testComp1.position = [0, 0]
        # editor.addNode(testComp1)
        # editor.view.resize()
        # AreaPlugin.zoomAt(editor, [testComp1])

        # # make_map()

        # def process(args):
        #     print('process start')
        #     engine.abort()
        #     engine.process(editor.toJSON())
        #     print('process')
        #     print(args)
        # editor.on(
        #     'process nodecreated noderemoved connectioncreated connectionremoved', process)

        # editor.trigger('process')
