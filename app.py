import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="CBRN Symbol Editor", layout="wide")

# -----------------------------
# SVG BASE URL (ВАЖНО: твой репозиторий)
# -----------------------------
BASE_URL = "https://raw.githubusercontent.com/sergsh1125-dotcom/SBRN-situation/main/svg/"

# -----------------------------
# СИМВОЛЫ
# -----------------------------
symbols = [
    {"label": "Радіаційне зараження", "icon": "detect_radiation.svg"},
    {"label": "Хімічне зараження", "icon": "detect_chemical.svg"},
    {"label": "Біологічне зараження", "icon": "detect_biological.svg"},
    {"label": "Ядерний вибух", "icon": "nuclear_blast.svg"},
    {"label": "Пост РХС", "icon": "cbrn_post.svg"},
]

selected = st.selectbox(
    "Умовні знаки",
    symbols,
    format_func=lambda x: x["label"]
)

icon_url = BASE_URL + selected["icon"]

# -----------------------------
# HTML + LEAFLET
# -----------------------------
map_html = f"""
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<div style="margin-bottom:10px;">
<button onclick="clearMarkers()">Очистити карту</button>
</div>

<div id="map" style="height:700px;"></div>

<script>
var map = L.map('map').setView([48.3794, 31.1656], 6);

L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: 'OSM'
}}).addTo(map);

var markers = [];

var selectedIcon = "{icon_url}";

function addMarker(e) {{
    var icon = L.icon({{
        iconUrl: selectedIcon,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    }});

    var m = L.marker(e.latlng, {{icon: icon}}).addTo(map);
    markers.push(m);
}}

map.on('click', addMarker);

function clearMarkers() {{
    markers.forEach(m => map.removeLayer(m));
    markers = [];
}}
</script>
"""

components.html(map_html, height=750)
