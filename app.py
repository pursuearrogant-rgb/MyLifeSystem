import streamlit as st
import datetime
import time
import pandas as pd
import os

# --- 1. 系統初始化設置 ---
st.set_page_config(page_title="PROTOCOL: AWAKEN", page_icon="⚡", layout="wide")

# 定義檔案名稱 (這就是你的數位帳本)
DATA_FILE = "player_data.csv"

# --- 2. 核心函數：讀取與存檔 (Save/Load System) ---
def load_data():
    # 如果帳本不存在，就一本新的 (初始設定)
    if not os.path.exists(DATA_FILE):
        default_data = {
            "level": 1,
            "xp_current": 0,
            "xp_next": 100,
            "vitality": 100,
            "streak": 0,
            "last_login": str(datetime.date.today())
        }
        df = pd.DataFrame([default_data])
        df.to_csv(DATA_FILE, index=False)
        return default_data
    else:
        # 如果存在，就讀取它
        df = pd.read_csv(DATA_FILE)
        return df.iloc[0].to_dict()

def save_data(data):
    # 把最新的數據寫回帳本
    df = pd.DataFrame([data])
    df.to_csv(DATA_FILE, index=False)

# 初始化：從帳本讀取玩家數據
player = load_data()

# --- 3. 鋼鐵人介面 CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #00ffcc; font-family: 'Courier New', monospace; }
    h1, h2, h3 { text-shadow: 0 0 10px #00ffcc; color: #00ffcc !important; }
    div.stButton > button { background-color: #1f2937; color: #00ffcc; border: 1px solid #00ffcc; border-radius: 5px; transition: all 0.3s; }
    div.stButton > button:hover { background-color: #00ffcc; color: #0e1117; box-shadow: 0 0 15px #00ffcc; }
    div[data-testid="stMetricValue"] { color: #00ffcc; text-shadow: 0 0 5px #00ffcc; }
    div.stProgress > div > div > div > div { background-color: #00ffcc; }
</style>
""", unsafe_allow_html=True)

# --- 4. 側邊欄：顯示即時狀態 ---
with st.sidebar:
    st.header(f"👤 ID: COMMANDER (LV.{player['level']})")
    st.markdown("---")
    
    # 計算進度條 (避免超過 1.0 報錯)
    progress_val = min(player['xp_current'] / player['xp_next'], 1.0)
    
    st.write(f"**EXP Progress:** {player['xp_current']} / {player['xp_next']}")
    st.progress(progress_val)
    
    if st.button("🔴 重置系統 (Reset)"):
        # 這是緊急按鈕，把檔案刪除重來
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.rerun()

# --- 5. 判斷時間與顯示主控台 ---
current_hour = datetime.datetime.now().hour
is_daytime = 6 <= current_hour < 18
phase_name = "DAY PHASE ☀️" if is_daytime else "NIGHT PHASE 🌙"

st.title(f"⚡ PROTOCOL: AWAKEN")
st.caption(f"SYSTEM TIME: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | MODE: {phase_name}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("LEVEL", f"LV. {player['level']}")
with col2:
    st.metric("XP GAINED", f"{player['xp_current']}")
with col3:
    st.metric("VITALITY", f"{player['vitality']}%")
with col4:
    st.metric("STREAK", f"{player['streak']} Days")

st.markdown("---")

# --- 6. 任務執行區 ---
st.subheader("🚀 MISSION CONTROL")
tab1, tab2 = st.tabs(["⚔️ 執行任務", "📊 數據分析"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("🏋️ **體能訓練 (Physical)**")
        if st.button("執行：健身房重訓 (+20 XP)"):
            # --- 數據更新邏輯 ---
            player['xp_current'] += 20
            player['vitality'] -= 10
            
            # 升級判斷
            if player['xp_current'] >= player['xp_next']:
                player['level'] += 1
                player['xp_current'] -= player['xp_next']
                player['xp_next'] = int(player['xp_next'] * 1.2) # 下一級更難 (複利)
                st.toast(f"🎉 恭喜升級！現在是 Level {player['level']}！")
            
            # 存檔！
            save_data(player)
            st.success("訓練完成！數據已寫入帳本。")
            st.balloons()
            time.sleep(1)
            st.rerun() # 自動重新整理畫面

    with col_b:
        st.info("🧠 **智力開發 (Intel)**")
        if st.button("執行：Python 學習 (+15 XP)"):
            player['xp_current'] += 15
            
            if player['xp_current'] >= player['xp_next']:
                player['level'] += 1
                player['xp_current'] -= player['xp_next']
                player['xp_next'] = int(player['xp_next'] * 1.2)
                st.toast(f"🎉 恭喜升級！現在是 Level {player['level']}！")
                
            save_data(player)
            st.success("知識下載完畢。")
            st.snow()
            time.sleep(1)
            st.rerun()

with tab2:
    st.write("### 📜 System Ledger (你的數位帳本)")
    # 直接讀取並顯示那個 CSV 檔案給你看
    if os.path.exists(DATA_FILE):
        df_display = pd.read_csv(DATA_FILE)
        st.dataframe(df_display)
    else:
        st.write("尚無數據。")