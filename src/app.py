import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Rag import generate_marketing_message_mistral
from llama import generate_marketing_message_llama
from de import random_selected_title



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
            st.session_state['dataframe'] = dataframe
            st.success("File uploaded successfully!")
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

        # Ensure the 'selected_name' in session state exists in the current options
        if 'selected_name' not in st.session_state or st.session_state.selected_name not in first_column_options:
            st.session_state.selected_name = first_column_options[0] if first_column_options else None

        # Display the selectbox with safe handling of the index
        if first_column_options:
            selected_name = st.selectbox(
                "Choose a name:",
                first_column_options,
                index=first_column_options.index(st.session_state.selected_name) if st.session_state.selected_name in first_column_options else 0
            )
            st.session_state.selected_name = selected_name
        else:
            st.write("No options available for selection.")


        # Save the selected name to session_state
        st.session_state.selected_name = selected_name

    # Page number input comes in col2
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
        category = st.selectbox(
            "Select a Category:",
            ["Dining", "Travelling", "Other"]
        )
    
    st.divider()
    
    # Initialize session state variables if they don't exist
    if 'generated_messages' not in st.session_state:
        st.session_state.generated_messages = False
    
    if st.button("Generate the Marketing Message"):
         
        customer_name = st.session_state.selected_name
        selected_voice = st.session_state.selected_voice
        discount = 20
        hotel_name = "Apa Villa Thalpe"
        start_date = "04th September 2024"
        end_date = "30th April 2025"
        link = card_links[card_type]
    
        # Extract location and gender from the dataframe based on the selected customer
        filtered_data = st.session_state['dataframe'][st.session_state['dataframe'].iloc[:, 0] == customer_name]
    
        if not filtered_data.empty:
            # Get the location and gender for the selected customer
            residence = filtered_data['Residance'].values[0]
            employment = filtered_data['Employment'].values[0]  
            # gender = filtered_data['gender'].values[0]  # Assuming 'Gender' column exists

            # Fetch offers
            offers = random_selected_title(card_type, category)
            print(offers)
            
            if not offers or "title" not in offers or "offer_details" not in offers:
                print("❌ No valid offers found for the given card and category.")

            title = offers["title"]
            details = offers["offer_details"]

            # print(f"Customer Name: {customer_name}")
            # print(f"Residence: {residence}")
            # print(f"Employment: {employment}")
            # print(f"Selected Voice: {selected_voice}")
            # print(f"Card Type: {card_type}")
            # print(f"Category: {category}")
            # print(f"Link: {link}")
            # print(f"title: {title}")
            # print(f"details: {details}")

            # Generate messages from both models, passing location and gender as parameters
            st.session_state.mistral_message = generate_marketing_message_mistral(customer_name, residence, employment, selected_voice, card_type, category,link,title,details)
            # print(st.session_state.mistral_message)
            st.session_state.llama_message = generate_marketing_message_llama(customer_name, residence, employment, selected_voice, card_type, category, link, title, details)
            # print(st.session_state.mistral_message)
            # Set flag to indicate messages have been generated
            st.session_state.generated_messages = True
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
        
        

st.divider()



