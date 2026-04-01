import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
import io

# 1. 页面基础配置 (移动端优先：使用手机常用的单列标准布局)
st.set_page_config(page_title="宠物基因身份证", page_icon="🧬", layout="centered")

# 2. 隐藏 Streamlit 默认的右上角菜单和底部水印，让 Demo 看起来更像一个真实的独立产品
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. 准备模拟数据 (使用 pandas 模拟后台数据库)
# 预设两条数据：A1 为完美健康的金毛，B2 为带遗传病风险的法斗
data = {
    "宠物ID": ["G-2026-A1", "G-2026-B2"],
    "品种": ["金毛寻回犬 (Golden Retriever)", "法国斗牛犬 (French Bulldog)"],
    "昵称": ["辛巴", "波霸"],
    "血统纯度": [99.8, 95.5],
    "遗传病筛查": ["【阴性】未检测出已知隐性致病基因", "【阳性】携带软骨发育不良隐性基因 (高风险)"],
    "狂犬疫苗": ["已接种 (有效)", "已接种 (有效)"],
    "检疫证号": ["CN-AQSIQ-2026-A88219", "CN-AQSIQ-2026-B77320"]
}
df_mock_db = pd.DataFrame(data)
df_mock_db.set_index("宠物ID", inplace=True)

# 4. 页面主视觉：居中大标题
st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>中国检验检疫</h3>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>宠物专属数字基因身份证</h2>", unsafe_allow_html=True)

# 5. 交互区：模拟扫码与手动输入
st.markdown("---")
# 调用手机摄像头模拟扫码动作
camera_result = st.camera_input("点击下方按钮模拟扫描宠物吊牌二维码 👇")

# 提供手动输入作为备用演示方案
pet_id_input = st.text_input(
    "或手动输入宠物基因序列号进行查询：", 
    placeholder="例如：G-2026-A1"
).strip().upper()

# 6. 核心逻辑与报告展示区
if pet_id_input:
    # 检查数据库中是否存在该 ID
    if pet_id_input in df_mock_db.index:
        pet_info = df_mock_db.loc[pet_id_input]
        
        st.markdown("### 📑 官方检测报告")
        
        # 模块 A：基础信息 (使用 Markdown 引用框，手机端显示清晰)
        st.markdown(f"""
        > **宠物昵称**：{pet_info['昵称']}  
        > **品种**：{pet_info['品种']}  
        > **基因序列号**：`{pet_id_input}`
        """)
        
        st.write("") # 增加空行留白
        
        # 模块 B：血统纯度 (大号指标 + 进度条)
        purity_val = pet_info['血统纯度']
        st.metric(label="🧬 血统纯度鉴定 (DNA测序)", value=f"{purity_val}%")
        st.progress(purity_val / 100.0)
        
        st.write("")
        
        # 模块 C：健康与检疫 (利用警示色块制造视觉冲击力)
        st.markdown("#### 🏥 遗传病与检疫状态")
        
        # 遗传病动态判断：包含"阳性"字眼则标红警告，否则标绿通过
        if "阳性" in pet_info['遗传病筛查']:
            st.error(f"⚠️ **遗传病筛查**：{pet_info['遗传病筛查']}")
        else:
            st.success(f"✅ **遗传病筛查**：{pet_info['遗传病筛查']}")
            
        st.success(f"💉 **狂犬疫苗状态**：{pet_info['狂犬疫苗']}")
        st.info(f"📜 **官方检疫合格证**：{pet_info['检疫证号']}")
        
        st.markdown("---")
        
        # 模块 D：防伪展示 (动态生成专属二维码)
        st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>官方授权防伪追溯码</p>", unsafe_allow_html=True)
        
        # 组装二维码内容
        qr_data = f"中国检验检疫系统认证\n序列号: {pet_id_input}\n品种: {pet_info['品种']}\n纯度: {purity_val}%"
        
        # 生成二维码图片
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 将 PIL 图片转换为 Streamlit 可渲染的字节流
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        
        # 在页面中央展示二维码，自适应宽度适配手机屏幕
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(buf, use_container_width=True)
            
        st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>长按保存此二维码</p>", unsafe_allow_html=True)
        
    else:
        # 查无此狗时的错误提示
        st.error("❌ 数据库中未查询到该基因序列号，请核对后重试或确认是否为伪造吊牌。")
