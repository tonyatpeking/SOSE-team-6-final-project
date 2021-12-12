import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json

from .BasicComponents import *
from .Editor import *


class MapComponent(BaseComponent):
    def __init__(self, editor):
        super().__init__(editor, 'MapComponent')

        # self is captured
        def builder(node):
            node.addInput(Rete.Input('geojson', 'geojson', geojson_socket))
            node.addControl(MapControl(
                self.editor, 'map'))

        def worker(node, inputs, outputs):
            geojson = self.get_input_value(inputs, 'geojson', '')
            self.set_control_value(node, 'map', geojson)

        self.set_builder(builder)
        self.set_worker(worker)


map_component = MapComponent(Editor.get_default_editor())


class MyIpComponent(BaseComponent):
    def __init__(self, editor):
        super().__init__(editor, 'MyIpComponent')

        # self is captured
        def builder(node):
            node.addOutput(Rete.Output('ip', 'ip', string_socket))
            node.addControl(InputControl(
                self.editor, 'ipControl', 'text', True))
            response = anvil.http.request('https://api64.ipify.org')
            self.ip = response.get_bytes().decode("utf-8")
            self.set_control_value(node, 'ipControl', self.ip)

        def worker(node, inputs, outputs):
            outputs['ip'] = self.ip
            self.set_control_value(node, 'ipControl', self.ip)

        self.set_builder(builder)
        self.set_worker(worker)


myIp_component = MyIpComponent(Editor.get_default_editor())


class IpToGeojsonComponent(BaseComponent):
    def __init__(self, editor):
        super().__init__(editor, 'IpToGeojsonComponent')

        # self is captured
        def builder(node):
            node.addInput(Rete.Input('ip', 'ip', string_socket))
            node.addOutput(Rete.Output('geojson', 'geojson', geojson_socket))
            node.addControl(TextAreaControl(
                self.editor, 'text', True))

        def worker(node, inputs, outputs):
            ip_str = self.get_input_value(inputs, 'ip', '')

            response = anvil.http.request(
                f'https://get.geojs.io/v1/ip/geo/{ip_str}.json', json=True)
            lat = float(response['latitude'])
            long = float(response['longitude'])
            coords = [long, lat]
            geojson = {
                "type": "Feature",
                "geometry": {
                        "type": "Point",
                        "coordinates": coords
                },
                "properties": {
                    "name": "Your Location"
                }
            }
            geojson = json.dumps(geojson, indent=4)
            outputs['geojson'] = geojson
            self.set_control_value(node, 'text', geojson)

        self.set_builder(builder)
        self.set_worker(worker)


ipToGeojson_component = IpToGeojsonComponent(Editor.get_default_editor())


class WeatherComponent(BaseComponent):
    def __init__(self, editor):
        super().__init__(editor, 'WeatherComponent')

        # self is captured
        def builder(node):
            node.addInput(Rete.Input('ip', 'ip', string_socket))
            node.addOutput(Rete.Output('json', 'json', json_socket))
            node.addControl(TextAreaControl(
                self.editor, 'text', True))

        def worker(node, inputs, outputs):
            ip_str = self.get_input_value(inputs, 'ip', '')

            response = anvil.http.request(
                url=f'https://api.weatherapi.com/v1/current.json?key=956954a9af3742daba3222048210612&q={ip_str}&aqi=no',
                json=True)

            s = json.dumps(response, indent=4)
            outputs['json'] = s
            self.set_control_value(node, 'text', s)

        self.set_builder(builder)
        self.set_worker(worker)


weather_component = WeatherComponent(Editor.get_default_editor())
