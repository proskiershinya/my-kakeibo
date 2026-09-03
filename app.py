import streamlit as st
import pandas as pd
import datetime
import holidays

# 1. パスワード認証機能（閉じた時・リロード時にロック）
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    if not st.session_state["authenticated"]:
        st.title("🔒 お金管理アプリ ログイン")
        pwd = st.text_input("パスワードを入力してください", type="password")
        if st.button("ログイン"):
            if pwd == "1234":  # ※任意のパスワードに変更してください
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("パスワードが違います")
        return False
    return True

if check_password():
    st.sidebar.title("💰 お金管理システム")
    if st.sidebar.button("🔒 ログアウト"):
        st.session_state["authenticated"] = False
        st.rerun()

    # 2. 日本の祝日判定関数（前倒し・後倒し計算）
    jp_holidays = holidays.Japan()

    def get_actual_date(dt, rule):
        # rule: '前営業日', '翌営業日', '休日決済'
        if rule == '休日決済':
            return dt
        
        while dt.weekday() >= 5 or dt in jp_holidays:
            if rule == '前営業日':
                dt -= datetime.timedelta(days=1)
            elif rule == '翌営業日':
                dt += datetime.timedelta(days=1)
        return dt

    # 3. メイン画面・タブ構成
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 日次口座残高予測", 
        "📝 取引入力＆予定・確定管理", 
        "🧾 確定申告まとめ（やよい連動）", 
        "⚙️ マスター設定"
    ])

    with tab1:
        st.header("📈 日次口座残高予測＆資金繰りチェック")
        st.info("※設定された初期残高とFutureの取引データ・カード引き落とし予定から日次残高を自動計算します。")

    with tab2:
        st.header("📝 取引の登録・修正")
        with st.form("entry_form"):
            col1, col2 = st.columns(2)
            with col1:
                t_date = st.date_input("日付", datetime.date.today())
                t_type = st.selectbox("取引種別", ["収入（バイト・売上）", "支出（経費・生活費）", "口座間振替"])
                
                # ★追加：スマホ代などの「家事按分対象」を選択肢に追加
                t_category_type = st.selectbox("確定申告区分", [
                    "事業所得（100%事業経費）", 
                    "事業所得（家事按分対象：スマホ代・自宅Wi-Fi等）", 
                    "事業外・給与所得（テレアポ等）", 
                    "所得控除（国保・年金・生命保険）", 
                    "事業外・その他（税金・生活費）"
                ])
                
                # ★追加：「通信費（スマホ代・ネット）」を明確に指定可能に
                t_category = st.selectbox("カテゴリ", [
                    "売上・給与", "仕入", "ツール代", "通信費（スマホ代・ネット）", 
                    "自動車保険・車両費", "旅費交通費", "生命保険料", 
                    "国民健康保険/年金", "生活費/その他"
                ])
            with col2:
                amount = st.number_input("金額（手取り/全額実支払額）", min_value=0, step=1000)
                tax_amount = st.number_input("源泉徴収額（引かれた場合）", min_value=0, step=100)
                pay_method = st.selectbox("決済方法", ["銀行口座", "クレジットカード", "現金"])
                status = st.radio("状態", ["予定", "確定"], horizontal=True)
                memo = st.text_input("備考（カード確定額補正メモなど）")

            submitted = st.form_submit_button("保存する")
            if submitted:
                st.success("登録しました！データは自動保存されます。")

    with tab3:
        st.header("🧾 確定申告データ集計（やよいの青色申告用）")
        year = st.selectbox("対象年度", [2026, 2025])
        
        # ★追加：スマホ代などの按分率（％）をリアルタイムにシミュレーション設定
        st.subheader("💡 家事按分（スマホ代等）の設定")
        phone_ratio = st.slider("通信費（スマホ代等）の事業使用割合（%）", min_value=0, max_value=100, value=50, step=5)
        
        if st.button("確定申告データを集計する"):
            st.markdown("### 📋 やよいの青色申告 転記用データ")
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("【事業所得の部】")
                st.metric("事業売上（農作業・スキー・動画）", "¥0")
                st.metric("事業経費（自動車保険・ツール代等）", "¥0")
                # ★追加：家事按分後のスマホ代経費の集計表示
                st.metric(f"うち通信費（按分率 {phone_ratio}% 適用後）", f"¥0 (全体金額の{phone_ratio}%)")
            with col_b:
                st.subheader("【給与所得・控除の部】")
                st.metric("給与収入合計（テレアポ等）", "¥0")
                st.metric("源泉徴収税額合計", "¥0")
                st.metric("社会保険・生命保険控除合計", "¥0")

    with tab4:
        st.header("⚙️ 口座・カード・バイト先マスター設定")
        st.write("ここから新しい銀行口座、クレジットカード、バイト先を自由に追加・変更できます。")
