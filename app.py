import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="CBRN Editor", layout="wide")

BASE_URL = "https://raw.githubusercontent.com/sergsh1125-dotcom/SBRN-situation/main/svg/"

map_html = f"""
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
html, body {{
    margin:0;
    padding:0;
}}

#map {{
    height:92vh;
    width:100%;
}}

#panel {{
    position:absolute;
    top:10px;
    right:10px;
    z-index:9999;
    background:white;
    padding:10px;
    border-radius:6px;
    width:220px;
    box-shadow:0 2px 10px rgba(0,0,0,0.25);
}}

.label-text {{
    background:white;
    border:1px solid #333;
    border-radius:4px;
    padding:2px 6px;
    color:black;
    font-size:12px;
    font-weight:bold;
}}
</style>

<div id="panel">

<select id="symbolSelect">
<option value="">-- умовні знаки --</option>

<option value="{BASE_URL}detect_radiation.svg">
Точка виявлення радіоактивного забруднення
</option>

<option value="{BASE_URL}detect_chemical.svg">
Точка виявлення хімічного забруднення
</option>

<option value="{BASE_URL}detect_biological.svg">
Точка виявлення біологічного зараження
</option>

<option value="{BASE_URL}nuclear_blast.svg">
Епіцентр ядерного вибуху
</option>

<option value="{BASE_URL}radioactive_site.svg">
Радіаційно небезпечний об’єкт
</option>

<option value="{BASE_URL}chemical_hazard_site.svg">
Хімічно небезпечний об’єкт
</option>

<option value="{BASE_URL}biological_hazard_site.svg">
Біологічно небезпечний об’єкт
</option>

<option value="{BASE_URL}cbrn_recon_area.svg">
Район РХБ розвідки
</option>

<option value="{BASE_URL}decon_area_special.svg">
Район спеціальної обробки
</option>

<option value="{BASE_URL}decon_point_special.svg">
Пункт спеціальної обробки
</option>

<option value="{BASE_URL}cbrn_post.svg">
Пост радіаційного та хімічного спостереження
</option>

</select>

<br><br>

<button onclick="enableText()">Текст</button>
<button onclick="disableMode()">ВИКЛ нанесення</button>
<button onclick="clearAll()">Очистити</button>

</div>

<div id="map"></div>

<script>

var map = L.map('map').setView([48.3794,31.1656],6);

L.tileLayer(
    'https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
    {{
        maxZoom:19
    }}
).addTo(map);

var selectedIcon = "";
var textMode = false;

var data = JSON.parse(
    localStorage.getItem("cbrn") || "[]"
);

function drawItem(p) {{

    if(p.type === "text") {{

    var textIcon = L.divIcon({{
        className: "",
        html: '<div class="label-text">' + p.text + '</div>',
        iconSize: [150, 24],
        iconAnchor: [0, 12]
    }});

    var textMarker = L.marker(
        [p.lat, p.lng],
        {{
            icon: textIcon
        }}
    ).addTo(map);

    textMarker.on("click", function() {{

        map.removeLayer(textMarker);

        data = data.filter(function(item) {{
            return !(
                item.type === "text" &&
                item.lat === p.lat &&
                item.lng === p.lng &&
                item.text === p.text
            );
        }});

        localStorage.setItem(
            "cbrn",
            JSON.stringify(data)
        );
    }});

    return;
}}
    var icon = L.icon({{
        iconUrl:p.icon,
        iconSize:[32,32],
        iconAnchor:[16,16]
    }});

    var marker = L.marker(
        [p.lat,p.lng],
        {{icon:icon}}
    ).addTo(map);

    marker.on("click", function() {{

        map.removeLayer(marker);

        data = data.filter(function(item) {{
            return !(
                item.type === "symbol" &&
                item.lat === p.lat &&
                item.lng === p.lng &&
                item.icon === p.icon
            );
        }});

        localStorage.setItem(
            "cbrn",
            JSON.stringify(data)
        );
    }});
}}

data.forEach(function(p) {{
    drawItem(p);
}});
document.getElementById("symbolSelect").onchange =
function(e) {{
    selectedIcon = e.target.value;
    textMode = false;
}};
map.on("click", function(e) {{

    // РЕЖИМ ТЕКСТА

    if(textMode) {{

        var txt = prompt("Введіть текст:");

        if(txt && txt.trim() !== "") {{

            var obj = {{
                type:"text",
                lat:e.latlng.lat,
                lng:e.latlng.lng,
                text:txt
            }};

            data.push(obj);

            localStorage.setItem(
                "cbrn",
                JSON.stringify(data)
            );

            drawItem(obj);
        }}

        return;
    }}

    // РЕЖИМ ЗНАКОВ

    if(!selectedIcon) return;

    var obj = {{
        type:"symbol",
        lat:e.latlng.lat,
        lng:e.latlng.lng,
        icon:selectedIcon
    }};

    data.push(obj);

    localStorage.setItem(
        "cbrn",
        JSON.stringify(data)
    );

    drawItem(obj);
}});
function enableText() {{
    textMode = true;
    selectedIcon = "";
}}

function disableMode() {{
    textMode = false;
    selectedIcon = "";
}}

function clearAll() {{
    if(confirm("Очистити карту?")) {{
        localStorage.removeItem("cbrn");
        location.reload();
    }}
}}
</script>
"""

components.html(map_html, height=850)
