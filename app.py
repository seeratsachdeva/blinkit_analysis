import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration and layout
st.set_page_config(page_title="BlinkIT Sales Dashboard", layout="wide")

# Load dataset
DATA_PATH = "https://raw.githubusercontent.com/seeratsachdeva/blinkit_analysis/refs/heads/main/BlinkIT%20Grocery%20Data%20(1).csv"
try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    st.error(f"Error loading dataset: {e}")

# Custom CSS for color scheme (yellow background, green, light gray, black)
st.markdown("""
    <style>
    .main {
        background-color: #FFFF00;  /* Yellow Background */
    }
    .stTextInput {
        background-color: #f0f0f0;  /* Light gray for input fields */
    }
    .stButton>button {
        background-color: #4CAF50;  /* Green for buttons */
        color: white;
    }
    .stButton:hover>button {
        background-color: #388E3C;  /* Darker green on hover */
        color: white;
    }
    .stTitle {
        color: #000000;  /* Black for titles */
    }
    </style>
""", unsafe_allow_html=True)

# Function for login system
def login():
    st.markdown("<h1 style='color: black;'>Login to Blink<span style='color: #4CAF50;'>IT</span> Dashboard</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "admin":  # Basic username/password check
            st.success("Login Successful")
            st.session_state["logged_in"] = True  # Save login status in session state
        else:
            st.error("Incorrect Username or Password")

# Check login status using session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Main Section - login check
if st.session_state["logged_in"]:
    # After successful login, show the dashboard content
    st.sidebar.title("BlinkIT Dashboard Navigation")
    
    # Sidebar navigation options
    section = st.sidebar.radio("Go to", ["Overview", "Sales Analysis", "Item Type Analysis", "Outlet Analysis", "Custom Analysis", "Add Data"])

    # Overview Section
    if section == "Overview":
        st.markdown("<h1 style='color: black;'>Blink<span style='color: #4CAF50;'>IT</span> Sales Overview</h1>", unsafe_allow_html=True)
        st.subheader("Summary")
        
        total_sales = df['Sales'].sum()
        number_of_sales = df['Sales'].count()
        number_of_items = df['Item Identifier'].nunique()
        avg_rating = df['Rating'].mean()

        st.write(f"**Total Sales:** ${total_sales:,.2f}")
        st.write(f"**Number of Sales Transactions:** {number_of_sales}")
        st.write(f"**Number of Unique Items:** {number_of_items}")
        st.write(f"**Average Rating:** {avg_rating:.2f}")

        st.markdown("""
        This dashboard presents insights into Blink<span style='color: #4CAF50;'>IT</span> sales data, including analysis on item types, outlet performance, 
        and sales distribution across various parameters.
        """, unsafe_allow_html=True)

    # Sales Analysis Section
    elif section == "Sales Analysis":
        st.title("Sales Analysis")
        st.subheader("Visualize Sales Data")

        # Chart type selection
        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Pie Chart", "Area Chart", "Histogram", "Scatter Plot", "Box Plot"])

        # Sales by Item Type
        item_sales = df.groupby('Item Type')['Sales'].sum()

        if chart_type == "Bar Chart":
            fig, ax = plt.subplots(figsize=(10, 5))
            item_sales.plot(kind='bar', color=['yellow', 'green', 'black', 'white'], ax=ax)
            plt.title('Sales by Item Type (Bar Chart)')
            plt.ylabel('Total Sales')
            st.pyplot(fig)

        elif chart_type == "Line Chart":
            fig, ax = plt.subplots(figsize=(10, 5))
            item_sales.plot(kind='line', marker='o', color='green', ax=ax)
            plt.title('Sales by Item Type (Line Chart)')
            plt.ylabel('Total Sales')
            st.pyplot(fig)

        elif chart_type == "Pie Chart":
            fig, ax = plt.subplots(figsize=(8, 8))
            item_sales.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
            plt.title('Sales by Item Type (Pie Chart)')
            st.pyplot(fig)

        elif chart_type == "Area Chart":
            fig, ax = plt.subplots(figsize=(10, 5))
            item_sales.plot(kind='area', alpha=0.5, ax=ax)
            plt.title('Sales by Item Type (Area Chart)')
            plt.ylabel('Total Sales')
            st.pyplot(fig)

        elif chart_type == "Histogram":
            fig, ax = plt.subplots(figsize=(10, 5))
            df['Sales'].plot(kind='hist', bins=30, color='green', ax=ax)
            plt.title('Sales Distribution (Histogram)')
            plt.xlabel('Sales')
            plt.ylabel('Frequency')
            st.pyplot(fig)

        elif chart_type == "Scatter Plot":
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.scatter(df['Item Weight'], df['Sales'], color='green')
            plt.title('Sales vs. Item Weight (Scatter Plot)')
            plt.xlabel('Item Weight')
            plt.ylabel('Sales')
            st.pyplot(fig)

        elif chart_type == "Box Plot":
            fig, ax = plt.subplots(figsize=(10, 5))
            df.boxplot(column='Sales', by='Item Type', ax=ax)
            plt.title('Sales Distribution by Item Type (Box Plot)')
            plt.suptitle('')
            plt.ylabel('Sales')
            st.pyplot(fig)

    # Item Type Analysis Section (Fix)
    elif section == "Item Type Analysis":
        st.title("Item Type Analysis")
        st.subheader("Analyze Sales by Item Type")

        # Aggregate sales by item type
        item_type_sales = df.groupby('Item Type')['Sales'].sum().sort_values(ascending=False)

        st.write("**Sales by Item Type:**")
        st.bar_chart(item_type_sales)

    # Outlet Analysis Section (Fix)
    elif section == "Outlet Analysis":
        st.title("Outlet Analysis")
        st.subheader("Analyze Sales by Outlet")

        # Aggregate sales by outlet type
        outlet_sales = df.groupby('Outlet Type')['Sales'].sum().sort_values(ascending=False)

        st.write("**Sales by Outlet Type:**")
        st.bar_chart(outlet_sales)

    # Custom Analysis Section
    elif section == "Custom Analysis":
        st.title("Custom Analysis")
        st.subheader("Create Your Own Analysis")

        # Select column for aggregation
        agg_column = st.selectbox("Select Column for Aggregation", df.select_dtypes(include=['float64', 'int64']).columns)

        # Select column to group by
        group_by_column = st.selectbox("Select Column to Group By", df.columns)

        # Select aggregation type
        agg_type = st.selectbox("Select Aggregation Type", ["Sum", "Average", "Count"])

        if st.button("Generate Analysis"):
            try:
                if agg_type == "Sum":
                    result = df.groupby(group_by_column)[agg_column].sum()
                elif agg_type == "Average":
                    result = df.groupby(group_by_column)[agg_column].mean()
                elif agg_type == "Count":
                    result = df.groupby(group_by_column)[agg_column].count()

                st.write(f"### Result of {agg_type} of '{agg_column}' grouped by '{group_by_column}':")
                st.write(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Add Data Section
    elif section == "Add Data":
        st.title("Add Data")
        st.subheader("Enter new data to add to the dataset")

        # Input fields for new data
        new_data = {}
        for column in df.columns:
            if df[column].dtype == 'object':
                new_data[column] = st.text_input(f"Enter {column}")
            elif df[column].dtype in ['int64', 'float64']:
                new_data[column] = st.number_input(f"Enter {column}", value=0)

        # Add new data to the dataframe
        if st.button("Add Row"):
            try:
                new_row = pd.DataFrame([new_data])
                df = pd.concat([df, new_row], ignore_index=True)
                st.success("Row added successfully!")
                st.dataframe(df.tail())
            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    login()
