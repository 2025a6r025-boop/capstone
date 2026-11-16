from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data/processed/launches_model.csv"
if not FILE.exists():
    raise SystemExit("Run the notebook first to create data/processed/launches_model.csv")
df = pd.read_csv(FILE)
app = Dash(__name__)
sites = sorted(df.launchpad.dropna().astype(str).unique())
app.layout = html.Div([
    html.H1("SpaceX Falcon 9 Launch Analytics"),
    dcc.Dropdown(id="site", options=[{"label":"All sites","value":"ALL"}] +
                 [{"label":s,"value":s} for s in sites], value="ALL", clearable=False),
    dcc.Graph(id="outcomes"), dcc.Graph(id="payload")
])
@app.callback(Output("outcomes","figure"), Output("payload","figure"), Input("site","value"))
def update(site):
    d = df if site == "ALL" else df[df.launchpad.astype(str) == site]
    counts = d.landing_success.value_counts(dropna=False).rename_axis("outcome").reset_index(name="count")
    fig1 = px.pie(counts, names="outcome", values="count", title="Landing outcomes")
    fig2 = px.scatter(d, x="payload_mass_kg", y="landing_success",
                      title="Payload mass versus landing outcome")
    return fig1, fig2
if __name__ == "__main__":
    app.run(debug=True)
