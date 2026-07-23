import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from io import BytesIO
from typing import Any

# Page configuration
st.set_page_config(
    page_title="ABC Classification Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    
    .category-card-a {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .category-card-b {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .category-card-c {
        background: linear-gradient(135deg, #45b7d1 0%, #96c93d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

def load_sample_data() -> pd.DataFrame:
    """Generate sample data for demonstration"""
    asins = []
    categories = []
    
    # Category A - 13 items
    for i in range(13):
        asins.append(f'B0{i:02d}MSW{i:03d}A')
        categories.append('A')
    
    # Category B - 37 items  
    for i in range(37):
        asins.append(f'B0{i:02d}N4B{i:03d}B')
        categories.append('B')
    
    # Category C - 26 items
    for i in range(26):
        asins.append(f'B0{i:02d}KCH{i:03d}C')
        categories.append('C')
    
    df = pd.DataFrame({
        'ASIN': asins,
        'Category': categories
    })
    
    return df

def process_uploaded_file(uploaded_file: Any) -> pd.DataFrame | None:
    """Process the uploaded file and return DataFrame"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Please upload a CSV or Excel file.")
            return None
        
        # Check if required columns exist
        required_columns = ['ASIN', 'Category']
        
        # Try to find columns that might contain the required data
        asin_column = None
        category_column = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'asin' in col_lower:
                asin_column = col
            elif any(keyword in col_lower for keyword in ['category', 'final_category', 'cat', 'class']):
                category_column = col
        
        if asin_column and category_column:
            # Rename columns to standard names
            df = df.rename(columns={asin_column: 'ASIN', category_column: 'Category'})
            
            # Clean the data
            df['ASIN'] = df['ASIN'].astype(str)
            df['Category'] = df['Category'].astype(str)
            
            # Remove rows with missing values
            df = df.dropna(subset=['ASIN', 'Category'])
            
            # Filter for only A, B, C categories
            df = df[df['Category'].isin(['A', 'B', 'C'])]
            
            st.success(f"✅ File processed successfully! Found {len(df)} records.")
            return df
        else:
            st.error("❌ Could not find required columns. Please ensure your file has columns for ASIN and Category (A/B/C).")
            st.info("Looking for columns containing: 'ASIN' and 'Category'/'Final_Category'/'Cat'")
            return None
            
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        return None

def create_category_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Create a modern donut chart for category distribution"""
    category_counts = df['Category'].value_counts()
    
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    
    fig = go.Figure(data=[go.Pie(
        labels=category_counts.index,
        values=category_counts.values,
        hole=.6,
        marker_colors=colors,
        textinfo='label+percent+value',
        textfont_size=14,
        pull=[0.1, 0, 0]  # Pull out the first slice slightly
    )])
    
    fig.update_layout(
        title={
            'text': "Category Distribution",
            'x': 0.5,
            'font': {'size': 20, 'color': '#1f2937'}
        },
        font=dict(size=12),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        height=400
    )
    
    return fig

def create_category_bar_chart(df: pd.DataFrame) -> go.Figure:
    """Create a modern bar chart for category distribution"""
    category_counts = df['Category'].value_counts().sort_index()
    
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    
    fig = go.Figure(data=[
        go.Bar(
            x=category_counts.index,
            y=category_counts.values,
            marker_color=colors,
            text=category_counts.values,
            textposition='auto',
            textfont=dict(color='white', size=14, family="Arial Black")
        )
    ])
    
    fig.update_layout(
        title={
            'text': "ASINs Count by Category",
            'x': 0.5,
            'font': {'size': 20, 'color': '#1f2937'}
        },
        xaxis_title="Category",
        yaxis_title="Number of ASINs",
        height=400,
        xaxis=dict(
            tickfont=dict(size=14, color='#1f2937'),
            title_font=dict(size=16, color='#1f2937')
        ),
        yaxis=dict(
            tickfont=dict(size=14, color='#1f2937'),
            title_font=dict(size=16, color='#1f2937'),
            gridcolor='lightgray'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_treemap(df: pd.DataFrame) -> go.Figure:
    """Create a treemap visualization"""
    category_counts = df['Category'].value_counts()
    
    fig = go.Figure(go.Treemap(
        labels=category_counts.index,
        values=category_counts.values,
        parents=[""] * len(category_counts),
        textinfo="label+value+percent root",
        marker_colors=['#ff6b6b', '#4ecdc4', '#45b7d1'],
        textfont_size=16
    ))
    
    fig.update_layout(
        title={
            'text': "Category Treemap",
            'x': 0.5,
            'font': {'size': 20, 'color': '#1f2937'}
        },
        height=400
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 ABC Classification Dashboard</h1>', unsafe_allow_html=True)
    
    # File upload section
    st.subheader("📁 Upload Your Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file containing ASINs and their categories",
            type=['csv', 'xlsx', 'xls'],
            help="File should contain columns for ASIN and Category (A/B/C)"
        )
    
    with col2:
        use_sample_data = st.checkbox("Use Sample Data", help="Check this to use sample data for demonstration")
    
    # Initialize df
    df = None
    
    # Load data based on user choice
    if uploaded_file is not None:
        df = process_uploaded_file(uploaded_file)
        if df is not None:
            st.success(f"✅ Data loaded successfully! Found {len(df)} ASINs across {df['Category'].nunique()} categories.")
            
            # Show data preview
            with st.expander("📋 Data Preview"):
                st.dataframe(df.head(10), use_container_width=True)
                
    elif use_sample_data:
        df = load_sample_data()
        st.info("📊 Using sample data for demonstration purposes.")
        
        # Show data preview
        with st.expander("📋 Sample Data Preview"):
            st.dataframe(df.head(10), use_container_width=True)
    
    else:
        # Show instructions when no data is loaded
        st.info("👆 Please upload a file or check 'Use Sample Data' to get started.")
        
        st.markdown("""
        ### 📋 File Requirements:
        
        Your file should contain:
        - **ASIN Column**: Product ASINs (any column name containing 'ASIN')
        - **Category Column**: Categories A, B, or C (column names like 'Category', 'Final_Category', 'Cat', etc.)
        
        ### 📄 Supported Formats:
        - CSV files (.csv)
        - Excel files (.xlsx, .xls)
        
        ### 📊 Example Data Structure:
        ```
        ASIN          | Category
        ------------- | --------
        B01MSW8UNY    | A
        B01N4B2R3E    | B
        B09KCHC9TF    | C
        ```
        """)
        
        return
    
    # Continue with dashboard if we have data
    if df is not None and len(df) > 0:
        # Sidebar filters
        st.sidebar.header("🔍 Filters")
        
        selected_categories = st.sidebar.multiselect(
            "Select Categories:",
            options=['A', 'B', 'C'],
            default=['A', 'B', 'C']
        )
        
        # Filter data
        filtered_df = df[df['Category'].isin(selected_categories)]
        
        if len(filtered_df) == 0:
            st.warning("No data matches the selected filters. Please adjust your selection.")
            return
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_asins = len(filtered_df)
        category_counts = filtered_df['Category'].value_counts()
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total ASINs</h3>
                <h2>{total_asins}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            category_a_count = category_counts.get('A', 0)
            st.markdown(f"""
            <div class="category-card-a">
                <h3>Category A</h3>
                <h2>{category_a_count}</h2>
                <p>High Priority</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            category_b_count = category_counts.get('B', 0)
            st.markdown(f"""
            <div class="category-card-b">
                <h3>Category B</h3>
                <h2>{category_b_count}</h2>
                <p>Medium Priority</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            category_c_count = category_counts.get('C', 0)
            st.markdown(f"""
            <div class="category-card-c">
                <h3>Category C</h3>
                <h2>{category_c_count}</h2>
                <p>Low Priority</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            fig_donut = create_category_distribution_chart(filtered_df)
            st.plotly_chart(fig_donut, use_container_width=True)
        
        with col2:
            fig_bar = create_category_bar_chart(filtered_df)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Treemap
        st.subheader("📈 Category Treemap")
        fig_treemap = create_treemap(filtered_df)
        st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Detailed table
        st.subheader("📋 Detailed ASIN List")
        
        # Search functionality
        search_term = st.text_input("🔎 Search ASINs:", placeholder="Enter ASIN to search...")
        
        display_df = filtered_df.copy()
        if search_term:
            display_df = display_df[display_df['ASIN'].str.contains(search_term, case=False, na=False)]
        
        # Category tabs
        tab1, tab2, tab3, tab4 = st.tabs(["All Categories", "Category A", "Category B", "Category C"])
        
        with tab1:
            st.dataframe(
                display_df,
                use_container_width=True,
                column_config={
                    "ASIN": st.column_config.TextColumn("ASIN", width="medium"),
                    "Category": st.column_config.SelectboxColumn(
                        "Category",
                        width="small",
                        options=["A", "B", "C"]
                    )
                }
            )
        
        with tab2:
            category_a_df = display_df[display_df['Category'] == 'A']
            st.dataframe(category_a_df, use_container_width=True)
            st.info(f"Category A contains {len(category_a_df)} ASINs - High priority items")
        
        with tab3:
            category_b_df = display_df[display_df['Category'] == 'B']
            st.dataframe(category_b_df, use_container_width=True)
            st.info(f"Category B contains {len(category_b_df)} ASINs - Medium priority items")
        
        with tab4:
            category_c_df = display_df[display_df['Category'] == 'C']
            st.dataframe(category_c_df, use_container_width=True)
            st.info(f"Category C contains {len(category_c_df)} ASINs - Low priority items")
        
        # Export functionality
        st.subheader("📤 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📄 Download as CSV",
                data=csv,
                file_name="abc_classification_filtered.csv",
                mime="text/csv"
            )
        
        with col2:
            # Create Excel buffer
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, sheet_name='ABC_Classification', index=False)
            
            st.download_button(
                label="📊 Download as Excel",
                data=buffer.getvalue(),
                file_name="abc_classification_filtered.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col3:
            json_data = filtered_df.to_json(orient='records', indent=2)
            st.download_button(
                label="🔗 Download as JSON",
                data=json_data,
                file_name="abc_classification_filtered.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
