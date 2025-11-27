import streamlit as st

st.title("🏥 MedSecure AI - Test")
st.success("✅ Basic setup completed successfully!")
st.write("If you can see this, Streamlit is working!")

if st.button('Click to test'):
    st.balloons()
    st.write('🎉 Everything works!')