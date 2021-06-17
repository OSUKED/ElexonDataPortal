L.Control.SliderControl = L.Control.extend({
    options: {
        position: 'topright',
        layer: null,
        timeAttribute: 'time',
        isEpoch: false,     // whether the time attribute is seconds elapsed from epoch
        startTimeIdx: 0,    // where to start looking for a timestring
        timeStrLength: 19,  // the size of  yyyy-mm-dd hh:mm:ss - if millis are present this will be larger
        maxValue: -1,
        minValue: 0,
        showAllOnStart: false,
        markers: null,
        range: false,
        follow: 0,
        sameDate: false,
        alwaysShowDate : false,
        rezoom: null,
        orderMarkers: true,
        orderDesc: false,
        popupOptions: {},
        popupContent: '',
        showAllPopups: true,
        showPopups: true,
    },

    initialize: function (options) {
        L.Util.setOptions(this, options);
        this._layer = this.options.layer;
        L.extend(this, L.Mixin.Events);
    },

    onAdd: function (map) {
        this.options.map = map;
        // Create a control sliderContainer with a jquery ui slider
        this.container = L.DomUtil.create('div', '', this._container);
        this.sliderBoxContainer = L.DomUtil.create('div', 'slider', this.container);
        var sliderContainer = L.DomUtil.create('div', '', this.sliderBoxContainer);
        sliderContainer.id = "leaflet-slider";
        sliderContainer.style.width = "200px";

        L.DomUtil.create('div', 'ui-slider-handle', sliderContainer);
        this.timestampContainer = L.DomUtil.create('div', 'slider', this.container);
        this.timestampContainer.id = "slider-timestamp";
        this.timestampContainer.style.cssText = "width:200px; margin-top:3px; background-color:#FFFFFF; text-align:center; border-radius:5px;display:none;";


        //Prevent map panning/zooming while using the slider
        L.DomEvent.disableClickPropagation(this.sliderBoxContainer);
        this._map.on('mouseup',this.clearTimestamp,this);


        var options = this.options;
        this.options.markers = [];

        function compare( a, b ) {
            var valA = null;
            var valB = null;

            if(a.features && a.features.properties && a.feature.properties[options.timeAttribute]){
                valA = a.feature.properties[options.timeAttribute];
            }else if(a.options[options.timeAttribute]){
                valA = a.options[options.timeAttribute];
            }
            if(b.features && b.features.properties && b.feature.properties[options.timeAttribute]){
                valB = b.feature.properties[options.timeAttribute];
            }else if(b.options[options.timeAttribute]){
                valB = b.options[options.timeAttribute];
            }
            if(valA && valB) {
                if (valA < valB) {
                    return -1;
                }
                if (valA > valB) {
                    return 1;
                }
            }
            return 0;
        }

        //If a layer has been provided: calculate the min and max values for the slider
        if (this._layer) {
            var index_temp = 0;
            var templayers = [];
            this._layer.eachLayer(function (layer) {
                templayers.push(layer);
            });

            if(options.orderMarkers){
                templayers = templayers.sort(compare);

                if(options.orderDesc){
                    templayers = templayers.reverse();
                }
            }

            var that = this;
            templayers.forEach(function (layer){


                if(layer instanceof L.LayerGroup) {
                    layer.getLayers().forEach(function (l) {
                        l = that._setPopupProperty(l);
                    });
                }else{
                    layer = that._setPopupProperty(layer);
                }
                options.markers[index_temp] = layer;

                ++index_temp;
            });

            options.maxValue = index_temp - 1;
            this.options = options;
        } else {
            console.log("Error: You have to specify a layer via new SliderControl({layer: your_layer});");
        }
        return this.container;
    },

    onRemove: function (map) {
        //Delete all markers which where added via the slider and remove the slider div
        for (i = this.options.minValue; i <= this.options.maxValue; i++) {
            map.removeLayer(this.options.markers[i]);
        }
        this.container.remove();

        map.off('mouseup',this.clearTimestamp,this);

    },

    startSlider: function (sliderStartPos=null) {
        var _options = this.options;
        var _extractTimestamp = this.extractTimestamp;
        var index_start = _options.minValue;
        if(_options.showAllOnStart){
            index_start = _options.maxValue;
            if(_options.range) _options.values = [_options.minValue,_options.maxValue];
            else _options.value = _options.maxValue;
        }
        var timestampContainer = this.timestampContainer;
        var that = this;
        if (sliderStartPos) _options.value = sliderStartPos;
        
        $(this.sliderBoxContainer).slider({
            range: _options.range,
            value: _options.value,
            values: _options.values,
            min: _options.minValue,
            max: _options.maxValue,
            sameDate: _options.sameDate,
            step: 1,
            slide: function (e, ui) {
                var map = _options.map;
                var fg = L.featureGroup();
                if(!!_options.markers[ui.value]) {
                    // If there is no time property, this line has to be removed (or exchanged with a different property)
                    if(_options.markers[ui.value].feature !== undefined) {
                        if(_options.markers[ui.value].feature.properties[_options.timeAttribute]){
                            if(_options.markers[ui.value]){
                                timestampContainer.style.display = "block";
                                $(timestampContainer).html(_extractTimestamp(_options.markers[ui.value].feature.properties[_options.timeAttribute], _options));
                            }
                        }else {
                            console.error("Time property "+ _options.timeAttribute +" not found in data");
                        }
                    }else {
                        // set by leaflet Vector Layers
                        if(_options.markers [ui.value].options[_options.timeAttribute]){
                            if(_options.markers[ui.value]){
                                timestampContainer.style.display = "block";
                                $(timestampContainer).html( _extractTimestamp(_options.markers[ui.value].options[_options.timeAttribute], _options));
                            }
                        }else {
                            console.error("Time property "+ _options.timeAttribute +" not found in data");
                        }
                    }
                    var markers = [];
                    var i;
                    // clear markers
                    for (i = _options.minValue; i <= _options.maxValue; i++) {
                        if(_options.markers[i]) map.removeLayer(_options.markers[i]);
                    }
                    if(_options.range){
                        // jquery ui using range
                        for (i = ui.values[0]; i <= ui.values[1]; i++){
                           if(_options.markers[i]) {
                               markers.push(_options.markers[i]);
                               map.addLayer(_options.markers[i]);
                               fg.addLayer(_options.markers[i]);
                           }
                        }
                    }else if(_options.follow > 0){
                        for (i = ui.value - _options.follow + 1; i <= ui.value ; i++) {
                            markers.push(_options.markers[i]);
                            map.addLayer(_options.markers[i]);
                            fg.addLayer(_options.markers[i]);
                        }
                    }else if(_options.sameDate){
                        var currentTime;
                        if (_options.markers[ui.value].feature !== undefined) {
                            currentTime = _options.markers[ui.value].feature.properties.time;
                        } else {
                            currentTime = _options.markers[ui.value].options.time;
                        }
                        for (i = _options.minValue; i <= _options.maxValue; i++) {
                            if(_options.markers[i].options.time == currentTime){
                                markers.push(_options.markers[i]);
                                map.addLayer(_options.markers[i]);
                            }
                        }
                    }else{
                        for (i = _options.minValue; i <= ui.value ; i++) {
                            if(_options.markers[i]) {
                                markers.push(_options.markers[i]);
                                map.addLayer(_options.markers[i]);
                                fg.addLayer(_options.markers[i]);
                            }
                        }
                    }

                    if(_options.showPopups) {
                        that._openPopups(markers);
                    }
                    that.fire('rangechanged',{
                        markers: markers,
                    });
                }
                if(_options.rezoom) {
                    map.fitBounds(fg.getBounds(), {
                        maxZoom: _options.rezoom
                    });
                }
            }
        });
        if (_options.alwaysShowDate) {
            timestampContainer.style.display = "block";

            if(_options.markers[index_start].feature !== undefined) {
                if(_options.markers[index_start].feature.properties[_options.timeAttribute]){
                    if(_options.markers[index_start]){
                        timestampContainer.style.display = "block";
                        $(timestampContainer).html(_extractTimestamp(_options.markers[index_start].feature.properties[_options.timeAttribute], _options));
                    }
                }else {
                    console.error("Time property "+ _options.timeAttribute +" not found in data");
                }
            }else {
                // set by leaflet Vector Layers
                if(_options.markers [index_start].options[_options.timeAttribute]){
                    if(_options.markers[index_start]){
                        timestampContainer.style.display = "block";
                        $(timestampContainer).html( _extractTimestamp(_options.markers[index_start].options[_options.timeAttribute], _options));
                    }
                }else {
                    console.error("Time property "+ _options.timeAttribute +" not found in data");
                }
            }
        }
        var markers = [];
        for (i = this.options.minValue; i <= this.options.maxValue; i++) {
            _options.map.removeLayer(this.options.markers[i]);
        }
        for (i = _options.minValue; i <= index_start; i++) {
            if(i == _options.value) {
                markers.push(_options.markers[i]);
                _options.map.addLayer(_options.markers[i]);
            }
        }
        if(_options.showPopups) {
            this._openPopups(markers);
        }
        this.fire('rangechanged',{
            markers: markers,
        });
    },
    clearTimestamp: function(){
        //Hide the slider timestamp if not range and option alwaysShowDate is set on false
        if (!this.options.alwaysShowDate) {
            this.timestampContainer.innerHTML = "";
            this.timestampContainer.style.display = "none";
        }
    },

    extractTimestamp: function(time, options) {
        if (options.isEpoch) {
            time = (new Date(parseInt(time))).toString(); // this is local time
        }
        return time.substr(options.startTimeIdx, options.startTimeIdx + options.timeStrLength);
    },

    setPosition: function (position) {
        var map = this._map;

        if (map) {
            map.removeControl(this);
        }

        this.options.position = position;

        if (map) {
            map.addControl(this);
        }
        this.startSlider();
        return this;
    },

    _setPopupProperty: function(marker){
        if (marker._popup) {
            marker._orgpopup = marker._popup;
        }
        return marker;
    },

    _openPopups: function(markers) {
        var options = this.options;
        var that = this;
        markers.forEach(function (marker) {
            if(marker instanceof L.LayerGroup){
                that._openPopups(marker.getLayers());
            }else {
                if (marker._orgpopup) {
                    marker._popup = marker._orgpopup;
                    if (options.showAllPopups) {
                        marker._popup.options.autoClose = false;
                    }
                    marker.openPopup();
                } else if (options.popupContent) {
                    var popupOptions = options.popupOptions;
                    if (options.showAllPopups) {
                        popupOptions.autoClose = false;
                    }
                    marker.bindPopup(options.popupContent, popupOptions).openPopup();
                }
            }
        });
    },

});


L.control.sliderControl = function (options) {
    return new L.Control.SliderControl(options);
};