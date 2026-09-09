import streamlit as st
import pandas as pd
import numpy as np
import re
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Mobile Mind AI",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# LOAD CSS
# =========================================================

def load_css():

    css_path = os.path.join(
        os.path.dirname(__file__),
        "style.css"
    )

    if os.path.exists(css_path):

        with open(
            css_path,
            "r",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


load_css()


# =========================================================
# SESSION STATE
# =========================================================

if "screen" not in st.session_state:
    st.session_state.screen = "search"

if "results" not in st.session_state:
    st.session_state.results = None

if "selected_mobile" not in st.session_state:
    st.session_state.selected_mobile = None

if "selected_price_range" not in st.session_state:
    st.session_state.selected_price_range = None

if "selected_price_label" not in st.session_state:
    st.session_state.selected_price_label = None

if "selected_company" not in st.session_state:
    st.session_state.selected_company = "All Companies"


# =========================================================
# DATASET PATH
# =========================================================

DATASET_PATH = os.path.join(
    os.path.dirname(__file__),
    "mobile_price_final_dataset.csv"
)


if not os.path.exists(DATASET_PATH):

    st.error(
        "❌ mobile_price_final_dataset.csv nahi mili."
    )

    st.info(
        "CSV file ko app.py ke same folder mein rakhein."
    )

    st.stop()


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    try:

        data = pd.read_csv(
            DATASET_PATH
        )

        data = data.dropna(
            how="all"
        )

        data.columns = [
            str(col).strip()
            for col in data.columns
        ]

        return data

    except Exception as e:

        st.error(
            f"❌ Dataset load nahi ho saka: {e}"
        )

        st.stop()


df = load_data()


# =========================================================
# FIND COLUMN
# =========================================================

def find_column(candidates):

    for column in candidates:

        if column in df.columns:

            return column

    return None


# =========================================================
# MAIN COLUMNS
# =========================================================

MODEL_COLUMN = find_column([
    "Model Name",
    "Model",
    "Mobile Model",
    "Phone Model",
    "Name"
])


COMPANY_COLUMN = find_column([
    "Company Name",
    "Company",
    "Brand",
    "Brand Name"
])


PRICE_COLUMN = find_column([
    "Launched Price (Pakistan)",
    "Launch Price (Pakistan)",
    "Price (Pakistan)",
    "Price",
    "Pakistan Price",
    "Launched Price"
])


if MODEL_COLUMN is None:

    st.error(
        "❌ Model column dataset mein nahi mili."
    )

    st.stop()


if COMPANY_COLUMN is None:

    st.error(
        "❌ Company column dataset mein nahi mili."
    )

    st.stop()


if PRICE_COLUMN is None:

    st.error(
        "❌ Price column dataset mein nahi mili."
    )

    st.stop()


# =========================================================
# OPTIONAL COLUMNS
# =========================================================

RAM_COLUMN = find_column([
    "RAM",
    "Ram",
    "RAM_GB",
    "RAM (GB)",
    "RAM Size"
])


ROM_COLUMN = find_column([
    "ROM",
    "Storage",
    "Internal Storage",
    "ROM_GB",
    "Storage (GB)",
    "Storage Capacity"
])


TECHNOLOGY_COLUMN = find_column([
    "Technology",
    "Network Technology",
    "Network",
    "Network Type"
])


BATTERY_COLUMN = find_column([
    "Battery Capacity",
    "Battery",
    "Battery Size",
    "Battery_mAh",
    "Battery Capacity (mAh)"
])


SCREEN_COLUMN = find_column([
    "Screen Size",
    "Display Size",
    "Display",
    "Screen"
])


FRONT_CAMERA_COLUMN = find_column([
    "Front Camera",
    "Selfie Camera",
    "Front Camera MP",
    "Front Camera (MP)"
])


BACK_CAMERA_COLUMN = find_column([
    "Back Camera",
    "Rear Camera",
    "Main Camera",
    "Back Camera MP",
    "Back Camera (MP)"
])


PROCESSOR_COLUMN = find_column([
    "Processor",
    "CPU",
    "Chipset",
    "Processor Type",
    "Chipset Name"
])


WEIGHT_COLUMN = find_column([
    "Mobile Weight",
    "Weight",
    "Weight (g)",
    "Weight_g"
])


# =========================================================
# INTERNAL COLUMNS
# =========================================================

INTERNAL_COLUMNS = {
    "_price_numeric",
    "_internal_score"
}


# =========================================================
# CLEAN VALUE
# =========================================================

def clean_value(value):

    if value is None:
        return ""

    try:

        if pd.isna(value):
            return ""

    except Exception:

        pass

    value = str(value).strip()

    if value.lower() in [
        "",
        "nan",
        "none",
        "null",
        "unknown",
        "n/a",
        "na",
        "-",
        "--"
    ]:

        return ""

    return value


# =========================================================
# MODEL NAME
# =========================================================

def get_model_name(row):

    value = clean_value(
        row.get(
            MODEL_COLUMN,
            ""
        )
    )

    if value:
        return value

    return "Mobile"


# =========================================================
# GET SPEC
# =========================================================

def get_spec(
    row,
    column
):

    if column is None:
        return ""

    return clean_value(
        row.get(
            column,
            ""
        )
    )


# =========================================================
# NUMBER FROM VALUE
# =========================================================

def get_number(value):

    value = clean_value(
        value
    )

    if not value:
        return 0

    value = value.replace(
        ",",
        ""
    )

    match = re.search(
        r"\d+(?:\.\d+)?",
        value
    )

    if match:

        try:

            return float(
                match.group()
            )

        except Exception:

            return 0

    return 0


# =========================================================
# PRICE TO NUMBER
# =========================================================

def price_to_number(value):

    value = clean_value(
        value
    )

    if not value:
        return np.nan

    value = value.replace(
        ",",
        ""
    )

    value = re.sub(
        r"(PKR|Rs\.?|Rupees)",
        "",
        value,
        flags=re.IGNORECASE
    )

    match = re.search(
        r"\d+(?:\.\d+)?",
        value
    )

    if match:

        try:

            return float(
                match.group()
            )

        except Exception:

            return np.nan

    return np.nan


# =========================================================
# FORMAT PRICE
# =========================================================

def format_price(price):

    try:

        price = float(
            price
        )

        if price <= 0:
            return "Price Not Available"

        return (
            f"PKR {price:,.0f}"
        )

    except Exception:

        return "Price Not Available"


# =========================================================
# PREPARE PRICE
# =========================================================

df["_price_numeric"] = (
    df[PRICE_COLUMN]
    .apply(price_to_number)
)


df = df[
    df["_price_numeric"].notna()
].copy()


df = df[
    df["_price_numeric"] > 0
].copy()


# =========================================================
# CLEAN COMPANY
# =========================================================

df[COMPANY_COLUMN] = (
    df[COMPANY_COLUMN]
    .fillna("")
    .astype(str)
    .str.strip()
)


# =========================================================
# CLEAN TECHNOLOGY
# =========================================================

if TECHNOLOGY_COLUMN is not None:

    df[TECHNOLOGY_COLUMN] = (
        df[TECHNOLOGY_COLUMN]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# =========================================================
# AI-STYLE MOBILE STRENGTH
# =========================================================

def mobile_strength(row):

    score = 0

    # RAM

    ram = get_number(
        get_spec(
            row,
            RAM_COLUMN
        )
    )

    score += (
        min(ram, 32) * 3
    )

    # ROM

    rom = get_number(
        get_spec(
            row,
            ROM_COLUMN
        )
    )

    score += (
        min(rom, 1024) / 50
    )

    # BATTERY

    battery = get_number(
        get_spec(
            row,
            BATTERY_COLUMN
        )
    )

    score += (
        min(battery, 7000) / 500
    )

    # SCREEN

    screen = get_number(
        get_spec(
            row,
            SCREEN_COLUMN
        )
    )

    score += (
        min(screen, 7) * 2
    )

    # FRONT CAMERA

    front_camera = get_number(
        get_spec(
            row,
            FRONT_CAMERA_COLUMN
        )
    )

    score += (
        min(front_camera, 50) * 0.5
    )

    # BACK CAMERA

    back_camera = get_number(
        get_spec(
            row,
            BACK_CAMERA_COLUMN
        )
    )

    score += (
        min(back_camera, 200) * 0.3
    )

    return score


# =========================================================
# ADVANCED AI ANALYSIS
# =========================================================

def generate_ai_analysis(row):

    analysis = []

    recommended_for = []

    # -----------------------------------------------------
    # PERFORMANCE
    # -----------------------------------------------------

    ram = get_number(
        get_spec(
            row,
            RAM_COLUMN
        )
    )

    processor = get_spec(
        row,
        PROCESSOR_COLUMN
    )

    if ram >= 12:

        performance_text = (
            "Excellent performance potential with "
            "high RAM capacity."
        )

        recommended_for.append(
            "🚀 Heavy Multitasking"
        )

    elif ram >= 8:

        performance_text = (
            "Strong everyday performance with "
            "8 GB or more RAM."
        )

        recommended_for.append(
            "🚀 Multitasking"
        )

    elif ram >= 6:

        performance_text = (
            "Good performance for everyday apps "
            "and moderate multitasking."
        )

        recommended_for.append(
            "📱 Daily Use"
        )

    elif ram > 0:

        performance_text = (
            "Suitable for basic everyday tasks "
            "and lightweight applications."
        )

        recommended_for.append(
            "📱 Basic Use"
        )

    else:

        performance_text = (
            "Performance information is limited "
            "because RAM data is unavailable."
        )

    if processor:

        performance_text += (
            f" Processor: {processor}"
        )

    analysis.append(
        (
            "🚀",
            "Performance",
            performance_text
        )
    )

    # -----------------------------------------------------
    # CAMERA
    # -----------------------------------------------------

    back_camera = get_number(
        get_spec(
            row,
            BACK_CAMERA_COLUMN
        )
    )

    front_camera = get_number(
        get_spec(
            row,
            FRONT_CAMERA_COLUMN
        )
    )

    if back_camera >= 100:

        camera_text = (
            "High-resolution rear camera setup "
            "makes this a strong photography option."
        )

        recommended_for.append(
            "📸 Photography"
        )

    elif back_camera >= 50:

        camera_text = (
            "Good rear camera capability for "
            "everyday photography."
        )

        recommended_for.append(
            "📸 Photography"
        )

    elif back_camera > 0:

        camera_text = (
            "Decent camera setup for everyday "
            "photos and social media."
        )

    else:

        camera_text = (
            "Camera information is limited "
            "in the available dataset."
        )

    if front_camera >= 20:

        camera_text += (
            " The front camera is also suitable "
            "for selfies and video calls."
        )

    analysis.append(
        (
            "📸",
            "Camera",
            camera_text
        )
    )

    # -----------------------------------------------------
    # BATTERY
    # -----------------------------------------------------

    battery = get_number(
        get_spec(
            row,
            BATTERY_COLUMN
        )
    )

    if battery >= 6000:

        battery_text = (
            "Very strong battery capacity designed "
            "for extended daily usage."
        )

        recommended_for.append(
            "🔋 Long Battery"
        )

    elif battery >= 5000:

        battery_text = (
            "Strong battery capacity suitable for "
            "normal full-day usage."
        )

        recommended_for.append(
            "🔋 Long Battery"
        )

    elif battery >= 4000:

        battery_text = (
            "Good battery capacity for regular "
            "daily smartphone usage."
        )

    elif battery > 0:

        battery_text = (
            "Battery capacity is suitable for "
            "basic everyday usage."
        )

    else:

        battery_text = (
            "Battery information is unavailable."
        )

    analysis.append(
        (
            "🔋",
            "Battery",
            battery_text
        )
    )

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    screen = get_number(
        get_spec(
            row,
            SCREEN_COLUMN
        )
    )

    if screen >= 6.5:

        display_text = (
            "Large display provides a comfortable "
            "experience for videos, browsing and gaming."
        )

        recommended_for.append(
            "🎬 Entertainment"
        )

    elif screen >= 6:

        display_text = (
            "Balanced display size suitable for "
            "media consumption and everyday use."
        )

    elif screen > 0:

        display_text = (
            "Compact display suitable for "
            "regular smartphone tasks."
        )

    else:

        display_text = (
            "Display information is unavailable."
        )

    analysis.append(
        (
            "📱",
            "Display",
            display_text
        )
    )

    # -----------------------------------------------------
    # STORAGE
    # -----------------------------------------------------

    rom = get_number(
        get_spec(
            row,
            ROM_COLUMN
        )
    )

    if rom >= 512:

        storage_text = (
            "Very high storage capacity with plenty "
            "of room for applications, photos and videos."
        )

        recommended_for.append(
            "💾 Heavy Storage"
        )

    elif rom >= 256:

        storage_text = (
            "256 GB or more provides comfortable "
            "space for apps, media and files."
        )

        recommended_for.append(
            "💾 Media & Apps"
        )

    elif rom >= 128:

        storage_text = (
            "Good storage capacity for everyday "
            "apps, photos and videos."
        )

    elif rom > 0:

        storage_text = (
            "Storage is suitable for basic usage, "
            "although space may be more limited."
        )

    else:

        storage_text = (
            "Storage information is unavailable."
        )

    analysis.append(
        (
            "💾",
            "Storage",
            storage_text
        )
    )

    # -----------------------------------------------------
    # NETWORK
    # -----------------------------------------------------

    technology = get_spec(
        row,
        TECHNOLOGY_COLUMN
    )

    if technology:

        network_text = (
            f"Network technology available: "
            f"{technology}"
        )

    else:

        network_text = (
            "Network technology information "
            "is limited in the dataset."
        )

    analysis.append(
        (
            "📡",
            "Connectivity",
            network_text
        )
    )

    # -----------------------------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------------------------

    recommended_for = list(
        dict.fromkeys(
            recommended_for
        )
    )

    return analysis, recommended_for


# =========================================================
# PRICE RANGES
# =========================================================

PRICE_RANGES = {

    "0 – 10K":
        (0, 10000),

    "10K – 20K":
        (10000, 20000),

    "20K – 30K":
        (20000, 30000),

    "30K – 40K":
        (30000, 40000),

    "40K – 50K":
        (40000, 50000),

    "50K – 60K":
        (50000, 60000),

    "60K – 70K":
        (60000, 70000),

    "70K – 80K":
        (70000, 80000),

    "80K – 90K":
        (80000, 90000),

    "90K – 100K":
        (90000, 100000),

    "100K – 150K":
        (100000, 150000),

    "150K – 200K":
        (150000, 200000),

    "200K – 300K":
        (200000, 300000),

    "300K+":
        (300000, float("inf"))
}


# =========================================================
# QUICK PRICE FILTERS
# =========================================================

QUICK_PRICE_FILTERS = {

    "Under 50K":
        (0, 50000),

    "Under 100K":
        (0, 100000),

    "Under 150K":
        (0, 150000)
}


# =========================================================
# SEARCH MOBILES
# =========================================================

def search_mobiles(
    selected_company,
    selected_price_range
):

    filtered_df = df.copy()

    # -----------------------------------------------------
    # COMPANY FILTER
    # -----------------------------------------------------

    if selected_company != "All Companies":

        filtered_df = filtered_df[
            filtered_df[
                COMPANY_COLUMN
            ]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            selected_company
            .strip()
            .lower()
        ]

    # -----------------------------------------------------
    # PRICE FILTER
    # -----------------------------------------------------

    low, high = selected_price_range

    if np.isinf(high):

        filtered_df = filtered_df[
            filtered_df[
                "_price_numeric"
            ] >= low
        ]

    else:

        filtered_df = filtered_df[
            (
                filtered_df[
                    "_price_numeric"
                ] >= low
            )
            &
            (
                filtered_df[
                    "_price_numeric"
                ] < high
            )
        ]

    # -----------------------------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------------------------

    filtered_df = (
        filtered_df
        .drop_duplicates(
            subset=[
                MODEL_COLUMN
            ],
            keep="first"
        )
    )

    # -----------------------------------------------------
    # AI RANKING
    # -----------------------------------------------------

    if len(filtered_df) > 0:

        filtered_df = (
            filtered_df.copy()
        )

        filtered_df[
            "_internal_score"
        ] = filtered_df.apply(
            mobile_strength,
            axis=1
        )

        filtered_df = (
            filtered_df
            .sort_values(
                by="_internal_score",
                ascending=False
            )
        )

    return filtered_df


# =========================================================
# SELECT PRICE
# =========================================================

def select_price(
    label,
    price_range
):

    st.session_state.selected_price_label = (
        label
    )

    st.session_state.selected_price_range = (
        price_range
    )

    results = search_mobiles(
        st.session_state.selected_company,
        price_range
    )

    st.session_state.results = (
        results
    )

    st.session_state.selected_mobile = (
        None
    )

    st.session_state.screen = (
        "results"
    )

    st.rerun()


# =========================================================
# SEARCH SCREEN
# =========================================================

if st.session_state.screen == "search":

    st.title(
        "📱 Mobile Mind AI"
    )

    st.write(
        "Find the right mobile according to your "
        "preferred company and budget."
    )

    st.divider()

    # =====================================================
    # COMPANY
    # =====================================================

    st.subheader(
        "🏢 Select Company"
    )

    companies = sorted(
        df[
            COMPANY_COLUMN
        ]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    companies = [
        company
        for company in companies
        if company
    ]

    company_options = [
        "All Companies"
    ] + companies

    current_company = (
        st.session_state.selected_company
    )

    if current_company not in company_options:

        current_company = (
            "All Companies"
        )

    selected_company = st.selectbox(
        "Choose Company",
        company_options,
        index=company_options.index(
            current_company
        ),
        key="company_selector"
    )

    st.session_state.selected_company = (
        selected_company
    )

    st.divider()

    # =====================================================
    # PRICE
    # =====================================================

    st.subheader(
        "💰 Select Price Range"
    )

    st.caption(
        "Select any one price range. "
        "Results will open automatically."
    )

    # =====================================================
    # QUICK FILTERS
    # =====================================================

    st.markdown(
        "### ⚡ Quick Price Filters"
    )

    quick_labels = list(
        QUICK_PRICE_FILTERS.keys()
    )

    quick_cols = st.columns(
        3,
        gap="medium"
    )

    for col, label in zip(
        quick_cols,
        quick_labels
    ):

        with col:

            if st.button(
                f"⚡ {label}",
                use_container_width=True,
                key=f"quick_{label}"
            ):

                select_price(
                    f"⚡ {label}",
                    QUICK_PRICE_FILTERS[
                        label
                    ]
                )

    st.markdown("")

    # =====================================================
    # DETAILED PRICE
    # =====================================================

    st.markdown(
        "### 📊 Detailed Price Ranges"
    )

    detailed_labels = list(
        PRICE_RANGES.keys()
    )

    for i in range(
        0,
        len(detailed_labels),
        3
    ):

        current_labels = (
            detailed_labels[
                i:i + 3
            ]
        )

        cols = st.columns(
            3,
            gap="medium"
        )

        for col, label in zip(
            cols,
            current_labels
        ):

            with col:

                if st.button(
                    f"💰 {label}",
                    use_container_width=True,
                    key=f"price_{label}"
                ):

                    select_price(
                        f"💰 {label}",
                        PRICE_RANGES[
                            label
                        ]
                    )

    st.stop()


# =========================================================
# RESULTS SCREEN
# =========================================================

if st.session_state.screen == "results":

    st.title(
        "📱 Matching Mobiles"
    )

    # =====================================================
    # BACK
    # =====================================================

    if st.button(
        "← Back to Search",
        key="back_to_search_top"
    ):

        st.session_state.screen = (
            "search"
        )

        st.session_state.results = (
            None
        )

        st.rerun()

    st.divider()

    results = (
        st.session_state.results
    )

    # =====================================================
    # NO RESULTS
    # =====================================================

    if results is None or len(results) == 0:

        st.warning(
            "😔 Is company aur price range mein "
            "koi mobile nahi mila."
        )

        st.info(
            "Please koi doosra company ya price range "
            "select karein."
        )

        if st.button(
            "🔎 Search Again",
            use_container_width=True,
            key="search_again_empty"
        ):

            st.session_state.screen = (
                "search"
            )

            st.session_state.results = (
                None
            )

            st.rerun()

        st.stop()

    # =====================================================
    # BEST MOBILE
    # =====================================================

    best_mobile = (
        results.iloc[0]
    )

    best_model = get_model_name(
        best_mobile
    )

    best_company = clean_value(
        best_mobile.get(
            COMPANY_COLUMN,
            ""
        )
    )

    best_price = format_price(
        best_mobile[
            "_price_numeric"
        ]
    )

    # =====================================================
    # AI SPECIFICATION GRID
    # =====================================================

    ai_specs = []

    if best_company:

        ai_specs.append(
            (
                "🏢",
                "Company",
                best_company
            )
        )

    ai_specs.append(
        (
            "💰",
            "Price",
            best_price
        )
    )

    technology_value = get_spec(
        best_mobile,
        TECHNOLOGY_COLUMN
    )

    if technology_value:

        ai_specs.append(
            (
                "📡",
                "Technology",
                technology_value
            )
        )

    ram_value = get_spec(
        best_mobile,
        RAM_COLUMN
    )

    if ram_value:

        ai_specs.append(
            (
                "🧠",
                "RAM",
                ram_value
            )
        )

    rom_value = get_spec(
        best_mobile,
        ROM_COLUMN
    )

    if rom_value:

        ai_specs.append(
            (
                "💾",
                "ROM",
                rom_value
            )
        )

    processor_value = get_spec(
        best_mobile,
        PROCESSOR_COLUMN
    )

    if processor_value:

        processor_short = (
            processor_value
        )

        if len(processor_short) > 85:

            processor_short = (
                processor_short[:82]
                + "..."
            )

        ai_specs.append(
            (
                "⚡",
                "Processor",
                processor_short
            )
        )

    battery_value = get_spec(
        best_mobile,
        BATTERY_COLUMN
    )

    if battery_value:

        ai_specs.append(
            (
                "🔋",
                "Battery",
                battery_value
            )
        )

    screen_value = get_spec(
        best_mobile,
        SCREEN_COLUMN
    )

    if screen_value:

        ai_specs.append(
            (
                "📱",
                "Screen",
                screen_value
            )
        )

    front_camera_value = get_spec(
        best_mobile,
        FRONT_CAMERA_COLUMN
    )

    if front_camera_value:

        front_camera_short = (
            front_camera_value
        )

        if len(front_camera_short) > 85:

            front_camera_short = (
                front_camera_short[:82]
                + "..."
            )

        ai_specs.append(
            (
                "🤳",
                "Front Camera",
                front_camera_short
            )
        )

    back_camera_value = get_spec(
        best_mobile,
        BACK_CAMERA_COLUMN
    )

    if back_camera_value:

        back_camera_short = (
            back_camera_value
        )

        if len(back_camera_short) > 85:

            back_camera_short = (
                back_camera_short[:82]
                + "..."
            )

        ai_specs.append(
            (
                "📷",
                "Back Camera",
                back_camera_short
            )
        )

    weight_value = get_spec(
        best_mobile,
        WEIGHT_COLUMN
    )

    if weight_value:

        ai_specs.append(
            (
                "⚖️",
                "Weight",
                weight_value
            )
        )

    # =====================================================
    # AI ANALYSIS
    # =====================================================

    ai_analysis, recommended_for = (
        generate_ai_analysis(
            best_mobile
        )
    )

    # =====================================================
    # AI BEST CHOICE
    # =====================================================

    with st.container(
        border=True
    ):

        st.subheader(
            "🏆 AI Best Choice"
        )

        st.markdown(
            f"### 📱 {best_model}"
        )

        if best_company:

            st.write(
                f"🏢 **{best_company}**"
            )

        st.write(
            "🤖 AI selected this mobile by analyzing "
            "the available hardware specifications "
            "within your selected budget."
        )

        st.markdown(
            "### 📊 Key Specifications"
        )

        # -------------------------------------------------
        # SPECIFICATION GRID
        # -------------------------------------------------

        for i in range(
            0,
            len(ai_specs),
            3
        ):

            cols = st.columns(
                3,
                gap="medium"
            )

            for col, spec in zip(
                cols,
                ai_specs[i:i + 3]
            ):

                icon, label, value = spec

                with col:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**{icon} {label}**"
                        )

                        st.write(
                            value
                        )

        st.markdown("")

        # -------------------------------------------------
        # AI ANALYSIS
        # -------------------------------------------------

        st.markdown(
            "### ✨ AI Analysis"
        )

        for icon, title, text in ai_analysis:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**{icon} {title}**"
                )

                st.write(
                    text
                )

        # -------------------------------------------------
        # RECOMMENDED FOR
        # -------------------------------------------------

        if recommended_for:

            st.markdown(
                "### 🎯 Recommended For"
            )

            tag_cols = st.columns(
                min(
                    len(recommended_for),
                    4
                ),
                gap="medium"
            )

            for col, tag in zip(
                tag_cols,
                recommended_for
            ):

                with col:

                    st.info(
                        tag
                    )

        # -------------------------------------------------
        # FINAL VERDICT
        # -------------------------------------------------

        st.markdown(
            "### 🤖 AI Verdict"
        )

        # IMPORTANT:
        # These variables are defined specifically
        # for the verdict section. This fixes the
        # Pylance undefined-variable errors.

        verdict_ram = get_number(
            get_spec(
                best_mobile,
                RAM_COLUMN
            )
        )

        verdict_rom = get_number(
            get_spec(
                best_mobile,
                ROM_COLUMN
            )
        )

        verdict_battery = get_number(
            get_spec(
                best_mobile,
                BATTERY_COLUMN
            )
        )

        verdict_back_camera = get_number(
            get_spec(
                best_mobile,
                BACK_CAMERA_COLUMN
            )
        )

        if len(recommended_for) >= 4:

            verdict = (
                "⭐ Strong all-rounder with a balanced "
                "combination of performance, camera, "
                "battery and storage capabilities."
            )

        elif (
            verdict_back_camera >= 100
            and verdict_battery >= 5000
        ):

            verdict = (
                "⭐ Excellent choice for users who "
                "prioritize camera quality and battery life."
            )

        elif (
            verdict_ram >= 8
            and verdict_rom >= 256
        ):

            verdict = (
                "⭐ Strong choice for multitasking, "
                "apps and media storage."
            )

        elif verdict_battery >= 5000:

            verdict = (
                "⭐ Good choice for users who prioritize "
                "battery life and everyday usage."
            )

        else:

            verdict = (
                "⭐ Suitable option within the selected "
                "budget based on the available specifications."
            )

        st.success(
            verdict
        )

    st.markdown("")

    # =====================================================
    # RESULT INFO
    # =====================================================

    st.subheader(
        f"📋 {len(results)} Matching Mobiles"
    )

    if st.session_state.selected_price_label:

        st.caption(
            f"Selected Price Range: "
            f"{st.session_state.selected_price_label}"
        )

    # =====================================================
    # MOBILE CARDS
    # =====================================================

    for i in range(
        0,
        len(results),
        2
    ):

        row_items = results.iloc[
            i:i + 2
        ]

        cols = st.columns(
            2,
            gap="large"
        )

        for col, (_, row) in zip(
            cols,
            row_items.iterrows()
        ):

            with col:

                with st.container(
                    border=True
                ):

                    model_name = (
                        get_model_name(
                            row
                        )
                    )

                    company_name = (
                        clean_value(
                            row.get(
                                COMPANY_COLUMN,
                                ""
                            )
                        )
                    )

                    mobile_price = (
                        format_price(
                            row[
                                "_price_numeric"
                            ]
                        )
                    )

                    # Only first result gets AI label

                    if i == 0:

                        st.success(
                            "🤖 AI BEST CHOICE"
                        )

                    st.subheader(
                        f"📱 {model_name}"
                    )

                    if company_name:

                        st.write(
                            f"🏢 **{company_name}**"
                        )

                    st.write(
                        f"💰 **{mobile_price}**"
                    )

                    technology = get_spec(
                        row,
                        TECHNOLOGY_COLUMN
                    )

                    if technology:

                        st.write(
                            f"📡 **Technology:** "
                            f"{technology}"
                        )

                    ram = get_spec(
                        row,
                        RAM_COLUMN
                    )

                    if ram:

                        st.write(
                            f"🧠 **RAM:** {ram}"
                        )

                    rom = get_spec(
                        row,
                        ROM_COLUMN
                    )

                    if rom:

                        st.write(
                            f"💾 **ROM:** {rom}"
                        )

                    battery = get_spec(
                        row,
                        BATTERY_COLUMN
                    )

                    if battery:

                        st.write(
                            f"🔋 **Battery:** "
                            f"{battery}"
                        )

                    st.markdown("")

                    if st.button(
                        "View Details →",
                        use_container_width=True,
                        key=f"details_{i}_{model_name}"
                    ):

                        st.session_state.selected_mobile = (
                            row.to_dict()
                        )

                        st.session_state.screen = (
                            "details"
                        )

                        st.rerun()

    # =====================================================
    # SEARCH AGAIN
    # =====================================================

    st.divider()

    if st.button(
        "🔎 Search Again",
        use_container_width=True,
        key="search_again_bottom"
    ):

        st.session_state.screen = (
            "search"
        )

        st.session_state.results = (
            None
        )

        st.session_state.selected_mobile = (
            None
        )

        st.rerun()

    st.stop()


# =========================================================
# DETAILS SCREEN
# =========================================================

if st.session_state.screen == "details":

    mobile = (
        st.session_state.selected_mobile
    )

    if mobile is None:

        st.session_state.screen = (
            "search"
        )

        st.rerun()

    # =====================================================
    # BACK
    # =====================================================

    if st.button(
        "← Back to Matching Mobiles",
        key="back_to_results_top"
    ):

        st.session_state.screen = (
            "results"
        )

        st.rerun()

    st.divider()

    # =====================================================
    # BASIC INFO
    # =====================================================

    model_name = get_model_name(
        mobile
    )

    company_name = clean_value(
        mobile.get(
            COMPANY_COLUMN,
            ""
        )
    )

    price = format_price(
        mobile.get(
            "_price_numeric",
            0
        )
    )

    st.title(
        f"📱 {model_name}"
    )

    if company_name:

        st.write(
            f"🏢 **Company:** {company_name}"
        )

    st.write(
        f"💰 **Price:** {price}"
    )

    st.divider()

    # =====================================================
    # KEY SPECIFICATIONS
    # =====================================================

    st.subheader(
        "⭐ Key Specifications"
    )

    key_specs = []

    if TECHNOLOGY_COLUMN:

        value = get_spec(
            mobile,
            TECHNOLOGY_COLUMN
        )

        if value:

            key_specs.append(
                (
                    "📡 Technology",
                    value
                )
            )

    if RAM_COLUMN:

        value = get_spec(
            mobile,
            RAM_COLUMN
        )

        if value:

            key_specs.append(
                (
                    "🧠 RAM",
                    value
                )
            )

    if ROM_COLUMN:

        value = get_spec(
            mobile,
            ROM_COLUMN
        )

        if value:

            key_specs.append(
                (
                    "💾 ROM",
                    value
                )
            )

    if PROCESSOR_COLUMN:

        value = get_spec(
            mobile,
            PROCESSOR_COLUMN
        )

        if value:

            key_specs.append(
                (
                    "⚡ Processor",
                    value
                )
            )

    if BATTERY_COLUMN:

        value = get_spec(
            mobile,
            BATTERY_COLUMN
        )

        if value:

            key_specs.append(
                (
                    "🔋 Battery",
                    value
                )
            )

    if SCREEN_COLUMN:

        value = get_spec(
            mobile,
            SCREEN_COLUMN
        )

        if value:

            key_specs.append(
                (
                    "📱 Screen",
                    value
                )
            )

    if FRONT_CAMERA_COLUMN:

        value = get_spec(
            mobile,
            FRONT_CAMERA_COLUMN
        )

        if value:

            key_specs.append(
                (
                    "🤳 Front Camera",
                    value
                )
            )

    if BACK_CAMERA_COLUMN:

        value = get_spec(
            mobile,
            BACK_CAMERA_COLUMN
        )

        if value:

            key_specs.append(
                (
                    "📷 Back Camera",
                    value
                )
            )

    if WEIGHT_COLUMN:

        value = get_spec(
            mobile,
            WEIGHT_COLUMN
        )

        if value:

            key_specs.append(
                (
                    "⚖️ Weight",
                    value
                )
            )

    # =====================================================
    # KEY SPEC GRID
    # =====================================================

    if key_specs:

        for i in range(
            0,
            len(key_specs),
            3
        ):

            cols = st.columns(
                3,
                gap="medium"
            )

            for col, item in zip(
                cols,
                key_specs[i:i + 3]
            ):

                with col:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**{item[0]}**"
                        )

                        st.write(
                            item[1]
                        )

    st.divider()

    # =====================================================
    # COMPLETE SPECIFICATIONS
    # =====================================================

    st.subheader(
        "📋 Complete Specifications"
    )

    complete_specs = []

    for column in df.columns:

        if column in INTERNAL_COLUMNS:

            continue

        value = clean_value(
            mobile.get(
                column,
                ""
            )
        )

        if not value:

            continue

        if column in [
            MODEL_COLUMN,
            COMPANY_COLUMN,
            PRICE_COLUMN
        ]:

            continue

        complete_specs.append(
            (
                column,
                value
            )
        )

    if complete_specs:

        for i in range(
            0,
            len(complete_specs),
            3
        ):

            cols = st.columns(
                3,
                gap="medium"
            )

            for col, item in zip(
                cols,
                complete_specs[i:i + 3]
            ):

                with col:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**{item[0]}**"
                        )

                        st.write(
                            item[1]
                        )

    else:

        st.info(
            "No additional specifications available."
        )

    st.divider()

    # =====================================================
    # BACK BUTTON
    # =====================================================

    if st.button(
        "← Back to Matching Mobiles",
        use_container_width=True,
        key="back_to_results_bottom"
    ):

        st.session_state.screen = (
            "results"
        )

        st.rerun()

    st.stop()