function getColor(d) {
    return d === 'wind' ? "#14A7E5" :
           d === 'solar' ? "#F8C52A" :
           d === 'gas' ? "#C23596" :
           d === 'other' ? "#1C0B2A" :
           d === 'hydro' ? "#3069B1" :
           d === 'oil' ? "#1C0B2A" :
           d === 'coal' ? "#B2B2B2" :
           d === 'nuclear' ? "#4CAE37" :
           d === 'biomass' ? "#FE9B32" :
           d === 'gas, oil' ? "#C23596" :
           d === 'coal, biomass' ? "#FE9B32" :
                        "#1C0B2A";
}

function capitalise(word) {
  return word[0].toUpperCase() + word.slice(1).toLowerCase();
}

function setNegativeToZero(value) {
    if (value<0) return 0
    else return value
}

function createVariables(geojsonFeatures){
    var dateLayers = [];

    for (let i in geojsonFeatures.timeseries) {
        const epochTime = geojsonFeatures.timeseries[i];
        dateLayer = new L.geoJSON(geojsonFeatures, {
            pointToLayer: (feature, latlng) => {
                var output = feature.properties.output[epochTime];
                var radius = null;

                if(output) radius = Math.sqrt(setNegativeToZero(output))*1000;
                else radius = 0;

                return new L.Circle(
                    [feature.properties.latitude, feature.properties.longitude], 
                    radius, {
                        fillOpacity: .75,
                        weight: 2,
                        color: getColor(feature.properties.fuel_type)
                    }
                );
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup('<p>Name: '+feature.properties.name);
            }
        });
        dateLayer.options.epoch = epochTime
        dateLayers[i] = dateLayer
    }

    return dateLayers;
}

function createLegend(){
    var legend = L.control({position: 'bottomleft'});
        legend.onAdd = function (mymap) {
            var div = L.DomUtil.create('div', 'info legend');
            labels = ['<p style="font-size: 20px"><strong>Fuel Types</strong>'],
            categories = ['wind', 'solar', 'gas', 'hydro', 'coal', 'nuclear', 'biomass', 'oil'];

            for (var i = 0; i < categories.length; i++) {

                    div.innerHTML += 
                    labels.push(
                        '<span id="dot" style="background-color:' + getColor(categories[i]) + '"></span> ' +
                    (categories[i] ? capitalise(categories[i]) : '+'));
            }
            labels.push('</p>')
            div.innerHTML = labels.join('<br>');
        return div;
    };
    
    return legend
}

document.addEventListener("DOMContentLoaded", function() {    

    $.getJSON("https://raw.githubusercontent.com/OSUKED/ElexonDataPortal/master/data/map.json", function(data) {
        var mymap = L.map('map').setView([53.96, -3.22], 5);

        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
          attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
          maxZoom: 18,
          id: 'mapbox/streets-v11',
          tileSize: 512,
          zoomOffset: -1,
          accessToken: 'pk.eyJ1IjoiZW5lcmd5dmlzIiwiYSI6ImNrbjR2aWo4azBsaHEycHM5dHByZzFnZW8ifQ.MyLCIQqHnNHQFWJQqs-j4w'
        }).addTo(mymap);
    
        var dateLayers = createVariables(data);
        var dateLayersGroup = L.layerGroup(dateLayers);
        dateLayersGroup.addTo(mymap);

        var legend = createLegend();
        legend.addTo(mymap);

        var sliderControl = null;

        sliderControl = L.control.sliderControl({
            position: "topright",
            layer: dateLayersGroup,
            sameDate: true,
            timeAttribute: "epoch",
            showPopups: false,
            showAllOnStart: true,
            startTimeIdx: 3,
            isEpoch: true,
            range: false,
            follow: 1
        });
        mymap.addControl(sliderControl);
        sliderControl.startSlider(334);
    });
});