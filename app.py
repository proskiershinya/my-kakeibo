import streamlit as st
import pandas as pd
from datetime import datetime

# ページ基本設定
st.set_page_config(page_title="お金管理システム", layout="wide")

# スプレッドシートID設定
SHEET_ID = "1bMVc-6f0SdNfpMYJV9pkdFgXhKtm-k6PQe-JdRxDwY0"

# データ読み込み関数
def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return pd.DataFrame()

# パスワード認証
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 ログイン")
    password = st.text_input("パスワードを入力してください", type="password")
    if st.button("ログイン", type="primary"):
        if password == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("パスワードが正しくありません")
    st.stop()

# サイドバー
st.sidebar.title("💰 お金管理システム")
st.sidebar.caption("Google Sheets 連動版")
if st.sidebar.button("ログアウト"):
    st.session_state.authenticated = False
    st.rerun()

# メイン画面のタブ設定
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 日次の残高予測", 
    "✏️ 取引入力＆予定・確定管理", 
    "📋 確定申告まとめ（やよい連動）", 
    "⚙️ マスター設定"
])

# データを事前に読み込み
df_accounts = load_data("accounts")
df_cards = load_data("cards")
df_jobs = load_data("jobs")
df_transactions = load_data("transactions")

# ----------------------------------------------------
# タブ1: 日次の残高予測
# ----------------------------------------------------
with tab1:
    st.header("📊 日次の残高予測")
    st.caption("登録済みの口座情報および取引データをもとに残高予測を表示します。")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏦 現在の登録口座一覧")
        st.dataframe(df_accounts, use_container_width=True)
    with col2:
        st.subheader("💳 登録カード一覧")
        st.dataframe(df_cards, use_container_width=True)

# ----------------------------------------------------
# タブ2: 取引入力＆予定・確定管理
# ----------------------------------------------------
with tab2:
    st.header("✏️ 取引（入出金・予定）の入力")
    
    account_options = df_accounts["口座名"].dropna().tolist() if not df_accounts.empty and "口座名" in df_accounts.columns else ["現金", "銀行口座"]
    card_options = df_cards["カード名"].dropna().tolist() if not df_cards.empty and "カード名" in df_cards.columns else ["なし"]
    
    with st.form("transaction_form", clear_on_submit=True):
        st.subheader("📝 新規取引の追加")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            tx_date = st.date_input("日付", value=datetime.today())
            tx_type = st.selectbox("区分", ["支出", "収入", "振替"])
            tx_category = st.text_input("勘定科目 / 項目（例: 旅費交通費, 売上）")
            
        with c2:
            tx_amount = st.number_input("金額（円）", min_value=0, step=1000)
            tx_account = st.selectbox("利用口座 / 振込先", account_options)
            tx_card = st.selectbox("使用カード（カード決済の場合）", ["指定なし"] + card_options)
            
        with c3:
            tx_status = st.selectbox("ステータス", ["予定", "確定"])
            tx_memo = st.text_area("メモ・詳細", placeholder="摘要や取引内容を入力")
            
        submitted_tx = st.form_submit_button("取引を記録する", type="primary")
        if submitted_tx:
            st.success("取引データを受け付けました！（※スプレッドシートへの直接追加機能は準備中）")

    st.markdown("---")
    st.subheader("📋 登録済み取引履歴 (transactions)")
    st.dataframe(df_transactions, use_container_width=True)

# ----------------------------------------------------
# タブ3: 確定申告まとめ（やよい連動）
# ----------------------------------------------------
with tab3:
    st.header("📋 確定申告まとめ（やよいの青色申告 連動）")
    st.info("確定データの集計結果および弥生会計インポート用インポートデータの出力画面です。")
    if not df_transactions.empty:
        st.dataframe(df_transactions, use_container_width=True)
    else:
        st.warning("現在表示できる確定取引データがありません。")

# ----------------------------------------------------
# タブ4: マスター設定
# ----------------------------------------------------
with tab4:
    st.header("⚙️ マスター設定（口座・カード・収入元）")
    st.caption("ここで登録・編集した設定情報がアプリ全体の計算・選択肢に使用されます。")
    
    st.subheader("1. 口座マスター設定")
    with st.form("account_form", clear_on_submit=True):
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            new_acc_name = st.text_input("口座名", placeholder="例: 東邦銀行, 楽天銀行")
        with col_a2:
            new_acc_date = st.date_input("開始日", value=datetime.today())
        with col_a3:
            new_acc_bal = st.number_input("初期残高（円）", value=0, step=10000)
            
        submit_acc = st.form_submit_button("口座を追加")
        if submit_acc:
            if new_acc_name:
                st.success(f"口座「{new_acc_name}」を入力しました。")
            else:
                st.error("口座名を入力してください。")

    st.write("**現在の口座マスターデータ (accounts)**")
    st.dataframe(df_accounts, use_container_width=True)

    st.markdown("---")
    st.subheader("2. クレジットカードマスター設定")
    with st.form("card_form", clear_on_submit=True):
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
        with col_c1:
            new_card_name = st.text_input("カード名", placeholder="例: 楽天カード")
        with col_c2:
            new_card_close = st.number_input("締め日（1〜31）", min_value=1, max_value=31, value=15)
        with col_c3:
            new_card_pay_acc = st.selectbox("引き落とし口座", account_options)
        with col_c4:
            new_card_pay_day = st.number_input("引き落とし日（1〜31）", min_value=1, max_value=31, value=10)
            
        submit_card = st.form_submit_button("カードを追加")
        if submit_card:
            if new_card_name:
                st.success(f"カード「{new_card_name}」を入力しました。")
            else:
                st.error("カード名を入力してください。")

    st.write("**現在のカードマスターデータ (cards)**")
    st.dataframe(df_cards, use_container_width=True)

    st.markdown("---")
    st.subheader("3. 収入元・バイト先マスター設定")
    with st.form("job_form", clear_on_submit=True):
        col_j1, col_j2, col_j3, col_j4 = st.columns(4)
        with col_j1:
            new_job_name = st.text_input("収入元・バイト先名称", placeholder="例: テレアポ, スキー場")
        with col_j2:
            new_job_close = st.number_input("締め日（日）", min_value=1, max_value=31, value=30)
        with col_j3:
            new_job_pay_day = st.number_input("給与支給日（日）", min_value=1, max_value=31, value=25)
        with col_j4:
            new_job_wage = st.number_input("時給・単価（円）", value=1000, step=50)
            
        submit_job = st.form_submit_button("収入元を追加")
        if submit_job:
            if new_job_name:
                st.success(f"収入元「{new_job_name}」を入力しました。")
            else:
                st.error("収入元名称を入力してください。")

    st.write("**現在のバイト先マスターデータ (jobs)**")
    st.dataframe(df_jobs, use_container_width=True)
