
var VueInputControl = {
    props: ['readonly', 'emitter', 'nodeStoreKey', 'getData', 'putData', 'type'],
    template: `<input :type="type" 
    :readonly="readonly" 
    v-model='inputData'
    @input="dataChanged($event)"
    @dblclick.stop="" 
    @pointerdown.stop="" 
    @pointermove.stop=""/>`,
    data() {
        return {
            inputData: 0,
        }
    },
    methods: {
        dataChanged(e) {
            if (this.nodeStoreKey)
                this.putData(this.nodeStoreKey, this.inputData);
            this.emitter.trigger('process');
        }
    },
    mounted() {
        this.inputData = this.getData(this.nodeStoreKey);
    }
}

var InputControl = class extends Rete.Control {
    constructor(emitter, key, inputType, readonly = false) {
        super(key);
        this.component = VueInputControl;
        this.props = { emitter, type: inputType, nodeStoreKey: key, readonly };
    }
    setValue(val) {
        this.vueContext.inputData = val;
    }
}


var VueMapControl = {
    props: ['readonly', 'emitter', 'nodeStoreKey', 'getData', 'putData', 'mapId'],
    template: '<div :id="mapId" @pointerdown.stop=""></div>',
    data() { return { value: 0, } },
    methods: {
        clearMap(map) {
            map.eachLayer(function (layer) {
                map.removeLayer(layer);
            });
        },
        makeMap() {
            container = document.getElementById(this.mapId)
            if (!container) {
                console.log('Map id not found');
                return null;
            }
            var map = L.map(this.mapId).setView([32.8266, -96.7888], 10);
            L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 25,
                id: 'mapbox/streets-v11',
                tileSize: 512,
                zoomOffset: -1,
                accessToken: 'pk.eyJ1IjoidG9ueWF0cGVraW5nIiwiYSI6ImNrd3NkYXh6YjE1NW4ydm1ucDY4cGU4bnAifQ.jUE-Mcub5atbsdk7IZk2UQ'
            }).addTo(map);
            return map
        },
        updateMap() {
            if (!this.map)
                this.map = this.makeMap();
            if (!this.map)
                return;
            if (this.mapLayer) {
                this.mapLayer.remove();
            }
            const jsonData = JSON.parse(this._inputData);

            this.mapLayer = L.geoJSON(jsonData).addTo(this.map);

        }
    },
    computed: {
        inputData: {
            get() {
                return this._inputData;
            },
            set(val) {
                const valChanged = this._inputData != val;
                this._inputData = val;
                if (this.nodeStoreKey)
                    this.putData(this.nodeStoreKey, this._inputData);
                if (valChanged) {
                    this.emitter.trigger('process');
                    this.updateMap();
                }
            }
        }
    },
    mounted() {
        this._inputData = this.getData(this.nodeStoreKey);
    }
}

var MapControl = class extends Rete.Control {
    constructor(emitter, key, readonly = false) {
        super(key);
        this.component = VueMapControl;
        const mapId = 'map-' + crypto.randomUUID();
        this.props = { emitter, nodeStoreKey: key, readonly, mapId };
    }
    setValue(val) {
        this.vueContext._inputData = val;
        this.vueContext.updateMap();
    }
    updateMap() {
        this.vueContext.updateMap();
    }
}




var VueTextAreaControl = {
    props: ['readonly', 'emitter', 'nodeStoreKey', 'getData', 'putData'],
    template: `<textarea 
    class="textarea-control"
    :readonly="readonly" 
    v-model='inputData'
    @input="dataChanged($event)"
    @dblclick.stop="" 
    @pointerdown.stop="" 
    @pointermove.stop=""/>`,
    data() {
        return {
            inputData: 0,
        }
    },
    methods: {
        dataChanged(e) {
            if (this.nodeStoreKey)
                this.putData(this.nodeStoreKey, this.inputData);
            this.emitter.trigger('process');
        }
    },
    mounted() {
        this.inputData = this.getData(this.nodeStoreKey);
    }
}

var TextAreaControl = class extends Rete.Control {
    constructor(emitter, key, readonly = false) {
        super(key);
        this.component = VueTextAreaControl;
        this.props = { emitter, nodeStoreKey: key, readonly };
    }
    setValue(val) {
        this.vueContext.inputData = val;
    }
}