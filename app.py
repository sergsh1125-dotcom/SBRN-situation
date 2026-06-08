import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="CBRN Symbol Editor", layout="wide")

BASE_URL = "https://raw.githubusercontent.com/sergsh1125-dotcom/SBRN-situation/main/svg/"

symbols = [
    {"label": "Радіаційне зараження", "icon": "detect_radiation.svg"},
    {"label": "Хімічне зараження", "icon": "detect_chemical.svg"},
    {"label": "Біологічне зараження", "icon": "detect_biological.svg"},
    {"label": "Ядерний вибух", "icon": "nuclear_blast.svg"},
    {"label": "Пост РХС", "icon": "cbrn_post.svg"},
]

selected = st.selectbox("Умовні знаки", symbols, format_func=lambda x: x["label"])
icon_url = BASE_URL + selected["icon"]

col_left, col_center = st.columns([1, 4])

# =========================
# ЛЕВАЯ ПАНЕЛЬ
# =========================
with col_left:

    st.markdown(
        """
        <div style="
            background:#ffcc00;
            color:black;
            font-weight:bold;
            padding:15px;
            text-align:center;
            border-radius:6px;
            margin-bottom:10px;
        ">
        УМОВНІ ЗНАКИ
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("ТЕКСТ (підпис)"):
        st.session_state["text_mode"] = True
    else:
        st.session_state.setdefault("text_mode", False)

# =========================
# ЦЕНТР - КАРТА
# =========================
with col_center:

    map_html = f"""
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<div id="map" style="height:700px;"></div>

<div style="margin-top:10px; text-align:center;">
    <button onclick="clearAll()">Очистити карту</button>
</div>

<script>

// ---------------- MAP ----------------
var map = L.map('map').setView([48.3794, 31.1656], 6);

L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: 'OSM'
}}).addTo(map);

// ---------------- STORAGE ----------------
var markers = JSON.parse(localStorage.getItem("cbrn_markers") || "[]");

function saveMarkers() {{
    localStorage.setItem("cbrn_markers", JSON.stringify(markers));
}}

// ---------------- ICON ----------------
var selectedIcon = "{icon_url}";

// ---------------- LOAD SAVED ----------------
markers.forEach(m => {{
    L.marker([m.lat, m.lng], {{
        icon: L.icon({{
            iconUrl: m.icon,
            iconSize: [32,32],
            iconAnchor: [16,16]
        }})
    }}).addTo(map).bindPopup(m.text || "");
}});

// ---------------- ADD MARKER ----------------
map.on('click', function(e) {{

    var text = "";

    if(window.textMode) {{
        text = prompt("Введіть підпис:");
    }}

    var icon = L.icon({{
        iconUrl: selectedIcon,
        iconSize: [32,32],
        iconAnchor: [16,16]
    }});

    L.marker(e.latlng, {{icon: icon}})
        .addTo(map)
        .bindPopup(text || "");

    markers.push({{
        lat: e.latlng.lat,
        lng: e.latlng.lng,
        icon: selectedIcon,
        text: text
    }});

    saveMarkers();
}});

// ---------------- CLEAR ----------------
function clearAll() {{
    localStorage.removeItem("cbrn_markers");
    location.reload();
}}

window.textMode = false;

</script>
"""

    components.html(map_html, height=750)
components.html(map_html, height=750)
