import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime, timedelta

# --- ページ設定 ---
st.set_page_config(layout="wide", page_title="商品・在庫管理システム")

# 安全に数値を取得するための関数
def safe_int(value):
    if isinstance(value, bytes):
        return int.from_bytes(value, 'little')
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

# --- データベース初期化 ---
def init_db():
    conn = sqlite3.connect('inventory_management.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS m_tags (id INTEGER PRIMARY KEY AUTOINCREMENT, tag_name TEXT NOT NULL UNIQUE, sort_order INTEGER DEFAULT 0)')
    # current_stock (在庫数) カラムを追加した状態でテーブル作成
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER,
            quantity INTEGER,
            current_stock INTEGER,
            expiration_date TEXT,
            tag TEXT,
            memo TEXT
        )
    ''')

    # 既存のデータベースがある場合、current_stockカラムがなければ追加する（マイグレーション）
    try:
        c.execute('SELECT current_stock FROM products LIMIT 1')
    except sqlite3.OperationalError:
        c.execute('ALTER TABLE products ADD COLUMN current_stock INTEGER')
        c.execute('UPDATE products SET current_stock = quantity')
        conn.commit()

    conn.commit()
    return conn

# タグ追加用のコールバック
def add_tag_callback():
    new_tag_name = st.session_state.tag_input_field
    if new_tag_name:
        conn = sqlite3.connect('inventory_management.db')
        c = conn.cursor()
        try:
            res = c.execute('SELECT MAX(sort_order) FROM m_tags').fetchone()[0]
            max_order = safe_int(res) if res is not None else 0
            c.execute('INSERT INTO m_tags (tag_name, sort_order) VALUES (?, ?)', (new_tag_name, max_order + 1))
            conn.commit()
            st.session_state.tag_input_field = ""
        except sqlite3.IntegrityError:
            st.error("そのタグは既に登録されています")
        finally:
            conn.close()

# 期限と在庫の状態に応じた色付け
def highlight_status(row):
    # 在庫切れ（赤系）
    if safe_int(row['在庫数']) <= 0:
        return ['background-color: #fce4ec; color: #c2185b; font-style: italic;'] * len(row)

    try:
        expiry = datetime.strptime(row['賞味期限'], '%Y-%m-%d').date()
        today = date.today()
        # 期限切れ
        if expiry < today:
            return ['background-color: #d9534f; color: white; font-weight: bold;'] * len(row)
        # 期限間近（7日以内）
        elif expiry <= today + timedelta(days=7):
            return ['background-color: #f0ad4e; color: black; font-weight: bold;'] * len(row)
    except:
        pass
    return [''] * len(row)

# 編集用ダイアログ
@st.dialog("データを編集")
def edit_dialog(row_data, tag_options):
    st.write(f"「{row_data['商品名']}」の情報を修正します")
    with st.form("edit_form"):
        new_name = st.text_input("商品名", value=row_data["商品名"])
        c1, c2 = st.columns(2)
        with c1:
            new_price = st.number_input("金額 (合計/円)", min_value=0, value=safe_int(row_data["金額"]), step=10)
            new_qty = st.number_input("入荷総数", min_value=1, value=safe_int(row_data["入荷数"]), step=1)
            new_stock = st.number_input("現在の在庫数", min_value=0, max_value=new_qty, value=safe_int(row_data["在庫数"]), step=1)
        with c2:
            current_tag = row_data["タグ"]
            tag_idx = tag_options.index(current_tag) if current_tag in tag_options else 0
            new_tag = st.selectbox("タグ", tag_options, index=tag_idx)
            new_expiry = st.date_input("賞味期限", value=datetime.strptime(row_data["賞味期限"], '%Y-%m-%d').date())
        new_memo = st.text_area("備考", value=row_data["備考"])

        if st.form_submit_button("保存する", type="primary"):
            conn_edit = sqlite3.connect('inventory_management.db')
            c_edit = conn_edit.cursor()
            c_edit.execute('UPDATE products SET name=?, price=?, quantity=?, current_stock=?, expiration_date=?, tag=?, memo=? WHERE id=?',
                      (new_name, safe_int(new_price), safe_int(new_qty), safe_int(new_stock), str(new_expiry), new_tag, new_memo, safe_int(row_data["id"])))
            conn_edit.commit()
            conn_edit.close()
            st.rerun()

conn = init_db()
tags_df = pd.read_sql_query('SELECT id, tag_name, sort_order FROM m_tags ORDER BY sort_order ASC', conn)
tag_options = tags_df['tag_name'].tolist()

# --- サイドバー：タグ管理 ---
with st.sidebar:
    st.header("🏷️ タグ管理")
    with st.expander("新しいタグを追加", expanded=True):
        st.text_input("タグ名", key="tag_input_field")
        st.button("追加", use_container_width=True, on_click=add_tag_callback)

    if not tags_df.empty:
        st.divider()
        selected_tag = st.selectbox("対象のタグ", tag_options)
        c_up, c_down, c_del = st.columns(3)
        idx = tag_options.index(selected_tag)

        with c_up:
            if st.button("⬆️", use_container_width=True) and idx > 0:
                t_id, t_order = safe_int(tags_df.iloc[idx]['id']), safe_int(tags_df.iloc[idx]['sort_order'])
                u_id, u_order = safe_int(tags_df.iloc[idx-1]['id']), safe_int(tags_df.iloc[idx-1]['sort_order'])
                c = conn.cursor()
                c.execute('UPDATE m_tags SET sort_order = ? WHERE id = ?', (u_order, t_id))
                c.execute('UPDATE m_tags SET sort_order = ? WHERE id = ?', (t_order, u_id))
                conn.commit()
                st.rerun()
        with c_down:
            if st.button("⬇️", use_container_width=True) and idx < len(tag_options) - 1:
                t_id, t_order = safe_int(tags_df.iloc[idx]['id']), safe_int(tags_df.iloc[idx]['sort_order'])
                l_id, l_order = safe_int(tags_df.iloc[idx+1]['id']), safe_int(tags_df.iloc[idx+1]['sort_order'])
                c = conn.cursor()
                c.execute('UPDATE m_tags SET sort_order = ? WHERE id = ?', (l_order, t_id))
                c.execute('UPDATE m_tags SET sort_order = ? WHERE id = ?', (t_order, l_id))
                conn.commit()
                st.rerun()
        with c_del:
            if st.button("🗑️", type="secondary", use_container_width=True):
                c = conn.cursor()
                c.execute('DELETE FROM m_tags WHERE tag_name = ?', (selected_tag,))
                conn.commit()
                st.rerun()

# --- 商品一覧データ取得 ---
df = pd.read_sql_query('SELECT * FROM products ORDER BY id DESC', conn)

st.title("📦 商品管理システム")
col_reg, col_view = st.columns([1, 2.5], gap="large")

with col_reg:
    with st.container(border=True):
        st.subheader("✨ 新規商品登録")
        if not tag_options:
            st.warning("タグを登録してください")
        else:
            with st.form("add_form", clear_on_submit=True):
                name = st.text_input("商品名")
                c1, c2 = st.columns(2)
                with c1:
                    price = st.number_input("金額 (合計/円)", min_value=0, step=10)
                    # 💡 入荷数のデフォルト値を 1 に設定
                    qty = st.number_input("入荷数", min_value=1, step=1, value=1)
                    unit_price_preview = price // qty if qty > 0 else 0
                    st.info(f"単価: {unit_price_preview:,} 円/個")
                with c2:
                    tag = st.selectbox("タグ", tag_options)
                    expiry = st.date_input("賞味期限", value=date.today())
                memo = st.text_area("備考")
                if st.form_submit_button("登録", type="primary", use_container_width=True):
                    if name:
                        c = conn.cursor()
                        # 💡 登録時は 入荷数(quantity) と 在庫数(current_stock) の両方に同じ値をいれる
                        c.execute('INSERT INTO products (name, price, quantity, current_stock, expiration_date, tag, memo) VALUES (?,?,?,?,?,?,?)',
                                  (name, safe_int(price), safe_int(qty), safe_int(qty), str(expiry), tag, memo))
                        conn.commit()
                        st.rerun()

with col_view:
    st.subheader("📋 在庫一覧")
    if not df.empty:
        display_df = df.copy()
        # カラム名の整理
        display_df.columns = ["id", "商品名", "金額", "入荷数", "在庫数", "賞味期限", "タグ", "備考"]
        display_df["単価"] = display_df["金額"] // display_df["入荷数"]

        # 💡 表の表示
        event = st.dataframe(
            display_df.style.apply(highlight_status, axis=1),
            use_container_width=True, hide_index=True, on_select="rerun", selection_mode="multi-row",
            key="main_table",
            column_order=("商品名", "在庫数", "入荷数", "単価", "賞味期限", "タグ", "備考"),
            column_config={
                "金額": st.column_config.NumberColumn("合計金額", format="%d 円"),
                "在庫数": st.column_config.NumberColumn("在庫数", format="%d 個 📦"),
                "入荷数": st.column_config.NumberColumn("入荷数", format="%d"),
                "単価": st.column_config.NumberColumn("単価", format="%d 円/個"),
                "賞味期限": st.column_config.DateColumn("賞味期限", format="YYYY年MM月DD日")
            }
        )

        # 選択行の操作
        selected_rows = st.session_state.main_table.selection.rows
        if selected_rows:
            st.divider()
            b_minus, b_plus, b_edit, b_del = st.columns([1, 1, 1, 1])

            # 1行選択時のみの操作用データ
            if len(selected_rows) == 1:
                selected_data = df.iloc[selected_rows[0]]
                sid = safe_int(selected_data["id"])
                current_s = safe_int(selected_data["current_stock"])

                with b_minus:
                    if st.button("➖ 1つ使う", use_container_width=True, disabled=current_s <= 0):
                        conn.cursor().execute('UPDATE products SET current_stock = ? WHERE id = ?', (max(0, current_s - 1), sid))
                        conn.commit()
                        st.rerun()
                with b_plus:
                    if st.button("➕ 1つ増やす", use_container_width=True):
                        conn.cursor().execute('UPDATE products SET current_stock = ? WHERE id = ?', (current_s + 1, sid))
                        conn.commit()
                        st.rerun()
                with b_edit:
                    if st.button("✏️ 編集", type="primary", use_container_width=True):
                        edit_dialog(display_df.iloc[selected_rows[0]], tag_options)

            with b_del:
                if st.button("🗑️ 削除", type="secondary", use_container_width=True):
                    ids = [safe_int(df.iloc[i]["id"]) for i in selected_rows]
                    c = conn.cursor()
                    c.execute(f"DELETE FROM products WHERE id IN ({','.join(['?']*len(ids))})", ids)
                    conn.commit()
                    st.rerun()
    else:
        st.info("データがありません")

conn.close()
