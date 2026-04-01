import streamlit as st
#水印1
st.markdown(
    """
    <style>
    .watermark {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
        display: flex;
        flex-wrap: wrap;
        opacity: 0.01;
        transform: rotate(-30deg);
    }

    .watermark span {
        font-size: 60px;
        margin: 60px;
        color: black;
        user-select: none;
    }
    </style>

    <div class="watermark">
        """ + ("<span>ZZF GPA</span>" * 20) + """
    </div>
    """,
    unsafe_allow_html=True
)
#水印2
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        right: 20px;
        font-size: 12px;
        color: rgba(0,0,0,0.5);
    }
    </style>
    <div class="footer">© ZZF | GPA Tool</div>
    """,
    unsafe_allow_html=True
)


st.set_page_config(page_title="绩点计算器", page_icon="📘", layout="centered")
st.title("📘 绩点计算器")

if "courses" not in st.session_state:
    st.session_state.courses = []


def parse_number(value):
    return float(str(value).replace(",", ".").strip())


st.subheader("当前信息")
current_credit = st.text_input("当前总学分", value="0")
current_gpa = st.text_input("当前总绩点", value="0")

# =========================
# 1. 添加新课程并计算最终总绩点
# =========================
st.subheader("添加新课程")
course_name = st.text_input("课程名称", key="course_name")
new_credit = st.text_input("新课程学分", key="new_credit")
new_gpa = st.text_input("新课程绩点", key="new_gpa")

col1, col2 = st.columns(2)

with col1:
    if st.button("添加课程"):
        try:
            credit = parse_number(new_credit)
            gpa = parse_number(new_gpa)

            if credit <= 0:
                st.error("学分必须大于 0")
            elif not (0 <= gpa <= 5):
                st.error("绩点必须在 0 到 5 之间")
            else:
                st.session_state.courses.append({
                    "name": course_name.strip() if course_name.strip() else f"课程{len(st.session_state.courses)+1}",
                    "credit": credit,
                    "gpa": gpa
                })
                st.success("课程已添加")
        except ValueError:
            st.error("请输入有效数字")

with col2:
    if st.button("清空课程"):
        st.session_state.courses = []
        st.success("已清空所有新课程")

st.subheader("已添加课程")

if st.session_state.courses:
    delete_index = None

    for i, course in enumerate(st.session_state.courses):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"{course['name']}：学分 {course['credit']}，绩点 {course['gpa']}")

        with col2:
            if st.button("删除", key=f"delete_{i}"):
                delete_index = i

    if delete_index is not None:
        st.session_state.courses.pop(delete_index)
        st.rerun()
else:
    st.info("暂无已添加课程")

st.subheader("计算最终总绩点")
if st.button("计算总绩点"):
    try:
        current_credit_num = parse_number(current_credit)
        current_gpa_num = parse_number(current_gpa)

        if current_credit_num < 0:
            st.error("当前总学分不能小于 0")
        elif not (0 <= current_gpa_num <= 5):
            st.error("当前总绩点必须在 0 到 5 之间")
        else:
            total_credits = current_credit_num
            total_points = current_credit_num * current_gpa_num

            for course in st.session_state.courses:
                total_credits += course["credit"]
                total_points += course["credit"] * course["gpa"]

            final_gpa = total_points / total_credits if total_credits > 0 else 0

            st.success(f"总学分：{total_credits:.2f}")
            st.success(f"总绩点：{final_gpa:.4f}")

    except ValueError:
        st.error("请正确填写当前总学分和当前总绩点")


# =========================
# 2. 根据目标总绩点反推所需新课程平均绩点
# =========================
st.subheader("反推所需新课程平均绩点")

target_gpa = st.text_input("目标总绩点", key="target_gpa")
future_credit = st.text_input("未来新课程总学分", key="future_credit")

if st.button("计算所需平均绩点"):
    try:
        current_credit_num = parse_number(current_credit)
        current_gpa_num = parse_number(current_gpa)
        target_gpa_num = parse_number(target_gpa)
        future_credit_num = parse_number(future_credit)

        if current_credit_num < 0:
            st.error("当前总学分不能小于 0")
        elif not (0 <= current_gpa_num <= 5):
            st.error("当前总绩点必须在 0 到 5 之间")
        elif not (0 <= target_gpa_num <= 5):
            st.error("目标总绩点必须在 0 到 5 之间")
        elif future_credit_num <= 0:
            st.error("未来新课程总学分必须大于 0")
        else:
            needed_gpa = (
                target_gpa_num * (current_credit_num + future_credit_num)
                - current_credit_num * current_gpa_num
            ) / future_credit_num

            st.info(f"若想达到目标总绩点 {target_gpa_num:.4f}：")
            st.info(f"未来 {future_credit_num:.2f} 学分的平均绩点需要达到：{needed_gpa:.4f}")

            if needed_gpa > 5:
                st.warning("这个目标超过 5.0，按当前规则无法达到。")
            elif needed_gpa < 0:
                st.warning("所需平均绩点小于 0，说明你已经超过这个目标了。")
            else:
                st.success("这个目标在理论上可实现。")

    except ValueError:
        st.error("请正确填写所有数字")