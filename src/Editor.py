import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
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
    ConnectionMasteryPlugin)


class Editor():
    _default_editor = None

    # stores the python classes
    def __init__(self, name):
        self.components_to_register = []
        self._editor_proxy = None
        self._engine_proxy = None
        self.name = name

    def attach_to_dom(self, js_div):
        editor_proxy = Rete.NodeEditor(self.name, js_div)
        editor_proxy.use(ConnectionPlugin.default)
        editor_proxy.use(VueRenderPlugin.default)
        editor_proxy.use(AreaPlugin, {
            'background': False,
            'snap': False,
            'scaleExtent': {'min': 0.1, 'max': 1},
            'translateExtent': {'width': 5000, 'height': 5000}
        })
        editor_proxy.use(ContextMenuPlugin.default)
        editor_proxy.use(CommentPlugin.default)
        editor_proxy.use(HistoryPlugin)
        editor_proxy.use(ConnectionMasteryPlugin.default)

        self._editor_proxy = editor_proxy
        self._engine_proxy = Rete.Engine(self.name)

        def process(args):
            self._engine_proxy.abort()
            self._engine_proxy.process(self._editor_proxy.toJSON())
        self._editor_proxy.on(
            'process nodecreated noderemoved connectioncreated connectionremoved', process)

        self._process_registers()

    # adds to register queue
    def register(self, component):
        self.components_to_register.append(component)

    def _process_registers(self):
        for component in self.components_to_register:
            self._engine_proxy.register(component._proxy)
            self._editor_proxy.register(component._proxy)

    def add_node(self, node):
        self._editor_proxy.addNode(node)

    def trigger_process(self):
        self._editor_proxy.trigger('process')

    def zoom(self, node_proxies):
        self._editor_proxy.view.resize()
        AreaPlugin.zoomAt(self._editor_proxy, node_proxies)

    def connect_nodes(self, nodeA, outA, nodeB, inB):
        self._editor_proxy.connect(
            nodeA.outputs.get(outA), nodeB.inputs.get(inB))

    @classmethod
    def get_default_editor(cls):
        return cls._default_editor

    @classmethod
    def set_default_editor(cls, editor):
        cls._default_editor = editor

    @classmethod
    def attach_default_editor(cls, anvil_panel):
        dom_element = anvil.js.get_dom_node(anvil_panel)
        div = document.createElement("div")
        dom_element.firstChild.prepend(div)
        editor = cls.get_default_editor()
        editor.attach_to_dom(div)


# make a default editor so that components can queue registers
Editor.set_default_editor(Editor('default@0.1.0'))
