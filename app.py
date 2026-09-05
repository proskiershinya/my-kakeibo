import streamlit as st
import pandas as pd

# ページ設定
st.set_page_config(page_title="お金管理システム", layout="wide")

# スプレッドシートID
SHEET_ID = "1bMVc-6f0SdNfpMYJV9pkdFgXhKtm-k6PQe-JdRxDwY0"

# データ読み込み関数
def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# パスワード認証
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 ログイン")
    password = st.text_input("パスワードを入力してください", type="password")
    if st.button("ログイン"):
        if password == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("パスワードが違います")
    st.stop()

# サイドバー
st.sidebar.title("💰 お金管理")
if st.sidebar.button("ログアウト"):
    st.session_state.authenticated = False
    st.rerun()

# メインコンテンツ
st.title("お金管理システム")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 日次の残高予測", 
    "✏️ 取引入力＆予定・確定管理", 
    "📋 確定申告まとめ（やよい連動）", 
    "⚙️ マスター設定"
])

with tab1:
    st.header("日次残高予測")
    st.info("データ連携の準備中です")

with tab2:
    st.header("取引入力＆管理")
    st.info("データ連携の準備中です")

with tab3:
    st.header("確定申告まとめ")
    st.info("データ連携の準備中です")

with tab4:
    st.header("⚙️ 口座・カード・バイト先マスター設定")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏦 口座設定")
        acc_name = st.text_input("口座名（例: 東邦銀行）")
        acc_bal = st.number_input("初期残高（円）", value=0)
        if st.button("口座を追加"):
            st.success(f"{acc_name} を追加しました（※スプレッドシート反映準備中）")

    with col2:
        st.subheader("💳 カード設定")
        card_name = st.text_input("カード名（例: 楽天カード）")
        card_close = st.number_input("締め日", min_value=1, max_value=31, value=15)
        card_pay = st.number_input("引き落とし日", min_value=1, max_value=31, value=10)
        if st.button("カードを追加"):
            st.success(f"{card_name} を追加しました（※スプレッドシート反映準備中）")

    with col3:
        st.subheader("💼 バイト先設定")
        job_name = st.text_input("バイト先名")
        job_wage = st.number_input("時給（円）", value=1000)
        if st.button("バイト先を追加"):
            st.success(f"{job_name} を追加しました（※スプレッドシート反映準備中）")

    st.markdown("---")
    st.subheader("現在の登録データ（スプレッドシート取得結果）")
    
    st.write("**【口座マスター】**")
    st.dataframe(load_data("accounts"), use_container_width=True)
    
    st.write("**【カードマスター】**")
    st.dataframe(load_data("cards"), use_container_width=True)
    
    st.write("**【バイト先マスター】**")
    st.dataframe(load_data("jobs"), use_container_width=True)
