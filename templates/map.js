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

document.addEventListener("DOMContentLoaded", function() {
    var mymap = L.map('map').setView({{ center }}, {{ zoom }});

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1,
      accessToken: 'pk.eyJ1IjoiZW5lcmd5dmlzIiwiYSI6ImNrbjR2aWo4azBsaHEycHM5dHByZzFnZW8ifQ.MyLCIQqHnNHQFWJQqs-j4w'
    }).addTo(mymap);

    var geojsonFeature = {{ geojson_features }}

    var geoJson = new L.geoJSON(geojsonFeature, {
        pointToLayer: (feature, latlng) => {
            return new L.Circle(
                [feature.properties.latitude, feature.properties.longitude], 
                Math.sqrt(feature.properties.output)*1000, {
                    fillOpacity: .75,
                    weight: 2,
                    color: getColor(feature.properties.fuel_type)
                }
            );
        },
        onEachFeature: function (feature, layer) {
            layer.bindPopup('<p>Name: '+feature.properties.name);
        }
    }).addTo(mymap);

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
    legend.addTo(mymap);
});