import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Rag import generate_marketing_message_mistral
from llama import generate_marketing_message_llama
from de2 import find_closest_offer
from WeightedScoringSystem import calculate_interest
import asyncio
from bs4 import BeautifulSoup
import markdown



# Initialize session state
if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = None

# //////////////// Heading Information ///////////////
col1, col2 = st.columns([1, 3], gap="small")
with col1:
    st.image("./static/boc.jpg", caption="Boc Smart Generator")
with col2:
    st.title("Personalized Marketing Message Generator")

# //////////////// Sidebar for File Upload ///////////////
# Custom CSS for reducing gaps
custom_css = """
<style>
    /* Previous CSS rules remain the same */
    .css-1d391kg {
        padding: 0 !important;
    }
    
    .css-1v3fvcr, .css-1n76uvr, .css-12w0qpk, .css-1yn6avt, .css-qri22k {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Modified header styling to remove bottom margin */
    .css-1v3fvcr h2 {
        margin: 0 0 -64px 0 !important;  /* Negative bottom margin to pull selectbox up */
        padding: 0 !important;
        font-size: 0.9em !important;
        line-height: 1 !important;
    }
    
    /* Tighten selectbox spacing */
    .stSelectbox {
        margin-top: 0 !important;
        padding-top: 0 !important;
        line-height: 1 !important;
    }
    
    /* Remove default selectbox label padding */
    .stSelectbox > div > div {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Adjust select container spacing */
    .css-1n76uvr .stSelectbox div[data-baseweb="select"] {
        margin: 0 !important;
        padding: 0 4px !important;
        min-height: 24px !important;
    }
    
    /* Additional spacing control for headers */
    .css-1n76uvr > div > div > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Further reduce any extra margins */
    div[data-testid="stMarkdownContainer"] {
        margin-bottom: -5px !important;
    }
    
    /* Rest of the previous CSS remains the same */
    .css-12w0qpk .stFileUploader {
        padding: 0 !important;
        margin-bottom: 4px !important;
    }
    
    .css-1n76uvr label, .css-12w0qpk label {
        padding: 0 !important;
        margin: 0 !important;
        line-height: 1 !important;
        display: none !important;
    }
    
    .css-1n76uvr .stSelectbox div[data-baseweb="select"] div:first-child {
        height: 24px !important;
        min-height: 24px !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    div[data-baseweb="popover"] ul {
        padding: 0 !important;
    }
    
    .uploadedFile {
        margin: 0 !important;
        padding: 2px !important;
    }
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    # Product Type
    st.markdown(
        "<h2 style='font-weight: bold; font-size: 1 rem;'>Product Type</h2>",
        unsafe_allow_html=True
    )
    ProductType = st.selectbox(' ', ('Credit Card Offers',), label_visibility="collapsed")
    
    # Marketing Channel
    st.markdown(
        "<h2 style='font-weight: bold; font-size: 1 rem;'>Marketing Channel</h2>",
        unsafe_allow_html=True
    )
    Marketing = st.selectbox('  ', ('WhatsApp', 'Email'), label_visibility="collapsed")
    
    # Tone of Voice
    st.markdown(
        "<h2 style='font-weight: bold; font-size: 1 rem;'>Tone of the Voice</h2>",
        unsafe_allow_html=True
    )
   

    
    # voice = st.selectbox('   ', ('Formal', 'Empathetic', 'Humorous'), key='voice', label_visibility="collapsed")
    selected_voice = st.selectbox('Choose a Voice:',["Empathetic","Formal","Humorous"])
    
    # Update the session state with the selected voice
    st.session_state.selected_voice = selected_voice

    expected_columns = [
    "Name", "DOB", "Employment", "Residance", "Online Shopping(Count)", 
    "Super Market(Count)", "Grocery(Count)", "Travelling(Count)", 
    "Payments(Count)", "Other(Count)", "Total No. of Transactions", 
    "Online Shopping(Volume)", "Super Market(Volume)", "Grocery(Volume)", 
    "Travelling(Volume)", "Payments(Volume)", "Other(Volume)", 
    "Volume of Transactions", "Tel.No", "Email Address"
]
    # File Upload
    st.markdown(
        "<h2 style='font-weight: bold; font-size: 1 rem;'>Please upload a Customer Excel file</h2>",
        unsafe_allow_html=True
    )
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        accept_multiple_files=False,
        type="xlsx",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            dataframe = pd.read_excel(uploaded_file)
            # Check if the columns in the uploaded file match the expected columns
            if list(dataframe.columns) == expected_columns:
                st.session_state['dataframe'] = dataframe
                st.success("File uploaded successfully!")
            else:
                # Find the mismatched columns
                missing_columns = set(expected_columns) - set(dataframe.columns)
                extra_columns = set(dataframe.columns) - set(expected_columns)

                error_message = "The uploaded file does not match the required format.\n"

                if missing_columns:
                    error_message += f"Missing columns: {', '.join(missing_columns)}.\n"
                if extra_columns:
                    error_message += f"Extra columns: {', '.join(extra_columns)}.\n"

                st.error(error_message)
        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")

# //////////////// Customer Information ///////////////
st.divider()
st.header("Customer Information")
# Check if dataframe is loaded in session state
if st.session_state.get('dataframe') is not None:
    st.write("Refreshed Customer Data:")

    # Pagination setup
    rows_per_page = 10  # Number of rows to display per page
    total_rows = len(st.session_state['dataframe'])
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page  # Calculate total number of pages

    # Get the current page number
    page_number = st.session_state.get("page_number", 1)  # Default to page 1 if not set

    # Calculate start and end indices
    start_idx = (page_number - 1) * rows_per_page
    end_idx = min(start_idx + rows_per_page, total_rows)  # Ensure it doesn't go beyond the total rows

    # Display row range and total rows
    st.write(f"Displaying rows {start_idx + 1} to {end_idx} of {total_rows}")

    # Display the current page of the DataFrame
    current_page_data = st.session_state['dataframe'].iloc[start_idx:end_idx]
    st.dataframe(current_page_data)

    # Filter dropdown options based on visible rows (first column)
    first_column_options = current_page_data.iloc[:, 0].dropna().unique().tolist()

    # Create two columns for dropdown and page navigation
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Select Names for Analysis:")

        # Extract unique names from dataframe safely
        first_column_options = dataframe["Name"].dropna().unique().tolist() if not dataframe.empty else []

        # Ensure 'selected_name' is in session state and valid
        if 'selected_name' not in st.session_state or st.session_state.selected_name not in first_column_options:
            st.session_state.selected_name = first_column_options[0] if first_column_options else None

        # Display select box safely
        if first_column_options:
            selected_name = st.selectbox(
                "Choose a name:",
                first_column_options,
                index=first_column_options.index(st.session_state.selected_name) if st.session_state.selected_name in first_column_options else 0
            )

            # Update session state if the name changes
            if st.session_state.selected_name != selected_name:
                st.session_state.selected_name = selected_name
                st.rerun()  

        else:
            st.write("No options available for selection.")
            selected_name = None  # Handle empty case

        # Convert DataFrame to list of dictionaries safely
        users_data = dataframe.to_dict(orient="records") if not dataframe.empty else []

        # Debugging: Show selected name and data
        st.write(f"DEBUG: Selected Name → {st.session_state.selected_name}")
        print(dataframe.columns.tolist())  # Check available columns

        # Calculate interest only if a valid name is selected
        if st.session_state.selected_name and users_data:
            user_interest = calculate_interest(users_data, st.session_state.selected_name)  # Fix function call

            # Store user_interest in session state
            st.session_state.user_interest = user_interest

            if user_interest:
                st.success(f"User: **{st.session_state.selected_name}** is more interested in **{user_interest}**")
            else:
                st.warning(f"No transaction data available for **{selected_name}**")
        else:
            st.warning("No data available for the selected user.")

    # Debugging: Show stored session state values
    st.write(f"DEBUG: Stored Interest → {st.session_state.get('user_interest', 'No interest data')}")


    with col2:
        st.markdown("<h4 style='font-weight: bold; margin-bottom: 0;'>Page Number</h4>", unsafe_allow_html=True)
        page_number = st.number_input(
            "Navigate Pages", 
            min_value=1, 
            max_value=total_pages, 
            value=page_number, 
            step=1, 
            key="page_number"
        )

    # Filter the data based on the selected name
    filtered_data = st.session_state['dataframe'][st.session_state['dataframe'].iloc[:, 0] == selected_name]

    pie, col3 = st.columns(2)
    with pie:
    # If there is filtered data, plot the transaction count distribution
        if not filtered_data.empty:
            st.subheader(f"Transaction Count Distribution for {selected_name}")

            # Define the transaction categories (these columns should exist in your DataFrame)
            categories = ['Online Shopping(Count)', 'Super Market(Count)', 'Grocery(Count)', 'Travelling(Count)', 'Payments(Count)', 'Other(Count)']
            
            # Extracting the transaction counts for each category (assumes these columns exist in your DataFrame)
            transaction_counts = [
                filtered_data['Online Shopping(Count)'], 
                filtered_data['Super Market(Count)'], 
                filtered_data['Grocery(Count)'], 
                filtered_data['Travelling(Count)'], 
                filtered_data['Payments(Count)'], 
                filtered_data['Other(Count)']
            ]
            
            # Sum the transaction counts for each category
            transaction_counts = [col.sum() for col in transaction_counts]

            # Create a Pie Chart for the transaction count distribution
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(transaction_counts, colors=sns.color_palette("Set2", len(categories)))
            ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

            # Move the legend outside the pie chart
            ax.legend(categories, title="Transaction Categories", bbox_to_anchor=(1.1, 0.5), loc='center left')

            # Display the Pie Chart
            st.pyplot(fig)
        else:
            st.write("No transaction data available for the selected name.")
    with col3:
        if not filtered_data.empty:
            st.subheader(f"Transaction Volume Distribution for {selected_name}")

            # Define the transaction categories (these columns should exist in your DataFrame)
            categories = ['Online Shopping(Volume)', 'Super Market(Volume)', 'Grocery(Volume)', 'Travelling(Volume)', 'Payments(Volume)', 'Other(Volume)']
            
            # Extracting the transaction volumes for each category (assumes these columns exist in your DataFrame)
            transaction_volumes = [
                filtered_data['Online Shopping(Volume)'], 
                filtered_data['Super Market(Volume)'], 
                filtered_data['Grocery(Volume)'], 
                filtered_data['Travelling(Volume)'], 
                filtered_data['Payments(Volume)'], 
                filtered_data['Other(Volume)']
            ]
            
            # Sum the transaction volumes for each category
            transaction_volumes = [col.sum() for col in transaction_volumes]

            # Create a Bar Chart for the transaction volume distribution
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(categories, transaction_volumes, color=sns.color_palette("Set2", len(categories)))

            # Rotate x labels for better readability
            ax.set_xticklabels(categories, rotation=45, ha='right')

            # Set chart labels and title
            ax.set_ylabel('Volume of Transactions')

            # Display the Bar Chart
            st.pyplot(fig)

        else:
         st.write("No transaction data available for the selected name.")
else:
    st.write("No data uploaded yet. Please upload an Excel file in the sidebar.")




st.divider()


# //////////////// Marketing Message Generation with Watsonx.ai ///////////////
st.header("Marketing Message Generation with Watsonx.ai")
# Check if dataframe is loaded in session state

if st.session_state.get('dataframe') is not None:

    card_links = {
    "World Master Card": "https://www.boc.lk/personal-banking/cards/credit-cards/world-master-card",
    "Titanium Card": "https://www.boc.lk/personal-banking/cards/credit-cards/master-titanium-card"
}
    # Create two columns
    col1, col2 = st.columns(2)

    # Radio button in the first column
    with col1:
        # Radio button for selecting card type
        card_type = st.radio(
            "Choose a Card:",
            list(card_links.keys())  # Dynamically get card names
        )

    # Select box in the second column
    with col2:
        # category = st.selectbox(
        #     "Select a Category:",
        #     ["Dining", "Travelling", "Other"]
        # )
        category=st.session_state.user_interest
        st.write(f"The Most Like category : **{category}**")
    
    st.divider()
    
    # Initialize session state variables if they don't exist
    if 'generated_messages' not in st.session_state:
        st.session_state.generated_messages = False
    
    if 'generated_messages_df' not in st.session_state:
        st.session_state['generated_messages_df'] = None  # Will hold the generated messages
    if 'generated_messages_All' not in st.session_state:
        st.session_state['generated_messages_All'] = False 

    if st.button("Generate the Marketing Message"):
         
        customer_name = st.session_state.selected_name
        selected_voice = st.session_state.selected_voice
        discount = 20
        hotel_name = "Apa Villa Thalpe"
        start_date = "04th September 2024"
        end_date = "30th April 2025"
        # reference_location="DEHIWALA"
        link = card_links[card_type]
    
        # Extract location and gender from the dataframe based on the selected customer
        filtered_data = st.session_state['dataframe'][st.session_state['dataframe'].iloc[:, 0] == customer_name]
    
        if not filtered_data.empty:
            # Get the location and gender for the selected customer
            residence = filtered_data['Residance'].values[0]
            employment = filtered_data['Employment'].values[0]  
            # gender = filtered_data['gender'].values[0]  # Assuming 'Gender' column exists

            # Fetch offers
            offers = find_closest_offer(card_type, category,residence)
            print(offers)
            
            if not offers or "title" not in offers or "offer_details" not in offers:
                print("❌ No valid offers found for the given card and category.")

            title = offers["title"]
            details = offers["offer_details"]
            distance = offers["distance"]
            print(f"Customer Name.................: {st.session_state.user_interest}")
            print(f"Customer Name: {customer_name}")
            print(f"Residence: {residence}")
            print(f"Employment: {employment}")
            print(f"Selected Voice: {selected_voice}")
            print(f"Card Type: {card_type}")
            print(f"Category: {category}")
            print(f"Link: {link}")
            print(f"title: {title}")
            print(f"details: {details}")
            print(f"details: {distance}")

            # # Generate messages from both models, passing location and gender as parameters
            # st.session_state.mistral_message = generate_marketing_message_mistral(customer_name, residence, employment, selected_voice, card_type, category,link,title,details)
            # # print(st.session_state.mistral_message)
            # st.session_state.llama_message = generate_marketing_message_llama(customer_name, residence, employment, selected_voice, card_type, category, link, title, details)
            # # print(st.session_state.mistral_message)
            # # Set flag to indicate messages have been generated
            # st.session_state.generated_messages = True

            async def generate_messages():
                mistral_task = asyncio.create_task(generate_marketing_message_mistral(customer_name, residence, employment, selected_voice, card_type, category, link, title, details,distance))
                llama_task = asyncio.create_task(generate_marketing_message_llama(customer_name, residence, employment, selected_voice, card_type, category, link, title, details,distance))

                mistral_message, llama_message = await asyncio.gather(mistral_task, llama_task)

                st.session_state.mistral_message = mistral_message
                st.session_state.llama_message = llama_message
                st.session_state.generated_messages = True

            asyncio.run(generate_messages())

        else:
            st.write("No customer data available for the selected name.")
    # Display messages if they have been generated
    st.divider()
    if st.session_state.generated_messages:
        mistral_col, llama_col = st.columns(2)
        
        with mistral_col:
            st.subheader("Generated Marketing Message (Mistral)")
            st.markdown(st.session_state.mistral_message)
        
        with llama_col:
            st.subheader("Generated Marketing Message (Llama)")
            st.markdown(st.session_state.llama_message)
        
        # Radio button for selection
        choice = st.radio(
            "Select the preferred marketing message:",
            options=["Mistral", "Llama"],
            key="message_choice"
        )
        
        # Store selected message based on choice
        if choice == "Mistral":
            st.session_state.selected_message = st.session_state.mistral_message
        else:
            st.session_state.selected_message = st.session_state.llama_message
        
        # Display selected message
        st.markdown("---")
        st.subheader("Selected Marketing Message:")
        st.markdown(st.session_state.selected_message)
        
  
    # Function to strip markdown formatting
    def strip_markdown(md_text):
       html = markdown.markdown(md_text)
       plain_text = BeautifulSoup(html, "html.parser").get_text()
       return plain_text

   # Create a button to generate marketing messages for all customers
    if st.button("Generate Marketing Messages for All Customers"):
        # Check if the dataframe is loaded and messages haven't been generated yet
        if st.session_state['dataframe'] is not None and not st.session_state.generated_messages_All:
            # Prepare an empty list to store customer marketing messages
            all_messages = []

            # Iterate through all customers in the dataframe
            for index, row in st.session_state['dataframe'].iterrows():
                customer_name = row['Name']
                residence = row['Residance']
                employment = row['Employment']
                selected_voice = st.session_state.selected_voice
                link = card_links.get(card_type)

                # **Compute category dynamically for each customer**
                users_data = st.session_state['dataframe'].to_dict(orient="records")
                category = calculate_interest(users_data, customer_name)  # **This ensures each customer gets their unique category**


                # Get offers
                offers = find_closest_offer(card_type, category,residence)
                title = offers["title"]
                details = offers["offer_details"]
                distance = offers["distance"]

                # Generate marketing messages
                async def generate_messages_for_all():
                    # Await the tasks and make sure both messages are fetched correctly
                    mistral_message = await generate_marketing_message_mistral(
                        customer_name, residence, employment, selected_voice, card_type, category, link, title, details,distance
                    )
                    llama_message = await generate_marketing_message_llama(
                        customer_name, residence, employment, selected_voice, card_type, category, link, title, details,distance
                    )

                    return {
                        'Customer Name': customer_name,
                        'Category': category,
                        'Mistral Message': strip_markdown(mistral_message),  # Clean markdown
                        'Llama Message': strip_markdown(llama_message)  # Clean markdown
                }

                # Run the async function and store the result
                customer_message = asyncio.run(generate_messages_for_all())
                all_messages.append(customer_message)

            # Convert the list of dictionaries to a DataFrame
            messages_df = pd.DataFrame(all_messages)

            # Save the DataFrame as a CSV file
            csv_filename = "generated_marketing_messages.csv"
            messages_df.to_csv(csv_filename, index=False)

            # Store the DataFrame in session state
            st.session_state['generated_messages_df'] = messages_df
            st.session_state.generated_messages_All = True  # Set flag to True after generation

            st.success(f"Marketing messages for all customers have been generated and saved as {csv_filename}.")

        elif st.session_state.generated_messages_All:
            st.write("Marketing messages have already been generated. You can download the previous results.")
            # Access the generated messages from session state
            st.dataframe(st.session_state['generated_messages_df'])

        else:
            st.write("No customer data available in the session.")

    # If messages have already been generated, show the messages and allow download
    if st.session_state.generated_messages_All:
        messages_df = st.session_state['generated_messages_df']  # Retrieve the generated messages
        st.dataframe(messages_df)

        # Allow the user to download the CSV file
        st.download_button(
            label="Download Marketing Messages CSV",
            data=messages_df.to_csv(index=False),
            file_name="generated_marketing_messages.csv",
            mime="text/csv"
        )

st.divider()



