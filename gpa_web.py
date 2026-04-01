import streamlit as st

st.set_page_config(page_title="绩点计算器", page_icon="📘", layout="centered")

st.title("📘 绩点计算器")

st.write("输入当前总学分、当前总绩点，以及后续课程的学分和绩点，计算新的总学分和总绩点。")

# 初始化课程列表
if "courses" not in st.session_state:
    st.session_state.courses = []


def parse_number(value):
    """兼容逗号和点号小数"""
    return float(str(value).replace(",", "."))


# 当前信息
st.subheader("当前信息")
current_credit = st.text_input("当前总学分", value="0")
current_gpa = st.text_input("当前总绩点", value="0")

st.subheader("添加新课程")
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
                st.session_state.courses.append({"credit": credit, "gpa": gpa})
                st.success(f"已添加课程：学分 {credit}，绩点 {gpa}")
        except ValueError:
            st.error("请输入有效数字")

with col2:
    if st.button("清空课程"):
        st.session_state.courses = []
        st.success("已清空所有新课程")

# 显示已添加课程
st.subheader("已添加课程")
if st.session_state.courses:
    for i, course in enumerate(st.session_state.courses, start=1):
        st.write(f"课程{i}：学分 {course['credit']}，绩点 {course['gpa']}")
else:
    st.info("暂无已添加课程")

# 计算结果
st.subheader("计算结果")
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