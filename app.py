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
    <div style="background:#ffcc00;color:black;padding:12px;font-weight:bold;text-align:center;border-radius:6px;">
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
    background:white;
    padding:10px;
    z-index:9999;
    border-radius:6px;
}}
</style>

<div id="panel">
<select id="symbolSelect">
<option value="">-- Умовні знаки --</option>
<option value="{BASE_URL}detect_radiation.svg">Радіація</option>
<option value="{BASE_URL}detect_chemical.svg">Хімія</option>
<option value="{BASE_URL}detect_biological.svg">Біо</option>
<option value="{BASE_URL}nuclear_blast.svg">Ядерний вибух</option>
<option value="{BASE_URL}cbrn_post.svg">Пост РХС</option>
</select>

<button onclick="toggleText()">Текст</button>
<button onclick="clearMap()">Очистити</button>
</div>

<div id="map" style="height:700px;"></div>

<script>

var map = L.map('map').setView([48.3794,31.1656],6);

L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);

var selectedIcon = "";
var textMode = false;

var data = JSON.parse(localStorage.getItem("cbrn") || "[]");

data.forEach(p => {{
    L.marker([p.lat,p.lng], {{
        icon: L.icon({{
            iconUrl: p.icon,
            iconSize: [32,32],
            iconAnchor: [16,16]
        }})
    }}).addTo(map).bindPopup(p.text || "");
}});

document.getElementById("symbolSelect").onchange = function(e) {{
    selectedIcon = e.target.value;
}};

map.on('click', function(e) {{

    if(!selectedIcon) {{
        alert("Вибери умовний знак");
        return;
    }}

    var text = "";

    if(textMode) {{
        text = prompt("Підпис:");
    }}

    var marker = L.marker(e.latlng, {{
        icon: L.icon({{
            iconUrl: selectedIcon,
            iconSize: [32,32],
            iconAnchor: [16,16]
        }})
    }}).addTo(map);

    if(text) marker.bindPopup(text);

    data.push({{
        lat: e.latlng.lat,
        lng: e.latlng.lng,
        icon: selectedIcon,
        text: text
    }});

    localStorage.setItem("cbrn", JSON.stringify(data));
}});

function toggleText() {{
    textMode = !textMode;
    alert("TEXT: " + (textMode ? "ON" : "OFF"));
}}

function clearMap() {{
    localStorage.removeItem("cbrn");
    location.reload();
}}

</script>
"""

    components.html(map_html, height=750)
