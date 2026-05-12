import streamlit as st
import random
import json

#页面设置
st.set_page_config(page_title="Arknights随机挑战", page_icon="🔮")
#注入 PWA 所需标签
st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/sw.js').then(function(registration) {
        console.log('ServiceWorker 注册成功');
      }, function(err) {
        console.log('ServiceWorker 注册失败: ', err);
      });
    });
  }
</script>
""", unsafe_allow_html=True)
#背景图
st.markdown("""
<style>
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url("data:image/svg+xml,..."); /* 噪点 SVG 或半透明 png */
    opacity: 0.15;
    pointer-events: none;
}
/* 全页面背景 */
.stApp {
    background-image: url("https://i.imgur.com/OdKqON4.jpeg") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}
/* 内容卡片半透明背景 */
.main .block-container {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 15px;
    padding: 2rem 2rem;
    margin-top: 1rem;
}
/* 卡片悬停动画 */
.result-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.result-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.4) !important;
}
</style>
""", unsafe_allow_html=True)
st.title("🔮 Arknights随机挑战")

st.markdown("""
<div style="
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    border-radius: 12px;
    padding: 8px 20px;
    margin-bottom: 20px;
    text-align: center;
    color: white;
    font-size: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
">
    ⚔ 唤醒你的大脑，拒绝维什戴尔 ⚔
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
:root {
    --primary-color: #ffb300;       /* 金色/琥珀 */
    --background-color: #0d1117;    /* 深色底 */
    --secondary-background-color: #161b22;
    --text-color: #e6edf3;
}
/* 按钮重绘 */
.stButton > button {
    background-color: var(--primary-color) !important;
    color: #000 !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    border: none !important;
}
/* 卡片底色统一 */
.stExpander, .stTextInput, .stNumberInput {
    background: rgba(255,255,255,0.05) !important;
}
</style>
""", unsafe_allow_html=True)

#挑战词条库
DEFAULT_WORDS = [
    "使用6个先锋和重装干员无漏挑战7-18",
    "使用6个先锋和重装干员无漏挑战9-19",
    "使用6个先锋和重装干员无漏挑战11-20",
    "使用6个先锋和重装干员无漏挑战13-21",
    "使用6个先锋和重装干员无漏挑战h9-6",
    "使用6个先锋和重装干员无漏挑战h7-4",
    "使用6个特种干员无漏挑战7-18",
    "使用6个特种干员无漏挑战9-19",
    "使用6个特种干员无漏挑战11-20",
    "使用6个特种干员无漏挑战13-21",
    "使用6个特种干员挑战h9-6",
    "使用6个特种干员无漏挑战h7-4",
    "使用6个医疗和辅助干员无漏挑战7-18",
    "使用6个医疗和辅助干员无漏挑战9-19",
    "使用6个医疗和辅助干员无漏挑战11-20",
    "使用6个医疗和辅助干员无漏挑战h9-6",
    "使用6个医疗和辅助干员无漏挑战h7-4",
    "使用6个近卫干员无漏挑战7-18",
    "使用6个近卫干员无漏挑战9-19",
    "使用6个近卫干员无漏挑战11-20",
    "使用6个近卫干员无漏挑战13-21",
    "使用6个近卫干员挑战h9-6",
    "使用6个近卫干员无漏挑战h7-4",
    "使用6个狙击和术士干员无漏挑战7-18",
    "使用6个狙击和术士干员无漏挑战9-19",
    "使用6个狙击和术士干员无漏挑战11-20",
    "使用6个狙击和术士干员无漏挑战13-21",
    "使用6个狙击和术士干员挑战h9-6",
    "使用6个狙击和术士干员无漏挑战h7-4",
    "特殊-不能使用穿鞋的干员无漏挑战7-18",
    "特殊-不能使用穿鞋的干员无漏挑战9-19",
    "特殊-不能使用穿鞋的干员无漏挑战11-20",
    "特殊-不能使用穿鞋的干员无漏挑战13-21",
    "特殊-不能使用穿鞋的干员挑战h9-6",
    "特殊-不能使用穿鞋的干员无漏挑战h7-4",
    "困难-使用每个职业获得的第一个6星干员组成编队无漏挑战7-18",
    "困难-使用每个职业获得的第一个6星干员组成编队无漏挑战9-19",
    "困难-使用每个职业获得的第一个6星干员组成编队无漏挑战11-20",
    "困难-使用每个职业获得的第一个6星干员组成编队无漏挑战13-21",
    "困难-使用每个职业获得的第一个6星干员组成编队无漏挑战h9-6",
    "困难-使用每个职业获得的第一个6星干员组成编队无漏挑战h7-4",
    "使用粉毛干员无漏挑战7-18",
    "使用粉毛的干员无漏挑战9-19",
    "使用粉毛的干员无漏挑战11-20",
    "使用粉毛的干员无漏挑战13-21",
    "使用粉毛的干员挑战h9-6",
    "使用粉毛的干员无漏挑战h7-4",
    "使用5个白毛干员无漏挑战7-18",
    "使用5个白毛的干员无漏挑战9-19",
    "使用5个白毛的干员无漏挑战11-20",
    "使用5个白毛的干员无漏挑战13-21",
    "使用5个白毛的干员挑战h9-6",
    "使用5个白毛的干员无漏挑战h7-4",
    "使用5个菲林干员无漏挑战7-18",
    "使用5个菲林干员无漏挑战9-19",
    "使用5个菲林干员无漏挑战11-20",
    "使用5个菲林干员无漏挑战13-21",
    "使用5个菲林干员挑战h9-6",
    "使用5个菲林干员无漏挑战h7-4",
    "使用4个限定干员无漏挑战7-18",
    "使用4个限定干员无漏挑战9-19",
    "使用4个限定干员无漏挑战11-20",
    "使用4个限定干员无漏挑战13-21",
    "使用4个限定干员挑战h9-6",
    "使用4个限定干员无漏挑战h7-4",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战7-18",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战9-19",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战11-20",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战13-21",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员挑战h9-6",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战h7-4",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战7-18",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战9-19",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战11-20",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战13-21",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员挑战h9-6",
    "特典-使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战h7-4",
    "特殊-使用4个白丝干员无漏挑战7-18",
    "特殊-使用4个白丝干员无漏挑战9-19",
    "特殊-使用4个白丝干员无漏挑战11-20",
    "特殊-使用4个白丝干员无漏挑战13-21",
    "特殊-使用4个白丝干员挑战h9-6",
    "特殊-使用4个白丝干员无漏挑战h7-4",
    "特殊-使用4个黑丝干员无漏挑战7-18",
    "特殊-使用4个黑丝干员无漏挑战9-19",
    "特殊-使用4个黑丝干员无漏挑战11-20",
    "特殊-使用4个黑丝干员无漏挑战13-21",
    "特殊-使用4个黑丝干员挑战h9-6",
    "特殊-使用4个黑丝干员无漏挑战h7-4",
    "特殊-使用4个光腿干员无漏挑战7-18",
    "特殊-使用4个光腿干员无漏挑战9-19",
    "特殊-使用4个光腿干员无漏挑战11-20",
    "特殊-使用4个光腿干员无漏挑战13-21",
    "特殊-使用4个光腿干员挑战h9-6",
    "特殊-使用4个光腿干员无漏挑战h7-4",
    "使用4个男性干员无漏挑战7-18",
    "使用4个男性干员无漏挑战9-19",
    "使用4个男性干员无漏挑战11-20",
    "使用4个男性干员无漏挑战13-21",
    "使用4个男性干员挑战h9-6",
    "使用4个男性干员无漏挑战h7-4",
    "使用4个白色系干员无漏挑战7-18",
    "使用4个白色系干员无漏挑战9-19",
    "使用4个白色系干员无漏挑战11-20",
    "使用4个白色系干员无漏挑战13-21",
    "使用4个白色系干员挑战h9-6",
    "使用4个白色系干员无漏挑战h7-4",
    "使用4个蓝色系干员无漏挑战7-18",
    "使用4个蓝色系干员无漏挑战9-19",
    "使用4个蓝色系干员无漏挑战11-20",
    "使用4个蓝色系干员无漏挑战13-21",
    "使用4个蓝色系干员挑战h9-6",
    "使用4个蓝色系干员无漏挑战h7-4",
    "使用4个红色系干员无漏挑战7-18",
    "使用4个红色系干员无漏挑战9-19",
    "使用4个红色系干员无漏挑战11-20",
    "使用4个红色系干员无漏挑战13-21",
    "使用4个红色系干员挑战h9-6",
    "使用4个红色系干员无漏挑战h7-4",
    "使用4个黄色系干员无漏挑战7-18",
    "使用4个黄色系干员无漏挑战9-19",
    "使用4个黄色系干员无漏挑战11-20",
    "使用4个黄色系干员无漏挑战13-21",
    "使用4个黄色系干员挑战h9-6",
    "使用4个黄色系干员无漏挑战h7-4",
    "仅使用2024年4月前（维什戴尔之前）的干员无漏挑战7-18",
    "仅使用2024年4月前（维什戴尔之前）的干员无漏挑战9-19",
    "仅使用2024年4月前（维什戴尔之前）的干员无漏挑战11-20",
    "仅使用2024年4月前（维什戴尔之前）的干员无漏挑战13-21",
    "仅使用2024年4月前（维什戴尔之前）的干员无漏挑战h9-6",
    "仅使用2024年4月前（维什戴尔之前）的干员无漏挑战h7-4",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战7-18",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战9-19",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战11-20",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战13-21",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战h9-6",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战h7-4",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战7-18",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战9-19",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战11-20",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战13-21",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战h9-6",
    "困难-仅使用2022年9月前（玛恩纳之前）的干员无漏挑战h7-4",
    "特殊-使用4个白丝干员无漏挑战7-18",
    "特殊-使用4个白丝干员无漏挑战9-19",
    "特殊-使用4个白丝干员无漏挑战11-20",
    "特殊-使用4个白丝干员无漏挑战13-21",
    "特殊-使用4个白丝干员挑战h9-6",
    "特殊-使用4个白丝干员无漏挑战h7-4",
    "特殊-使用4个黑丝干员无漏挑战7-18",
    "特殊-使用4个黑丝干员无漏挑战9-19",
    "特殊-使用4个黑丝干员无漏挑战11-20",
    "特殊-使用4个黑丝干员无漏挑战13-21",
    "特殊-使用4个黑丝干员挑战h9-6",
    "特殊-使用4个黑丝干员无漏挑战h7-4",
    "特殊-使用4个光腿干员无漏挑战7-18",
    "特殊-使用4个光腿干员无漏挑战9-19",
    "特殊-使用4个光腿干员无漏挑战11-20",
    "特殊-使用4个光腿干员无漏挑战13-21",
    "特殊-使用4个光腿干员挑战h9-6",
    "特殊-使用4个光腿干员无漏挑战h7-4",
    "特殊-不能使用穿鞋的干员无漏挑战7-18",
    "特殊-不能使用穿鞋的干员无漏挑战9-19",
    "特殊-不能使用穿鞋的干员无漏挑战11-20",
    "特殊-不能使用穿鞋的干员无漏挑战13-21",
    "特殊-不能使用穿鞋的干员挑战h9-6",
    "特殊-不能使用穿鞋的干员无漏挑战h7-4",

]

if "words" not in st.session_state:
    st.session_state.words = DEFAULT_WORDS.copy()
if "history" not in st.session_state:
    st.session_state.history = []  # 保存最近几次抽取的词条列表

#侧边栏：词库管理
with st.sidebar:
    st.header("📚 词库管理")

    # 1. 上传 JSON 文件（字符串列表）
    uploaded_file = st.file_uploader("上传词库 JSON 文件", type=["json"])
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            if isinstance(data, list) and all(isinstance(item, str) for item in data):
                st.session_state.words = data
                st.success(f"已导入 {len(data)} 个词条")
            else:
                st.error("JSON 格式错误：需要是一个由字符串组成的列表，例如 [\"词条1\", \"词条2\"]")
        except Exception as e:
            st.error(f"读取失败：{e}")

    # 2. 粘贴 JSON 文本
    with st.expander("或直接粘贴 JSON 文本"):
        json_text = st.text_area("词条列表，格式：[\"词条1\", \"词条2\", ...]", height=120)
        if st.button("导入粘贴的文本"):
            try:
                data = json.loads(json_text)
                if isinstance(data, list) and all(isinstance(item, str) for item in data):
                    st.session_state.words = data
                    st.success(f"已导入 {len(data)} 个词条")
                else:
                    st.error("格式错误：需要是字符串列表")
            except Exception as e:
                st.error(f"解析失败：{e}")

    # 3. 手动添加单个词条
    with st.expander("✏️ 手动添加词条"):
        with st.form("add_word"):
            new_word = st.text_input("新词条内容")
            submitted = st.form_submit_button("添加")
            if submitted and new_word:
                st.session_state.words.append(new_word)
                st.success(f"已添加：{new_word}")


    # 4. 重置为默认词库
    if st.button("🔄 重置为默认词库"):
        st.session_state.words = DEFAULT_WORDS.copy()
        st.success("已重置")

# ------------------------ 主界面：抽取区 ------------------------
st.header("🎲 随机抽取词条")

# 抽取数量
draw_count = st.number_input("你想抽取几次？", min_value=1, max_value=6, value=1)

# 抽取按钮
if st.button("✨ 随机抽取", type="primary", use_container_width=True):
    if draw_count > len(st.session_state.words):
        st.warning(f"词库只有 {len(st.session_state.words)} 个词条，已全部展示。")
        result = st.session_state.words.copy()
    else:
        result = random.sample(st.session_state.words, draw_count)

    # 保存到历史
    st.session_state.history.append(result)
    if len(st.session_state.history) > 10:
        st.session_state.history.pop(0)

    # ------------------------ 卡片式展示 ------------------------
    st.subheader("📋请选择一个作为本次挑战")

    # 每张卡片的样式
    for i, word in enumerate(result, 1):
        # 动态边框颜色
        if "困难" in word:
            border_color = "#e74c3c"
        elif "特殊" in word:
            border_color = "#f1c40f"
        elif "特典" in word:
            border_color = "#e67e22"
        else:
            border_color = "#3498db"

        st.markdown(f"""
        <div class="result-card" style="
            background: linear-gradient(135deg, #434343 0%, #1a1a1a 100%);
            border-radius: 15px;
            padding: 14px 16px;
            margin-bottom: 10px;
            color: #ffffff;
            font-size: 18px;
            font-weight: 500;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border-left: 6px solid {border_color};
        ">
            <span style="opacity:0.7;">词条 {i}</span>&nbsp;&nbsp;{word}
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📜 最近抽取记录"):
        if not st.session_state.history:
            st.write("暂无记录")
        else:
            for idx, draw in enumerate(reversed(st.session_state.history), 1):
                # 每条记录一张小卡片
                words_formatted = "、".join(draw)
                st.markdown(f"""
                <div class="result-card" style="
                    background: #f8f9fa;
                    border-radius: 8px;
                    padding: 10px 14px;
                    margin-bottom: 8px;
                    border-left: 4px solid #2a5298;
                    font-size: 15px;
                ">
                    <b>第 {idx} 次</b> · {words_formatted}
                </div>
                """, unsafe_allow_html=True)


#历史记录
with st.expander("📜 最近抽取记录"):
    if not st.session_state.history:
        st.write("暂无记录")
    else:
        for idx, draw in enumerate(reversed(st.session_state.history), 1):
            st.caption(f"第 {idx} 次：")
            st.write("、".join(draw))