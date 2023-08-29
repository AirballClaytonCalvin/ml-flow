import dash_pro_components as pro


# Tour component
tour = pro.Tour(
    id="tour",
    className="ddkProTourDefault",
    steps=[
        dict(
            selector="#overall-app-row",
            content="Welcome to the ML Pipeline! This app demonstrates the awesome potential of Dash PRO Components: FlowChart, Tour and Ag-grid!",
            position="right",
        ),
        dict(
            selector="#card-add-nodes",
            content="Add different types of nodes for you ML pipeline. Go ahead, try adding a Dataset!",
            position="right",
        ),
        dict(
            selector="#flowchart-card",
            content="Configure your ML pipeline by connecting the nodes your own way. You can click on any node to expand its details and options.",
            position="left",
        ),
        dict(
            selector="#run-pipeline-card",
            content="Run and log each step of your ML pipeline, from data ingestion to model deployment!",
            position="top",
        ),
        dict(
            selector=".edit-theme-button",
            content="FlowChart, Tour and Ag-grid can be easily stylised using DDK Theme Editor. Try it out!",
            position="right",
        ),
    ],
)

tour_test = pro.Tour(id="tour-example", steps=[])