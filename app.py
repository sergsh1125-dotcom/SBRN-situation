import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="CBRN Editor", layout="wide")

BASE_URL = "https://raw.githubusercontent.com/sergsh1125-dotcom/SBRN-situation/main/svg/"

symbols = {
    "Радіація": "detect_radiation.svg",
    "Хімія": "detect_chemical.svg",
    "Біо": "detect_biological.svg",
    "Ядерний вибух": "nuclear_blast.svg",
    "Пост РХС": "cbrn_post.svg"
}

col_left, col_center = st.columns([1, 4])

# ================= LEFT =================
with col_left:
    st.markdown("""
    <div style="
        background:#ffcc00;
        color:black;
        font-weight:bold;
        text-align:center;
        padding:12px;
        border-radius:6px;
    ">
    УМОВНІ ЗНАКИ
    </div>
    """, unsafe_allow_html=True)

# ================= CENTER =================
with col_center:

    map_html = f"""
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
#panel {{
    position:absolute;
    top:10px;
    left:10px;
    z-index:9999;
    background:white;
    padding:10px;
    border-radius:6px;
    width:180px;
}}

button {{
    width:100%;
    margin-top:5px;
}}
</style>

<div id="panel">

<select id="symbolSelect">
<option value="">-- вибір --</option>
<option value="{BASE_URL}detect_radiation.svg">Радіація</option>
<option value="{BASE_URL}detect_chemical.svg">Хімія</option>
<option value="{BASE_URL}detect_biological.svg">Біо</option>
<option value="{BASE_URL}nuclear_blast.svg">Ядерний вибух</option>
<option value="{BASE_URL}cbrn_post.svg">Пост РХС</option>
</select>

<button onclick="enableText()">Текст</button>
<button onclick="disableMode()">ВИКЛ режим</button>
<button onclick="clearAll()">Очистити</button>

</div>

<div id="map" style="height:700px;"></div>

<script>

var map = L.map('map').setView([48.3794,31.1656],6);

L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);

var selectedIcon = "";
var textMode = false;
var addMode = true;

var data = JSON.parse(localStorage.getItem("cbrn") || "[]");

// LOAD
data.forEach(p => {{

    var icon = L.icon({{
        iconUrl: p.icon,
        iconSize: [32,32],
        iconAnchor: [16,16]
    }});

    var m = L.marker([p.lat,p.lng], {{icon:icon}}).addTo(map);

    if(p.text) m.bindPopup(p.text);

    m.on("click", function() {{
        map.removeLayer(m);
    }});
}});

// SELECT SYMBOL
document.getElementById("symbolSelect").onchange = function(e) {{
    selectedIcon = e.target.value;
    addMode = true;
}};

// CLICK MAP
map.on('click', function(e) {{

    if(!addMode || !selectedIcon) return;

    var text = "";

    if(textMode) {{
        text = prompt("Підпис:");
        textMode = false;
    }}

    var icon = L.icon({{
        iconUrl: selectedIcon,
        iconSize: [32,32],
        iconAnchor: [16,16]
    }});

    var m = L.marker(e.latlng, {{icon:icon}}).addTo(map);

    if(text) m.bindPopup(text);

    m.on("click", function() {{
        map.removeLayer(m);
    }});

    data.push({{
        lat: e.latlng.lat,
        lng: e.latlng.lng,
        icon: selectedIcon,
        text: text
    }});

    localStorage.setItem("cbrn", JSON.stringify(data));
}});

// TEXT (one-time)
function enableText() {{
    textMode = true;
    alert("Режим тексту ON (один клік)");
}}

// DISABLE ALL
function disableMode() {{
    addMode = false;
    selectedIcon = "";
    alert("Режим нанесення ВИМКНЕНО");
}}

// CLEAR
function clearAll() {{
    localStorage.removeItem("cbrn");
    location.reload();
}}

</script>
"""

    components.html(map_html, height=750)
