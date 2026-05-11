import streamlit as st
import random
import json

#页面设置
st.set_page_config(page_title="明日方舟 · 挑战词条抽取", page_icon="🎲")
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
/* 整个页面背景使用本地图片 */
.stApp {
    background-image: url("/app/static/bg.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* 内容区半透明白底，提升可读性 */
.main .block-container {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 15px;
    padding: 2rem 2rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)


st.title("🎲 明日方舟 · 随机挑战")

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
    "使用6个特种干员无漏挑战h9-6",
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
    "使用6个近卫干员无漏挑战h9-6",
    "使用6个近卫干员无漏挑战h7-4",
    "使用6个狙击和术士干员无漏挑战7-18",
    "使用6个狙击和术士干员无漏挑战9-19",
    "使用6个狙击和术士干员无漏挑战11-20",
    "使用6个狙击和术士干员无漏挑战13-21",
    "使用6个狙击和术士干员无漏挑战h9-6",
    "使用6个狙击和术士干员无漏挑战h7-4",
    "使用不穿鞋的干员无漏挑战7-18",
    "使用不穿鞋的干员无漏挑战9-19",
    "使用不穿鞋的干员无漏挑战11-20",
    "使用不穿鞋的干员无漏挑战13-21",
    "使用不穿鞋的干员无漏挑战h9-6",
    "使用不穿鞋的干员无漏挑战h7-4",
    "使用每个职业获得的第一个6星干员组成编队无漏挑战7-18",
    "使用每个职业获得的第一个6星干员组成编队无漏挑战9-19",
    "使用每个职业获得的第一个6星干员组成编队无漏挑战11-20",
    "使用每个职业获得的第一个6星干员组成编队无漏挑战13-21",
    "使用每个职业获得的第一个6星干员组成编队无漏挑战h9-6",
    "使用每个职业获得的第一个6星干员组成编队无漏挑战h7-4",
    "使用粉毛干员无漏挑战7-18",
    "使用粉毛的干员无漏挑战9-19",
    "使用粉毛的干员无漏挑战11-20",
    "使用粉毛的干员无漏挑战13-21",
    "使用粉毛的干员无漏挑战h9-6",
    "使用粉毛的干员无漏挑战h7-4",
    "使用6个白毛干员无漏挑战7-18",
    "使用6个白毛的干员无漏挑战9-19",
    "使用6个白毛的干员无漏挑战11-20",
    "使用6个白毛的干员无漏挑战13-21",
    "使用6个白毛的干员无漏挑战h9-6",
    "使用6个白毛的干员无漏挑战h7-4",
    "使用6个菲林干员无漏挑战7-18",
    "使用6个菲林干员无漏挑战9-19",
    "使用6个菲林干员无漏挑战11-20",
    "使用6个菲林干员无漏挑战13-21",
    "使用6个菲林干员无漏挑战h9-6",
    "使用6个菲林干员无漏挑战h7-4",
    "使用4个限定干员无漏挑战7-18",
    "使用4个限定干员无漏挑战9-19",
    "使用4个限定干员无漏挑战11-20",
    "使用4个限定干员无漏挑战13-21",
    "使用4个限定干员无漏挑战h9-6",
    "使用4个限定干员无漏挑战h7-4",
    "使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战7-18",
    "使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战9-19",
    "使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战11-20",
    "使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战13-21",
    "使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战h9-6",
    "使用阿米娅和box内第20，19，12，23一共五位干员无漏挑战h7-4",
    "使用5个白色袜子干员无漏挑战7-18",
    "使用5个白色袜子干员无漏挑战9-19",
    "使用5个白色袜子干员无漏挑战11-20",
    "使用5个白色袜子干员无漏挑战13-21",
    "使用5个白色袜子干员无漏挑战h9-6",
    "使用5个白色袜子干员无漏挑战h7-4",
    "使用5个黑色袜子干员无漏挑战7-18",
    "使用5个黑色袜子干员无漏挑战9-19",
    "使用5个黑色袜子干员无漏挑战11-20",
    "使用5个黑色袜子干员无漏挑战13-21",
    "使用5个黑色袜子干员无漏挑战h9-6",
    "使用5个黑色袜子干员无漏挑战h7-4",
    "使用5个光腿干员无漏挑战7-18",
    "使用5个光腿干员无漏挑战9-19",
    "使用5个光腿干员无漏挑战11-20",
    "使用5个光腿干员无漏挑战13-21",
    "使用5个光腿干员无漏挑战h9-6",
    "使用5个光腿干员无漏挑战h7-4",
    "使用5个男性干员无漏挑战7-18",
    "使用5个男性干员无漏挑战9-19",
    "使用5个男性干员无漏挑战11-20",
    "使用5个男性干员无漏挑战13-21",
    "使用5个男性干员无漏挑战h9-6",
    "使用5个男性干员无漏挑战h7-4",
    "使用4个白色系干员无漏挑战7-18",
    "使用4个白色系干员无漏挑战9-19",
    "使用4个白色系干员无漏挑战11-20",
    "使用4个白色系干员无漏挑战13-21",
    "使用4个白色系干员无漏挑战h9-6",
    "使用4个白色系干员无漏挑战h7-4",
    "使用4个蓝色系干员无漏挑战7-18",
    "使用4个蓝色系干员无漏挑战9-19",
    "使用4个蓝色系干员无漏挑战11-20",
    "使用4个蓝色系干员无漏挑战13-21",
    "使用4个蓝色系干员无漏挑战h9-6",
    "使用4个蓝色系干员无漏挑战h7-4",
    "使用4个红色系干员无漏挑战7-18",
    "使用4个红色系干员无漏挑战9-19",
    "使用4个红色系干员无漏挑战11-20",
    "使用4个红色系干员无漏挑战13-21",
    "使用4个红色系干员无漏挑战h9-6",
    "使用4个红色系干员无漏挑战h7-4",
    "使用4个黄色系干员无漏挑战7-18",
    "使用4个黄色系干员无漏挑战9-19",
    "使用4个黄色系干员无漏挑战11-20",
    "使用4个黄色系干员无漏挑战13-21",
    "使用4个黄色系干员无漏挑战h9-6",
    "使用4个黄色系干员无漏挑战h7-4",
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
st.header("🎯 随机抽取词条")

# 抽取数量
draw_count = st.number_input("抽取几次？", min_value=1, max_value=3, value=1)

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

    # 展示结果
    st.subheader("📋 请选择一个进行挑战")
    for i, word in enumerate(result, 1):
        st.markdown(f"**{i}.** {word}")

#历史记录
with st.expander("📜 最近抽取记录"):
    if not st.session_state.history:
        st.write("暂无记录")
    else:
        for idx, draw in enumerate(reversed(st.session_state.history), 1):
            st.caption(f"第 {idx} 次：")
            st.write("、".join(draw))