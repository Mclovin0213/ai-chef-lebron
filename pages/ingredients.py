import streamlit as st
from ai_template import get_json_response

system_prompt = """
    Make some recipes based on these ingredients, output in json
"""

def show(database):
    ingredients = st.text_area("Input Ingredients")


    if st.button("Submit"):

        user_prompt = ", ".join(ingredients)



        output = get_json_response(system_prompt, user_prompt)

        st.write(output)

        data = {
            "userData": {
                "ingredients": ingredients
            },
        }
        user = st.session_state['user']
        database.collection("users").document(user['localId']).set(data)





