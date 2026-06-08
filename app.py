import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="CBRN Editor", layout="wide")

BASE_URL = "https://raw.githubusercontent.com/sergsh1125-dotcom/SBRN-situation/main/svg/"

symbols = [
    {"label": "Радіація", "icon": "detect_radiation.svg"},
    {"label": "Хімія", "icon": "detect_chemical.svg"},
    {"label": "Біо", "icon": "detect_biological.svg"},
    {"label": "Ядерний вибух", "icon": "nuclear_blast.svg"},
    {"label": "Пост", "icon": "cbrn_post.svg"},
]

selected = st.selectbox("Умовні знаки", symbols, format_func=lambda x: x["label"])

icon_url = BASE_URL + selected["icon"]

col_left, col_center = st.columns([1, 4])

# ================= LEFT =================
with col_left:

    st.markdown("""
    <div style="background:#ffcc00;color:black;padding:12px;font-weight:bold;text-align:center;border-radius:6px;">
    УМОВНІ ЗНАКИ
    </div>
    """, unsafe_allow_html=True)

    text_mode = st.button("ТЕКСТ")

# ================= CENTER =================
with col_center:

    map_html = f"""
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<div id="map" style="height:700px;"></div>

<div style="margin-top:10px; text-align:center;">
<button onclick="clearMap()">Очистити карту</button>
<button onclick="toggleText()">Текст: ON/OFF</button>
</div>

<script>

var map = L.map('map').setView([48.3794, 31.1656], 6);

L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: 'OSM'
}}).addTo(map);

var iconUrl = "{icon_url}";
var textMode = false;

// ---------------- storage ----------------
var data = JSON.parse(localStorage.getItem("cbrn") || "[]");

// load saved
data.forEach(p => {{
    L.marker([p.lat, p.lng], {{
        icon: L.icon({{
            iconUrl: p.icon,
            iconSize: [32,32],
            iconAnchor: [16,16]
        }})
    }}).addTo(map).bindPopup(p.text || "");
}});

function save() {{
    localStorage.setItem("cbrn", JSON.stringify(data));
}}

// ---------------- click ----------------
map.on('click', function(e) {{

    var text = "";

    if(textMode) {{
        text = prompt("Підпис:");
    }}

    var marker = L.marker(e.latlng, {{
        icon: L.icon({{
            iconUrl: iconUrl,
            iconSize: [32,32],
            iconAnchor: [16,16]
        }})
    }}).addTo(map);

    if(text) marker.bindPopup(text);

    data.push({{
        lat: e.latlng.lat,
        lng: e.latlng.lng,
        icon: iconUrl,
        text: text
    }});

    save();
}});

// ---------------- clear ----------------
function clearMap() {{
    localStorage.removeItem("cbrn");
    location.reload();
}}

// ---------------- toggle text ----------------
function toggleText() {{
    textMode = !textMode;
    alert("Текст режим: " + (textMode ? "ON" : "OFF"));
}}

</script>
"""

    components.html(map_html, height=750)
