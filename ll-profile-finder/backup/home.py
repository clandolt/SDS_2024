import time
import streamlit as st
import profile_finder.builder as pfb
import profile_finder.manager as pfm
import profile_finder.config as config


if __name__ == "__main__":

    st.title("RAG app for the business case")
    st.subheader("by D ONE - Data Driven Value Creation", divider=True)

    input_text = st.text_area(
        "Describe the project and its requirements below:",
        # a simple example of project description
        "Building a data platform for a mechanical engineering company. "
        "Previous experience with Databricks is nice to have. "
        "Direct experience or education in mechatronics is very important!"
    )
    col1, _, _= st.columns(3)
    with col1:
        # Challenge #1: implement selection of an LLM model: 
        # - use selectbox() method of the streamlit, 
        # - pass a string with an appropriate question for users,
        # - check out supported LLMs in the config.py and pass them to selectbox()
        pass
        
    required_cert = st.selectbox(
        'Which technology certification is required?',
        config.ALL_CERTIFICATES,
    )
    required_skillset = st.text_input(
        "List names of required technologies (comma separated values expected)"
    )
    required_skills = pfb.parse_skills(required_skillset)


    # Challenge #2: implement a checkbox for consultant capacity: 
    # - use checkbox() method of the streamlit,
    # - pass a string with an appropriate question for users,
    # - pass the checkbox value to has_capacity argument of the function building the context
    pass

    # Challenge #3: create a dropdown menu for capacity values:
    # - use selectbox() method of the streamlit, 
    # - pass a string with an appropriate question for users,
    # - check out config.py for an appropriate range of values,
    # - extend definition of build_context_from_table to support the selected capacity,
    # - pass the selected capacity to the function and update consultant full capacity with it
    pass

    # retrieve text of biographies
    biographies, count = pfb.build_context_from_table(
        config.DATA_PATH,
        required_cert=required_cert,
        required_skills=required_skills,
    )
    # estimate pricing
    if count > 0:
         # using gpt-35 tokenizer for simplicity
        warning = pfb.print_stats_pricing(biographies, count)
        st.write(warning)
        st.divider()

        with st.spinner("Waiting for response..."):
            all_configs_loaded = False
            while not input_text:
                time.sleep(3)
            if st.button("Generate response"):
                # get GPT response
                
                # Challenge #4: time the LLM prompt: 
                # - wrap the following function with time.time(),
                # - compute the difference between the end and the start time, 
                # - show to the user using write() method of the streamlit
                pass
                profiles, file_name = pfm.find_best_matching_profiles(
                    input_text,
                    biographies,
                    save_output=config.SAVE_OUTPUT_TO_JSON,
                )
                pass
                
                # save to file
                if file_name:
                    st.write(f"The output will be stored in the file {file_name}.")
                # enforce ranking
                cleaned_profiles = []
                for item in profiles.items():
                    cleaned_profiles.append(
                        (
                            item[1][config.SYSTEM_PROMPT_JSON_RANK],
                            item[0],
                            item[1][config.SYSTEM_PROMPT_JSON_REASONS],
                        )
                    )
                cleaned_profiles = sorted(cleaned_profiles, key=lambda x: x[0])
                # display results
                for profile in cleaned_profiles:
                    st.text_area(f"Rank: {profile[0]}, Profile: {profile[1]}.", value=profile[2])
    else:
        st.write("No biographies satisfy the requirements.")