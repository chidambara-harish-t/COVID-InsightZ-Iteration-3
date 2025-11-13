import pandas as pd
import plotly.express as px


def plot_top10_px(latest_totals: pd.Series):
    """Plot top 10 regions by total cases (Plotly)."""
    import plotly.express as px
    import pandas as pd

    latest_totals = pd.to_numeric(latest_totals, errors="coerce").dropna()

    if latest_totals.empty:
        return px.bar(title="No valid data to display")

    # Convert to DataFrame
    df = (
        latest_totals
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    if df.shape[1] == 2:
        df.columns = ["Region", "Total"]
    elif df.shape[1] == 3:
        df.columns = ["Country", "Province", "Total"]
        df["Region"] = df.apply(
            lambda r: f"{r['Country']} - {r['Province']}"
            if pd.notna(r["Province"]) and str(r["Province"]).lower() != "nan"
            and r["Province"] != r["Country"]
            else r["Country"],
            axis=1
        )
    else:
        df["Region"] = df.iloc[:, 0].astype(str)

    fig = px.bar(
        df,
        x="Region",
        y="Total",
        title="Top 10 Regions by Total Cases",
        labels={"Total": "Total Cases"},
        text="Total"
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(xaxis_tickangle=-30, height=420, margin=dict(l=10, r=10, t=30, b=30))
    return fig



def plot_daily_px(df: pd.DataFrame, countries: list[tuple[str, str]]):
    """Plot daily confirmed cases for selected countries/provinces (Plotly)."""
    plot_df = pd.DataFrame({
        "Date": df[("Date", "")],
    })

    # Select regions
    for c in countries:
        label = f"{c[0]} - {c[1]}" if c[1] and c[1] != c[0] else c[0]
        plot_df[label] = pd.to_numeric(df[c], errors="coerce")

    plot_df = plot_df.melt(id_vars="Date", var_name="Region", value_name="Cases")

    fig = px.line(
        plot_df,
        x="Date",
        y="Cases",
        color="Region",
        title="Daily COVID-19 Confirmed Cases",
        hover_data={"Date": "|%Y-%m-%d", "Cases": ":,"}
    )
    fig.update_layout(legend_title_text="Region", height=500)
    return fig


def plot_global_px(df: pd.DataFrame):
    """Plot global confirmed cases over time (Plotly)."""
    import plotly.express as px
    import pandas as pd

    if isinstance(df.columns, pd.MultiIndex):
        df_flat = df.copy()
        df_flat.columns = ['_'.join(filter(None, map(str, col))).strip() for col in df.columns]
    else:
        df_flat = df.copy()

    if "Date" not in df_flat.columns:
        df_flat = df_flat.rename(columns={"Date_": "Date"})
    if "GlobalCases" not in df_flat.columns and "GlobalCases_" in df_flat.columns:
        df_flat = df_flat.rename(columns={"GlobalCases_": "GlobalCases"})

    df_flat = df_flat.dropna(subset=["Date", "GlobalCases"])

    fig = px.line(
        df_flat,
        x="Date",
        y="GlobalCases",
        title="Global COVID-19 Confirmed Cases Over Time",
        hover_data={"Date": "|%Y-%m-%d", "GlobalCases": ":,"},
        color_discrete_sequence=["#1f77b4"]
    )
    fig.update_layout(height=500, xaxis_title="Date", yaxis_title="Confirmed Cases")
    return fig