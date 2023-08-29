import dash
import dash_design_kit as ddk
import dash_pro_components as pro

styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}

tree_data = [
    {
        "title": "United States",
        "expanded": True,
        "children": [
            {
                "title": "California",
                "subtitle": "CA",
                "children": [
                    {"title": "San Francisco", "subtitle": "SF"},
                    {"title": "San Diego"},
                ],
            }
        ],
    },
    {
        "title": "Canada",
        "children": [
            {"title": "Quebec", "children": [{"title": "Montreal", "subtitle": "MTL"}]},
            {"title": "Ontario", "subtitle": "ON"},
        ],
    },
]

app = dash.Dash(__name__)
server = app.server

app.layout = ddk.App(
    show_editor=True,
    children=[
        ddk.Row(
            [
                ddk.Block(
                    width=50,
                    children=[
                        ddk.Card(
                            [
                                ddk.CardHeader(
                                    title="TreeView Component",
                                ),
                                pro.TreeView(
                                    id="treeview",
                                    treeData=tree_data,
                                    className="custom-treeview",
                                    style={"height": "400px"},
                                ),
                            ]
                        ),
                    ],
                )
            ]
        )
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)