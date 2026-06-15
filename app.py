import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. PAGE ENGINE INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="Skyward Portfolio Engine", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Set clean aesthetic defaults for matplotlib/seaborn plots within Streamlit
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.edgecolor': '#cccccc',
    'axes.linewidth': 0.8
})

# ==========================================
# 2. PREMIUM SAFE EDITORIAL CUSTOM CSS INJECTION
# ==========================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tenor+Sans&family=Outfit:wght@300;400;500;600;700&display=swap');

        /* HEADER ARCHITECTURE: Apply Tenor Sans cleanly */
        h1, h2, h3, h4, h5, h6, .custom-bold-header {
            font-family: 'Tenor Sans', system-ui, -apple-system, sans-serif !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            letter-spacing: -0.02em !important;
        }
        
        .editorial-narrative-p, .profile-inspection-dossier, .dict-box, .directive-box p {
            font-family: 'Outfit', system-ui, sans-serif !important;
            font-weight: 400;
        }

        h1 {
            font-size: 4.2rem !important;
            line-height: 1.1 !important;
            margin-bottom: 20px !important;
            letter-spacing: -0.04em !important;
            color: var(--text-color) !important;
        }

        h2 { font-size: 2.3rem !important; margin-bottom: 1.5rem !important; font-weight: bold !important; }
        h3 { font-size: 1.8rem !important; margin-bottom: 1.2rem !important; font-weight: bold !important; }
        h4 { font-size: 1.4rem !important; font-weight: bold !important; }

        .editorial-narrative-p {
            font-size: 1.25rem !important;
            line-height: 1.7 !important;
            max-width: 950px;
            opacity: 0.88;
            margin-top: 10px;
            margin-bottom: 30px;
        }

        /* COLOR-CODED SECTIONS */
        .color-heading-controls { color: #E67E22 !important; }      
        .color-heading-directive { color: #2980B9 !important; }     
        .color-heading-directory { color: #27AE60 !important; }     
        .color-heading-investigation { color: #8E44AD !important; } 
        .color-heading-matrix { color: #D35400 !important; }        
        .color-heading-dictionary { color: #C0392B !important; }    
        .color-heading-visuals { color: #16A34A !important; }

        label[data-testid="stWidgetLabel"] p {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.04em !important;
        }

        button[data-baseweb="tab"] p {
            font-family: 'Tenor Sans', system-ui, sans-serif !important;
            font-size: 1.2rem !important;
            font-weight: bold !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.95rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            font-weight: 600 !important;
        }
        [data-testid="stMetricValue"] {
            font-family: 'Tenor Sans', system-ui, sans-serif !important;
            font-size: 3.2rem !important;
            font-weight: bold !important;
            line-height: 1 !important;
        }

        div[data-testid="stBlock"] {
            padding-bottom: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .stDataFrame {
            border: 1px solid var(--border-color) !important;
            font-size: 1.05rem !important;
        }

        .profile-inspection-dossier, .dict-box {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid var(--border-color) !important;
            padding: 30px;
            margin-top: 15px;
            font-size: 1.15rem !important;
            line-height: 1.6;
        }

        .stButton>button {
            background-color: var(--text-color) !important;
            color: var(--background-color) !important;
            border-radius: 0px !important;
            border: 1px solid var(--border-color) !important;
            font-family: 'Tenor Sans', sans-serif !important;
            font-weight: bold !important;
            font-size: 1.05rem !important;
            padding: 0.6rem 2.0rem !important;
        }

        .directive-box {
            border-left: 6px solid var(--border-color);
            padding-left: 25px;
            margin: 25px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HIGH-PERFORMANCE BACKEND PIPELINE
# ==========================================
@st.cache_data
def load_and_process_data():
    # 1. Data Loading
    activity = pd.read_csv('Customer Flight Activity.csv')
    loyalty = pd.read_csv('Customer Loyalty History.csv')
    calendar = pd.read_csv('Calendar.csv')
    
    # 2. Hierarchical Salary Imputation
    loyalty['Salary'] = loyalty['Salary'].fillna(
        loyalty.groupby(['Province', 'Education'])['Salary'].transform('median')
    )
    loyalty['Salary'] = loyalty['Salary'].fillna(
        loyalty.groupby('Education')['Salary'].transform('median')
    )
    loyalty['Salary'] = loyalty['Salary'].fillna(loyalty['Salary'].median())
    
    # 3. Feature Engineering
    # A. Member Tenure
    loyalty['tenure_months'] = (
        (loyalty['Enrollment Year'] - 2012) * 12 + loyalty['Enrollment Month']
    ).clip(lower=1)
    
    # B. Lifetime Metrics
    lifetime = activity.groupby('Loyalty Number').agg(
        lifetime_flights=('Total Flights', 'sum'),
        lifetime_distance=('Distance', 'sum'),
        active_months=('Total Flights', lambda x: (x > 0).sum()),
        total_months=('Total Flights', 'count')
    ).reset_index()
    lifetime['activity_rate'] = lifetime['active_months'] / lifetime['total_months']
    
    # C. Points & Redemptions
    pts = activity.groupby('Loyalty Number').agg(
        pts_accumulated=('Points Accumulated', 'sum'),
        pts_redeemed=('Points Redeemed', 'sum'),
        dollar_redemption=('Dollar Cost Points Redeemed', 'sum')
    ).reset_index()
    pts['redemption_rate'] = pts['pts_redeemed'] / pts['pts_accumulated'].replace(0, np.nan)
    pts['ever_redeemed'] = (pts['pts_redeemed'] > 0).astype(int)
    
    # D. Continuous Recency Assessment
    last_active = (
        activity[activity['Total Flights'] > 0]
        .groupby('Loyalty Number')
        .agg(last_year=('Year', 'max'), last_month=('Month', 'max'))
        .reset_index()
    )
    last_active['months_since_active'] = (
        (2018 - last_active['last_year']) * 12 + (12 - last_active['last_month'])
    )
    
    # E. Year-over-Year Volatility (2017 & 2018 Only)
    yearly = activity.groupby(['Loyalty Number', 'Year'])['Total Flights'].sum().reset_index()
    pivoted = yearly.pivot(index='Loyalty Number', columns='Year', values='Total Flights').fillna(0)
    for yr in [2017, 2018]:
        if yr not in pivoted.columns:
            pivoted[yr] = 0.0
    pivoted.columns = [f'Flights_{int(y)}' for y in pivoted.columns]
    
    # F. Seasonal Flight Distribution Analysis
    calendar['Date'] = pd.to_datetime(calendar['Date'])
    calendar['Month'] = calendar['Date'].dt.month
    calendar['Season'] = pd.cut(
        calendar['Month'], bins=[0, 3, 6, 9, 12], 
        labels=['Winter', 'Spring', 'Summer', 'Fall']
    )
    cal_monthly = calendar.groupby('Month')['Season'].first().reset_index()
    
    activity_season = activity.merge(cal_monthly, on='Month', how='left')
    seasonal = activity_season.groupby(['Loyalty Number', 'Season'])['Total Flights'].sum().reset_index()
    seasonal_pivot = seasonal.pivot(index='Loyalty Number', columns='Season', values='Total Flights').fillna(0)
    seasonal_pivot.columns = [f'Flights_{col}' for col in seasonal_pivot.columns]
    
    # Master DataFrame Join Setup
    df = loyalty.merge(lifetime, on='Loyalty Number', how='inner')
    df = df.merge(pts, on='Loyalty Number', how='left')
    df = df.merge(last_active[['Loyalty Number', 'months_since_active']], on='Loyalty Number', how='left')
    df = df.merge(pivoted, left_on='Loyalty Number', right_index=True, how='inner')
    df = df.merge(seasonal_pivot, left_on='Loyalty Number', right_index=True, how='left')
    
    df['months_since_active'] = df['months_since_active'].fillna(24)
    df['redemption_rate'] = df['redemption_rate'].fillna(0)
    
    # 4. Vectorized Value Matrix Sorting Logic
    salary_median = df['Salary'].median()
    clv_median = df['CLV'].median()
    
    high_salary = df['Salary'] >= salary_median
    high_clv = df['CLV'] >= clv_median
    is_married = df['Marital Status'] == 'Married'
    is_premium = df['Loyalty Card'].isin(['Aurora', 'Nova'])
    
    df['Value_Class'] = np.where(
        (high_salary & high_clv) | (high_clv & is_married) | (high_salary & is_premium),
        'Class 1 (High Value)', 'Class 2 (Low Value)'
    )
    
    # Composite Multi-Criteria Rank
    df['Value_Score'] = (
        df['CLV'].rank(pct=True) + 
        df['Salary'].rank(pct=True) + 
        df['lifetime_flights'].rank(pct=True) + 
        df['lifetime_distance'].rank(pct=True)
    ) / 4
    
    # 5. High-Performance Select Churn Grading Logic
    slope_17_18 = df['Flights_2018'] - df['Flights_2017']
    is_cancelled = df['Cancellation Year'].notna()
    is_promo_2018 = df['Enrollment Type'] == '2018 Promotion'
    is_flatline = (df['Flights_2018'] == 0) & (df['Flights_2017'] > 0)
    is_growing = slope_17_18 > 0
    is_never_flew = (df['Flights_2017'] == 0) & (df['Flights_2018'] == 0)
    
    conditions = [
        is_cancelled,
        is_promo_2018 & ~is_cancelled,
        is_never_flew & ~is_cancelled,
        is_flatline & ~is_promo_2018,
        is_growing & ~is_cancelled,
    ]
    choices = [
        'Grade D - Already Cancelled',
        'Insufficient History (2018 Promo)',
        'Grade E - Never Flew',
        'Grade A - Highly Likely',
        'Grade B - Not Likely (Growing)',
    ]
    df['Churn_Grade'] = np.select(conditions, choices, default='Grade C - Neutral')
    
    # Continuous Four-Quadrant Mapping
    recency_threshold = 6
    df['Portfolio_Segment'] = np.where(
        df['Value_Score'] >= df['Value_Score'].median(),
        np.where(df['months_since_active'] > recency_threshold, 'High Value - High Risk', 'High Value - Low Risk'),
        np.where(df['months_since_active'] > recency_threshold, 'Low Value - High Risk', 'Low Value - Low Risk')
    )
    
    return df

# Initialize Data Access Matrix Safely
try:
    df = load_and_process_data()
    
    # Title Frame Infrastructure Layout
    st.markdown("<h1><b>PASSENGER RETENTION &<br>ACCOUNT PORTFOLIO DIAGONISTIC.</b></h1>", unsafe_allow_html=True)
    st.markdown("<p class='editorial-narrative-p'><strong>Data Operations Brief — Skyward Core Analytics.</strong><br>This diagnostic workspace centralizes customer demographic metrics, year-over-year flight frequencies, and point redemption profiles across the 2017 and 2018 fiscal cycles to monitor overall portfolio health. By identifying soft-churn vulnerabilities and tracking declining booking trends, the application translates raw account data into clear, risk-adjusted workflows, providing immediate targeted retention strategies to protect high-value revenue streams.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: none; border-top: 2px solid var(--border-color); opacity: 0.15; margin-bottom: 35px;'>", unsafe_allow_html=True)

    # ==========================================
    # 4. SIDEBAR MANAGEMENT SYSTEM
    # ==========================================
    st.sidebar.markdown("<h2 class='color-heading-controls'><b>STRATEGY CONTROLS</b></h2>", unsafe_allow_html=True)

    selected_value = st.sidebar.selectbox(
        "VALUATION ARCHETYPE:",
        options=sorted(df['Value_Class'].unique())
    )
    
    selected_churn = st.sidebar.selectbox(
        "RISK GRADE PROFILE:",
        options=[
            'Grade A - Highly Likely', 
            'Grade B - Not Likely (Growing)', 
            'Grade C - Neutral', 
            'Grade D - Already Cancelled',
            'Grade E - Never Flew',
            'Insufficient History (2018 Promo)'
        ]
    )

    # Dynamic Color Routing Metrics Engine
    if 'Grade A' in selected_churn:
        urgency_color = "#E53935"      
        urgency_title = "CRITICAL INTERVENTION (URGENCY STATUS: MAXIMA)"
        sidebar_focus = "**Operational Focus:** High-Yield Rescue Mode"
        sidebar_tasks = """
        * [ ] **Priority Target:** Focus on the 25 High-Value soft-churn accounts.
        * [ ] Deploy personalized **double-points offers** on their most-flown routes within 30 days.
        * [ ] Establish a 60-day reactivation tracking window (Success Target: >= 25%).
        * [ ] Escalate selected files directly to the Executive Outreach Desk.
        
        """
    elif 'Grade C' in selected_churn or 'Grade B' in selected_churn:
        urgency_color = "#D97706"      
        urgency_title = "ELEVATED RISK MITIGATION (URGENCY STATUS: MEDIUM)"
        sidebar_focus = "**Operational Focus:** Value Protection & Relationship Upsell"
        sidebar_tasks = """
        * [ ] **Strict Protocol:** Do NOT discount (protect accounts with above-median CLV).
        * [ ] Enroll targets into a tiered engagement program with quarterly milestone rewards.
        * [ ] Monitor continuous seasonal distribution shifts to time promotional triggers.
        """
    elif 'Grade E' in selected_churn:
        urgency_color = "#2980B9"
        urgency_title = "PROACTIVE ACTIVATION (URGENCY STATUS: INACTIVE)"
        sidebar_focus = "**Operational Focus:** First-Flight Acquisition Rescue"
        sidebar_tasks = """
        * [ ] Target the **318 High-Value ghost members** whose acquisition costs are sunk.
        * [ ] Launch automated **90-day onboarding campaigns** with a first-flight bonus incentive.
        * [ ] Programmatically deprioritize profiles if zero engagement occurs within 90 days.
        
        """
    
    elif 'Grade D' in selected_churn:
        urgency_color = "#4B5563"      
        urgency_title = "HISTORICAL METRIC SURVEY (URGENCY STATUS: TERMINATED)"
        sidebar_focus = "**Operational Focus:** Automated Exit Profiling"
        sidebar_tasks = """
        * [ ] **Total Blackout:** Suppress all active promotional marketing channels immediately.
        * [ ] Route profile logs to exit survey banks to isolate structural loss metrics.
        """
    else:
        urgency_color = "#7B1FA2"
        urgency_title = "INSUFFICIENT TIMELINE BUFFER (URGENCY STATUS: PENDING)"
        sidebar_focus = "**Operational Focus:** Baseline Trend Monitoring"
        sidebar_tasks = """
        * [ ] Suppress slope delta validation anomalies.
        * [ ] Audit monthly account activity logs manually. 
        """

    st.sidebar.markdown(f"""
        <div style='border-left: 5px solid {urgency_color}; padding-left: 15px; margin: 20px 0 10px 0;'>
            <h4 style='color: {urgency_color} !important; font-family: \"Tenor Sans\", sans-serif !important; font-weight: bold !important; font-size: 1.1rem; line-height: 1.4; margin: 0;'><b>{urgency_title}</b></h4>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border-color: var(--border-color); opacity: 0.15; margin: 15px 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<h3 style='font-size: 1.25rem; margin-bottom: 5px;'><b>📋 CURRENT AUDIT SCOPE</b></h3>", unsafe_allow_html=True)
    st.sidebar.markdown(sidebar_focus)
    st.sidebar.markdown(sidebar_tasks)
        
    st.sidebar.markdown("<hr style='border-color: var(--border-color); opacity: 0.15; margin: 20px 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<h3 style='font-size: 1.15rem; margin-bottom: 5px;'><b>👤 WORKSPACE ASSIGNMENT</b></h3>", unsafe_allow_html=True)
    st.sidebar.caption("Assigned Analyst: System Core\nRegistry: SKW-PROD-2026\nData Status: Live Processing Core")

    # Segment Sorting Logic Operations
    filtered_df = df[(df['Value_Class'] == selected_value) & (df['Churn_Grade'] == selected_churn)]

    # Dynamic KPI Block Layout Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="TOTAL ACTIVE PORTFOLIO BASELINE", value=f"{len(df):,}")
    with col2:
        pipeline_risk = len(df[df['Churn_Grade'] == 'Grade A - Highly Likely'])
        st.metric(label="IMMINENT RISK PIPELINE (GRADE A)", value=f"{pipeline_risk:,}")
    with col3:
        st.metric(label="CURRENT TARGET MATCH COHORT", value=f"{len(filtered_df):,}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Workspace Tab Architecture Layout Definition
    tab1, tab2, tab3, tab4 = st.tabs([
        "📂 CAMPAIGN WORKSPACE", 
        "🔄 SIDE-BY-SIDE ACCOUNT CROSS-EXAMINATION",
        "📊 PORTFOLIO MACRO ANALYTICS",
        "📖 CORE CRITERIA DOCUMENTATION"
    ])

    # ==========================================
    # TAB 1: WORKING EXECUTIVE CANVAS
    # ==========================================
    with tab1:
        st.markdown("<h3 class='color-heading-directive'><b>STRATEGIC ACTION DIRECTIVE</b></h3>", unsafe_allow_html=True)
        st.markdown("<p class='editorial-narrative-p'>The operational directives detailed below are generated programmatically based on historic travel volumes, localized loyalty matrix variations, and projected multi-year customer lifecycles.</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='directive-box' style='border-left-color: {urgency_color} !important;'>
                <h4 style='color: {urgency_color} !important; font-family: \"Tenor Sans\", sans-serif !important; font-weight: bold !important; font-size: 1.6rem; margin-bottom: 12px;'><b>{urgency_title}</b></h4>
        """, unsafe_allow_html=True)

        # Detect the selected value class dynamically
        is_high_value = "Class 1" in selected_value

        if 'Grade A' in selected_churn:
            if is_high_value:
                st.markdown("""
                        <p class='editorial-narrative-p' style='margin: 0; font-size: 1.2rem !important;'><strong>Target Profile:</strong> Critical soft-churn account arrays. This cohort isolates 42 flatlined users, out of which 25 are ultra-premium High-Value (Class 1) accounts representing your highest-priority revenue risk.<br><br>
                        <strong>Mandatory Playbook Action:</strong> Disengage all generic automated notifications immediately to prevent brand fatigue. Route these files to specialized retention desks to deploy a personalized double-points compensation offer on their most-flown route within 30 days. Track performance metrics against a strict 60-day reactivation window; operational workflows require an execution success threshold of ≥ 25% to validate campaign ROI.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                        <p class='editorial-narrative-p' style='margin: 0; font-size: 1.2rem !important;'><strong>Target Profile:</strong> Standard soft-churn account arrays. This cohort isolates the remaining 17 lower-margin accounts showing sudden, severe flatlines in flight intervals.<br><br>
                        <strong>Mandatory Playbook Action:</strong> AUTOMATED ACCELERATOR LOOP: Trigger a low-cost, system-automated loyalty point multiplier reward package. Because baseline revenue margins are lower ($5,112.15 average CLV), restrict manual outreach pipelines and track recovery rates over a compressed 45-day window via automated transactional logging.</p>
                    </div>
                """, unsafe_allow_html=True)
                
        elif 'Grade B' in selected_churn:
            if is_high_value:
                st.markdown("""
                        <p class='editorial-narrative-p' style='margin: 0; font-size: 1.2rem !important;'><strong>Target Profile:</strong> High-performance expansion portfolio. This cohort encompasses 7,430 active members (44.4% of your total user base) displaying healthy year-over-year transactional trajectory gains.<br><br>
                        <strong>Mandatory Playbook Action:</strong> Focus efforts entirely on relationship extension and loyalty tier upselling. Enroll these accounts into your premium tiered status milestone frameworks with customized lifestyle rewards. STRICT COMPLIANCE DIRECTIVE: Do NOT introduce margin-slashing price discounts; these customers maintain an elite average CLV ($10,175.58) and must not be trained to expect devalued price drops.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                        <p class='editorial-narrative-p' style='margin: 0; font-size: 1.2rem !important;'><strong>Target Profile:</strong> Standard volume development portfolio. This cohort tracks active Class 2 accounts maintaining stable baseline activity but lower overall revenue margins.<br><br>
                        <strong>Mandatory Playbook Action:</strong> INCREMENTAL FREQUENCY STIMULATION: Unlike premium tiers, this segment is highly responsive to price elasticity. Deploy targeted entry-level fare vouchers and integrated partner promotions to increase annual flight frequency, aiming to graduate these profiles toward higher value tiers over the next fiscal cycle.</p>
                    </div>
                """, unsafe_allow_html=True)
                
        elif 'Grade C' in selected_churn:
            if is_high_value:
                st.markdown("""
                        <p class='editorial-narrative-p' style='margin: 0; font-size: 1.2rem !important;'><strong>Target Profile:</strong> Stable account arrays carrying unpredictable or plateaued travel frequencies across consecutive monitoring cycles.<br><br>
                        <strong>Mandatory Playbook Action:</strong> Mitigate risk by systematically enrolling high-value neutral accounts into an active engagement program tied to quarterly milestone rewards. Similar to your growing segments, safeguard your financial baselines by withholding baseline price cuts—incentivize retention purely through experiential milestones and non-discounted point tier bumps.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                        <p class='editorial-narrative-p' style='margin: 0; font-size: 1.2rem !important;'><strong>Target Profile:</strong> Stable lower-margin account arrays carrying unpredictable or plateaued travel frequencies across consecutive monitoring cycles.<br><br>
                        <strong>Mandatory Playbook Action:</strong> PORTFOLIO NURTURE DRIVER: Use targeted entry-level promotional flight vouchers and cross-sell network partner deals to boost interaction velocity without adding high cost. Monitor quarterly margin changes against baseline thresholds to ensure campaigns remain profitable.</p>
                    </div>
                """, unsafe_allow_html=True)
                
        elif 'Grade E' in selected_churn:
            if is_high_value:
                st.markdown("""
                        <p class='editorial-narrative-p' style='margin: 0; font-size: 1.2rem !important;'><strong>Target Profile:</strong> Dormant registrations ("Ghost Members"). This cohort consists of 573 accounts who completed enrollment but logged zero lifetime flights, including 318 high-potential profiles where customer acquisition cost is already sunk.<br><br>
                        <strong>Mandatory Playbook Action:</strong> Initialize an automated, targeted 90-day onboarding communication sequence built around an explicit, high-incentive first-flight bonus mile offer. Monitor these accounts closely for 90 days; if zero booking activity is recorded at the conclusion of this timeline, programmatically deprioritize the files to prevent wasteful outbound marketing expenditures.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                        <p class='editorial-narrative-p' style='margin: 0; font-size: 1.2rem !important;'><strong>Target Profile:</strong> Standard dormant entries. This cohort isolates the remaining 255 low-value registration profiles who have never booked an active flight sequence since account creation.<br><br>
                        <strong>Mandatory Playbook Action:</strong> DIGITAL RE-ENGAGEMENT LOOP: Initiate a basic, low-overhead 3-step automated email welcoming track using a baseline introductory mileage incentive. To protect cloud pipeline resources, programmatically archive or suppress these accounts from active tracking arrays if zero activity occurs within a compressed 60-day testing window.</p>
                    </div>
                """, unsafe_allow_html=True)
                
        else:
            # Fallback block handles both tiers identically for finalized churn statuses
            st.markdown("""
                    <p class='editorial-narrative-p' style='margin: 0; font-size: 1.2rem !important;'><strong>Target Profile:</strong> Confirmed hard-churned portfolios. This segment contains 2,067 lost members representing a structural leakage of 12.3% of your total analyzed membership base.<br><br>
                    <strong>Mandatory Playbook Action:</strong> Enforce an immediate, absolute communication blackout across all promotional, active channels to protect marketing budgets. Programmatically route these profile identifiers to your offline exit survey banks to isolate historical churn triggers and compile loss metrics without wasting further outreach capital. Retain profile identifiers only for internal historical metrics analysis.</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><h3 class='color-heading-directory'><b>COHORT DIRECTORY BREAKDOWN</b></h3>", unsafe_allow_html=True)
        st.markdown("<p class='editorial-narrative-p'>The comprehensive ledger below displays the uncompromised account records belonging to the filtered segment. Key engineered attributes like overall redemption rates and current recency indicators are included natively.</p>", unsafe_allow_html=True)
        
        display_cols = [
            'Loyalty Number', 'Province', 'City', 'Education', 'Salary', 
            'Marital Status', 'Loyalty Card', 'CLV', 'Flights_2017', 
            'Flights_2018', 'months_since_active', 'redemption_rate'
        ]
        
        st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
        
        csv_data = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="EXPORT TARGET COHORT LIST (CSV)",
            data=csv_data,
            file_name=f"Target_Segment_{selected_value.replace(' ', '_')}.csv",
            mime="text/csv"
        )

        st.markdown("<br><br><h3 class='color-heading-investigation'><b>GRANULAR ACCOUNT INVESTIGATION PANEL</b></h3>", unsafe_allow_html=True)
        st.markdown("<p class='editorial-narrative-p'>Isolate precise account lines to examine demographic criteria and multi-year transaction profiles prior to initializing direct communications.</p>", unsafe_allow_html=True)
        
        if not filtered_df.empty:
            target_account = st.selectbox("SELECT SPECIFIC USER ID TO EXPAND:", options=filtered_df['Loyalty Number'].unique())
            account_row = filtered_df[filtered_df['Loyalty Number'] == target_account].iloc[0]
            
            with st.expander(f"📂 ACCESS DETAILED ACCOUNT FILE: RECORD #{target_account}"):
                st.markdown(f"""
                    <div class='profile-inspection-dossier'>
                        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 40px;'>
                            <div>
                                <strong style='color:{urgency_color};'>📍 Geographic Demographics:</strong> {account_row['City']}, {account_row['Province']}<br>
                                <strong style='color:{urgency_color};'>🎓 Academic Attainment Level:</strong> {account_row['Education']}<br>
                                <strong style='color:{urgency_color};'>💍 Registered Relationship Status:</strong> {account_row['Marital Status']}<br>
                                <strong style='color:{urgency_color};'>💳 Active Account Program Tier:</strong> {account_row['Loyalty Card']}<br>
                                <strong style='color:{urgency_color};'>⏱️ Membership Tenure Length:</strong> {int(account_row['tenure_months'])} months
                            </div>
                            <div>
                                <strong style='color:{urgency_color};'>💰 Imputed Base Income Asset Level:</strong> ${account_row['Salary']:,.2f}<br>
                                <strong style='color:{urgency_color};'>📈 Customer Lifetime Value Index (CLV):</strong> ${account_row['CLV']:,.2f}<br>
                                <strong style='color:{urgency_color};'>🔄 Program Engagement Redemption Rate:</strong> {account_row['redemption_rate']*100:.2f}%<br>
                                <strong style='color:{urgency_color};'>🚨 Idle Timeline Counter:</strong> {int(account_row['months_since_active'])} months since active flight<br>
                                <strong style='color:{urgency_color};'>📊 Longitudinal Annual Split Volumes:</strong><br>
                                &nbsp;&nbsp;• 2017 Fiscal Cycle: {int(account_row['Flights_2017'])} flights logged<br>
                                &nbsp;&nbsp;• 2018 Fiscal Cycle: {int(account_row['Flights_2018'])} flights logged
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active profiles match current configuration models to review.")
# ==========================================
# TAB 2: SIDE-BY-SIDE CROSS EXAMINATION MATRIX
# ==========================================
    with tab2:
        st.markdown("<h3 class='color-heading-matrix'><b>SIDE-BY-SIDE CROSS-EXAMINATION MATRIX</b></h3>", unsafe_allow_html=True)
        st.markdown("<p class='editorial-narrative-p'>This transposition ledger maps distinct consumer timelines horizontally to enable structured behavioral contrast mapping across an aligned grid view.</p>", unsafe_allow_html=True)
        
        compare_targets = st.multiselect(
            "CHOOSE ACCOUNT IDENTIFIERS TO PROFILE:",
            options=df['Loyalty Number'].unique(),
            default=df['Loyalty Number'].unique()[:2] if len(df) > 2 else None
        )
        
        if compare_targets:
            compare_df = df[df['Loyalty Number'].isin(compare_targets)].copy()
            matrix_cols = [
                'Loyalty Number', 'Value_Class', 'Churn_Grade', 'Province', 'City', 
                'Education', 'Salary', 'CLV', 'tenure_months', 'lifetime_flights', 
                'months_since_active', 'redemption_rate', 'Flights_Winter', 
                'Flights_Spring', 'Flights_Summer', 'Flights_Fall'
            ]
            matrix_display = compare_df[matrix_cols].set_index('Loyalty Number').T
            st.dataframe(matrix_display, use_container_width=True)

# ==========================================
# TAB 3: VISUAL PORTFOLIO MACRO ANALYTICS
# ==========================================
    with tab3:
        st.markdown("<h3 class='color-heading-visuals'><b>PORTFOLIO MACRO ANALYTICS VISUALIZATIONS</b></h3>", unsafe_allow_html=True)
        st.markdown("<p class='editorial-narrative-p'>Interactive visualization grids ported from backend research notebooks showing distribution trends, value-by-recency matrix clusters, and redemption patterns.</p>", unsafe_allow_html=True)
        
        # Grid Row 1: Four-Quadrant Scatter Plot
        st.markdown("#### 1. Four-Quadrant Portfolio Segmentation Matrix")
        fig1, ax1 = plt.subplots(figsize=(11, 5.5))
        value_score_median = df['Value_Score'].median()
        
        sns.scatterplot(
            data=df, x='Value_Score', y='months_since_active', 
            hue='Portfolio_Segment', palette={
                'High Value - Low Risk' : '#2ecc71', 'High Value - High Risk': '#e74c3c',
                'Low Value - Low Risk'  : '#3498db', 'Low Value - High Risk' : '#f39c12'
            }, alpha=0.55, s=20, ax=ax1
        )
        ax1.axvline(value_score_median, color='grey', linestyle='--', linewidth=0.8)
        ax1.axhline(6, color='grey', linestyle=':', linewidth=0.8)
        ax1.set_xlabel("Customer Value Score (Composite Percentile Rank)")
        ax1.set_ylabel("Months Since Last Flight (Recency Risk)")
        ax1.legend(title="Portfolio Quadrant Descriptor", bbox_to_anchor=(1.01, 1))
        plt.tight_layout()
        st.pyplot(fig1)
        
        st.markdown("---")
        
        # Grid Row 2: At-Risk Metrics Split & Redemption Rate Densities
        vcol1, vcol2 = st.columns(2)
        with vcol1:
            st.markdown("#### 2. High-Value At-Risk Profile Breakdown")
            at_risk_hv = df[(df['Value_Class'] == 'Class 1 (High Value)') & (df['Churn_Grade'].isin(['Grade A - Highly Likely', 'Grade C - Neutral']))]
            
            fig2, ax2 = plt.subplots(figsize=(7, 4.5))
            at_risk_hv['Loyalty Card'].value_counts().plot(kind='bar', color=['#f39c12', '#e74c3c', '#9b59b6'], edgecolor='white', ax=ax2)
            ax2.set_ylabel("Customer Count")
            ax2.set_xlabel("Loyalty Card Tier Allocation")
            plt.xticks(rotation=0)
            plt.tight_layout()
            st.pyplot(fig2)
            
        with vcol2:
            st.markdown("#### 3. Redemption Curve Densities by Value Bracket")
            fig3, ax3 = plt.subplots(figsize=(7, 4.5))
            for label, group in df.groupby('Value_Class'):
                clean_series = group['redemption_rate'].dropna().clip(upper=0.15)
                sns.kdeplot(clean_series, label=label, fill=True, alpha=0.35, ax=ax3)
            ax3.set_xlabel("Redemption Ratio (Redeemed / Accumulated)")
            ax3.legend(title="Value Stratification Class")
            plt.tight_layout()
            st.pyplot(fig3)

        st.markdown("---")
        
        # Grid Row 3: Seasonal Flights Bar Chart
        st.markdown("#### 4. Average Seasonal Distribution Behavior Vectors")
        fig4, ax4 = plt.subplots(figsize=(10, 4))
        seasonal_cols = ['Flights_Winter', 'Flights_Spring', 'Flights_Summer', 'Flights_Fall']
        df.groupby('Value_Class')[seasonal_cols].mean().T.plot(kind='bar', color=['#2ecc71', '#e74c3c'], edgecolor='white', ax=ax4)
        ax4.set_ylabel("Mean Flights Tracked")
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig4)

# ==========================================
# TAB 4: SYSTEM METRIC DOCUMENTATION
# ==========================================
    with tab4:
        st.markdown("<h3 class='color-heading-dictionary'><b>SYSTEM CATEGORIZATION ARCHITECTURE DICTIONARY</b></h3>", unsafe_allow_html=True)
        st.markdown("<p class='editorial-narrative-p'>This documentation blueprint details the objective quantitative parameters operating inside the updated retention modeling processing pipeline.</p>", unsafe_allow_html=True)
        
        doc_col1, doc_col2 = st.columns(2)
        with doc_col1:
            st.markdown(f"""
                <div class='dict-box'>
                    <h4 style='margin-top: 0; color: #27AE60;'><b>VALUE SEGMENT ALLOCATION MATRIX (OR-GATE)</b></h4>
                    <p class='editorial-narrative-p' style='font-size: 1.15rem !important; margin-bottom: 0;'>Accounts are automatically routed into localized monetary classifications using vectorized logic across three qualifying profiles:<br><br>
                    • <strong>Class 1 (High Value):</strong> Premium high-yield customer profiles. Users must clear the dataset median base salary baseline (${df['Salary'].median():,.2f}) AND simultaneously display an elite Customer Lifetime Value index (${df['CLV'].median():,.2f}). Secondary optimization overrides automatically capture high-value married family segments or premium card variations (Aurora/Nova) regardless of baseline income markers.<br><br>
                    • <strong>Class 2 (Low Value):</strong> General customer portfolios whose tracked metrics fall outside core premium guidelines, assigning them primarily to low-resource programmatic digital automation frameworks.</p>
                </div>
            """, unsafe_allow_html=True)
            
        with doc_col2:
            st.markdown("""
                <div class='dict-box'>
                    <h4 style='margin-top: 0; color: #E67E22;'><b>CHURN RISK GRADING MECHANISMS</b></h4>
                    <p class='editorial-narrative-p' style='font-size: 1.15rem !important; margin-bottom: 0;'>Instead of monitoring formal cancellations after they occur (hard churn), this system checks continuous data patterns across a rolling cycle:<br><br>
                    • <strong>Grade A - Highly Likely:</strong> Critical soft churn risk. Maintained active flight patterns in 2017 but flatlined to zero bookings during 2018.<br><br>
                    • <strong>Grade B - Not Likely (Growing):</strong> Healthy account profiles exhibiting expanding flight volumes from 2017 to 2018.<br><br>
                    • <strong>Grade C - Neutral:</strong> Accounts displaying fluctuating or flat structural trend variances.<br><br>
                    • <strong>Grade D - Already Cancelled:</strong> Hard churn profiles possessing a processed cancellation date logged inside core servers.<br><br>
                    • <strong>Grade E - Never Flew:</strong> Ghost members who enrolled but logged zero flights across both monitoring years.</p>
                </div>
            """, unsafe_allow_html=True)

except FileNotFoundError as e:
    st.error(f"Operational Database Components Missing. Confirm that 'Customer Flight Activity.csv', 'Customer Loyalty History.csv', and 'Calendar.csv' exist inside the workspace directory.") 