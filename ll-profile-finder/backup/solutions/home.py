import time
import streamlit as st
from profile_finder import builder as pfb
from profile_finder import manager as pfm
from profile_finder import config


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
        # select LLM
        config.SELECTED_MODEL = st.selectbox(
            'Which model to use?',
            config.MODEL_SET,
        )
    
    required_cert = st.selectbox(
        'Which technology certification is required?',
        config.ALL_CERTIFICATES,
    )
    required_skillset = st.text_input(
        "List names of required technologies (comma separated values expected)"
    )
    required_skills = pfb.parse_skills(required_skillset)

    # add checkbox for capacity
    has_capacity = st.checkbox('Consider available capacity only?')
    # add dropdown to select the capacity value
    # use checkbox value to disable selectbox if capacity not under consideration
    selected_capacity = st.selectbox(
        'Select capacity',
        config.CONSULTANT_CAPACITY_RANGE,
        disabled=not has_capacity,
    )

    # retrieve text of biographies
    biographies, count = pfb.build_context_from_table(
        config.DATA_PATH,
        # pass input capacity flag and value
        has_capacity=has_capacity,
        selected_capacity=selected_capacity,
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
                
                # and time the response
                start_time = time.time()
                profiles, file_name = pfm.find_best_matching_profiles(
                    input_text,
                    biographies,
                    save_output=config.SAVE_OUTPUT_TO_JSON,
                )
                total_secondes = round(time.time() - start_time, 2)
                st.write(f"The process took {total_secondes} seconds.")

                # save to file
                if file_name is not None:
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
