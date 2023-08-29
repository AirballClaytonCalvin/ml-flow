from datetime import datetime
from datetime import timedelta

import dash
import dash_design_kit as ddk
import dash_core_components as dcc
from dash_design_kit.Block import Block
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_pro_components as pro
import dash_cool_components as cool


FA = "https://use.fontawesome.com/releases/v5.15.2/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[FA])
server = app.server  # expose server variable for Procfile


# Tour component
tour = pro.Tour(
    id="tour",
    className="ddkProTourDefault",
    steps=[
        dict(
            selector="#gantt-block",
            content="Welcome to Dash PRO Gantt chart demonstration! Gantt charts can be easily included in your Dash apps and are highly customizable.",
            position='right'
        ),
        dict(
            selector="#gantt-chart > g.bar > g:nth-child(1)",
            content="Here's an example task. It can be dragged around, easily updated, and popup informative content.",
            position='right'
        ),
        dict(
            selector="#card-edit-gantt",
            content="The Gantt chart has many customizable properties.",
            position='right'
        ),
        dict(
            selector="#card-add-tasks",
            content="New tasks can be created from your Dash app callbacks. Go ahead, add some more tasks to your project!",
            position='right'
        ),
        dict(
            selector="#card-edit-tasks",
            content="Tasks properties are also readily customizable: name, duration, style... you can even add custom html and markdown to the popups!",
            position='right'
        ),
        dict(
            selector=".edit-theme-button",
            content="Gantt chart can be easily stylised using DDK Theme Editor. Try it out!",
            position='right'
        )
    ]
)

# Page header
page_header = ddk.Row(
    children=[
        html.H1(
            'Gantt chart with Dash PRO',
            style={
                'text-align': 'center', 'font-family': "Sans-Serif", 'font-weight': 'bold',
                'padding-right': '2rem'
            }
        ),
        html.Button(
            'Tour',
            style={
                'width': "6rem", 
                'min-width': '6rem',
                'height': '8%',
                'border-radius': '15rem',
                'font-weight': 'bold'
            },
            id='tour-btn'
        ),
        tour
    ],
    id='app-page-header',
    style={
        'margin': '0 auto', 'width': '50%',
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    }
)

# Gantt chart tasks
tasks = [
      {
        "id": 'task-1',
        "name": 'Redesign website',
        "start": '2021-08-20',
        "end": '2021-09-06',
        "progress": 20,
    },
      {
        "id": 'task-2',
        "name": 'Product release 2.0',
        "start": '2021-09-06',
        "end": '2021-09-12',
        "progress": 10,
        "dependencies": 'task-1',
    },
    {
        "id": 'task-3',
        "name": 'Contact clients',
        "start": '2021-09-06',
        "end": '2021-09-18',
        "progress": 1,
        "dependencies": 'task-1, task-2',
    },
    {
        "id": 'task-4',
        "name": 'Review contracts',
        "start": '2021-08-26',
        "end": '2021-09-08',
        "progress": 1
    }
]







# Gantt Chart
gantt_chart = ddk.Block(
    id = 'gantt-block',
    width=75,
    style={'padding': '1rem'},
    children=[
        pro.Gantt(
            id='gantt-chart',
            tasks=tasks,
            autosize_columns=False,
            task_draggable=True,
            progress_draggable=True
        )
    ]
)

app.layout = ddk.App(
    ddk.Block(
        id='main-block',
        children=[
            page_header,
            ddk.Row(
                id='row-1',
                children=[
                    
                    gantt_chart
                ]
            ),
        ]
    ),
    show_editor=True
)


# @app.callback(
#     Output('gantt-chart', 'gantt_start'),
#     [Input('timeline-start', 'value')]
# )
# def update_gantt_start(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update
#     return value

# @app.callback(
#     Output('gantt-chart', 'gantt_end'),
#     [Input('timeline-end', 'value')]
# )
# def update_gantt_start(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update
    
#     return value


# @app.callback(
#     [
#         Output('gantt-chart', 'use_custom_popup'),
#         Output('popup-textarea-form-edit', 'style'),
#         Output('popup-type-form-edit', 'style'),
#         Output('popup-textarea-form-new', 'style'),
#         Output('popup-type-form-new', 'style'),
#     ],
#     [Input('input-popup-type', 'value')]
# )
# def update_popup_type(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

#     if value == 1:
#         return bool(value), {}, {}, {}, {}
#     if value == 0:
#         return bool(value), {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    
#     return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    

# # Tour control callback
# @app.callback(
#     Output('tour', 'isOpen'), 
#     [Input('tour-btn', 'n_clicks')],
# )
# def enable_tour(n_clicks):
#     return n_clicks is not None and n_clicks > 0

# # Collapsible Edit task
# @app.callback(
#     Output("collapsible-3", "is_open"),
#     [Input('button-toggle-edit-task', "n_clicks")],
#     [State("collapsible-3", "is_open")],
# )
# def toggle_collapse_1(n, is_open):
#     if n and n > 0:
#         return not is_open
#     return is_open

# # Collapsible Add task
# @app.callback(
#     Output("collapsible-1", "is_open"),
#     [Input('button-toggle-add-task', "n_clicks")],
#     [State("collapsible-1", "is_open")],
# )
# def toggle_collapse_1(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# # Collapsible Edit Gantt
# @app.callback(
#     Output("collapsible-2", "is_open"),
#     [Input('button-toggle-edit-gantt', "n_clicks")],
#     [State("collapsible-2", "is_open")],
# )
# def toggle_collapse_2(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# # Update Add task list of dependencies
# @app.callback(
#     [
#         Output("input-new-task-dependencies", "options"),
#         Output('input-new-task-start', 'value'),
#         Output('input-new-task-end', 'value')
#     ],
#     [Input('button-toggle-add-task', "n_clicks")],
#     [State('gantt-chart', 'tasks')]
# )
# def update_task_dependencies(n, dependencies):
#     ctx = dash.callback_context
#     if not ctx.triggered or not dependencies:
#         return dash.no_update, dash.no_update, dash.no_update

#     options = [{'label': d['name'], 'value': d['id']} for d in dependencies]

#     new_default_start_date = dependencies[-1]['end']
#     new_default_end_date = datetime.strptime(new_default_start_date, '%Y-%m-%d %H:%M:%S.%f') + timedelta(3)
#     new_default_end_date = datetime.strftime(new_default_end_date, '%Y-%m-%d %H:%M:%S.%f')

#     return options, new_default_start_date, new_default_end_date

# # Update Edit task list of tasks
# @app.callback(
#     [
#         Output("select-edit-task-tasks", "options"),
#         Output('select-edit-task-tasks', 'value')
#     ],
#     [Input('button-toggle-edit-task', "n_clicks")],
#     [State('gantt-chart', 'tasks')]
# )
# def update_edit_task_tasks(n, dependencies):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update, dash.no_update
#     options = [{'label': d['name'], 'value': d['id']} for d in dependencies]
#     value = options[-1]['value']

#     return options, value

# # Update Edit task fields
# @app.callback(
#     [   
#         Output("input-edit-task-name", "value"),
#         Output("input-edit-task-progress", "value"),
#         Output("input-edit-task-start", "value"),
#         Output("input-edit-task-end", "value"),
#         Output("input-edit-task-dependencies", "options"),
#         Output("input-edit-task-dependencies", "value"),
#         Output('input-popup-type-edit', 'value'),
#         Output('input-popup-textarea-edit', 'value')
#     ],
#     [Input('select-edit-task-tasks', "value")],
#     [State('gantt-chart', 'tasks')]
# )
# def update_edit_task_fields(value, all_tasks):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

#     task = [d for d in all_tasks if d['id']==value][0]
#     dependencies_ids = task['dependencies']
#     options = [{'label': t['name'], 'value': t['id']} for t in all_tasks]
#     dep_value = [t['id'] for t in all_tasks if t['id'] in dependencies_ids]

#     popup_type = task.get('popup_type', 'markdown')
#     popup_content = task.get('popup_content', '')

#     # TODO - fix start/end datetimes updates
#     start = datetime.strptime(task['start'], "%Y-%m-%d %H:%M:%S.%f").isoformat() + "+00:00"
#     end = datetime.strptime(task['end'], "%Y-%m-%d %H:%M:%S.%f").isoformat() + "+00:00"

#     return task['name'], task['progress'], start, end, options, dep_value, popup_type, popup_content

# # Edit Gantt boolean options
# @app.callback(
#     [
#         Output('gantt-chart', 'task_draggable'),
#         Output('gantt-chart', 'progress_draggable')
#     ],
#     [Input('input-boolean-options', 'value')]
# )
# def change_gantt_booleans(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update, dash.no_update
#     output = [i in value for i in range(2)]
#     return output

# # Edit Gantt header height
# @app.callback(
#     Output('gantt-chart', 'header_height'),
#     [Input('input-header-height', 'value')]
# )
# def change_height(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update
#     return value

# # Edit Gantt arrow curve
# @app.callback(
#     Output('gantt-chart', 'arrow_curve'),
#     [Input('input-arrow-curve', 'value')]
# )
# def change_arrow_curve(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update
#     return value

# # Edit Gantt column width
# @app.callback(
#     Output('gantt-chart', 'column_width'),
#     [Input('input-column-width', 'value')]
# )
# def change_width(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update
#     return value

# # Edit Gantt bar corner radius
# @app.callback(
#     Output('gantt-chart', 'bar_corner_radius'),
#     [Input('input-bar-corner-radius', 'value')]
# )
# def change_bar_corner_radius(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update
#     return value


# # Edit Gantt bar height
# @app.callback(
#     Output('gantt-chart', 'bar_height'),
#     [Input('input-bar-height', 'value')]
# )
# def change_bar_height(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update
#     return value

# @app.callback(
#     Output('gantt-chart', 'padding'),
#     [Input('input-padding', 'value')]
# )
# def change_padding(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update
#     return value

# @app.callback(
#     Output('gantt-chart', 'view_mode'),
#     [Input('input-view-modes', 'value')]
# )
# def change_padding(value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update
#     return value


# # Update task list
# @app.callback(
#     [
#         Output("gantt-chart", "tasks"),
#         Output('button-toggle-edit-task', 'n_clicks')
#     ],
#     [
#         Input('button-add-task', "n_clicks"),
#         Input('button-update-task', "n_clicks"),
#         Input('button-delete-task', "n_clicks")
#     ],
#     [
#         State("gantt-chart", 'tasks'),
#         State("input-new-task-name", 'value'),
#         State("input-new-task-progress", 'value'),
#         State("input-new-task-start", 'value'),
#         State("input-new-task-end", 'value'),
#         State("input-new-task-dependencies", 'value'),
#         State("select-edit-task-tasks", 'value'),
#         State("input-edit-task-name", 'value'),
#         State("input-edit-task-progress", 'value'),
#         State("input-edit-task-start", 'value'),
#         State("input-edit-task-end", 'value'),
#         State("input-edit-task-dependencies", 'value'),
#         State('input-popup-textarea-edit', 'value'),
#         State('input-popup-type-edit', 'value'),
#         State('input-popup-textarea-new', 'value'),
#         State('input-popup-type-new', 'value')
#     ]
# )
# def update_task(
#     click_add, click_update, click_del, tasks_list, 
#     new_name, new_progress, new_start, new_end, new_dependencies,
#     edit_task_id, edit_name, edit_progress, edit_start, edit_end, edit_dependencies,
#     popup_content_edit, popup_type_edit, popup_content_new, popup_type_new
#     ):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update, dash.no_update

#     trigger_source = ctx.triggered[0]['prop_id'].split('.')[0]

#     if trigger_source == 'button-add-task':
#         new_task = {
#             "id": f'added-task-{click_add}',
#             "name": new_name,
#             "start": datetime.fromisoformat(new_start).strftime("%Y-%m-%d %H:%M"),
#             "end": datetime.fromisoformat(new_end).strftime("%Y-%m-%d %H:%M"),
#             "progress": new_progress,
#             "dependencies": ', '.join(new_dependencies),
#             "popup_content": popup_content_new,
#             "popup_type": popup_type_new
#         }
#         tasks_list.append(new_task)

#         return tasks_list, -1

#     if trigger_source == 'button-update-task':
#         i, edited_task = [(i, t) for i, t in enumerate(tasks_list) if t['id'] == edit_task_id][0]
#         edited_task.update({
#             'name': edit_name,
#             'progress': edit_progress,
#             'start': datetime.fromisoformat(edit_start).strftime("%Y-%m-%d %H:%M"),
#             'end': datetime.fromisoformat(edit_end).strftime("%Y-%m-%d %H:%M"),
#             'dependencies': edit_dependencies,
#             "popup_content": popup_content_edit,
#             "popup_type": popup_type_edit
#         })
#         tasks_list[i] = edited_task

#         return tasks_list, dash.no_update

#     if trigger_source == 'button-delete-task':
#         i = [i for i, t in enumerate(tasks_list) if t['id'] == edit_task_id][0]
#         del tasks_list[i]

#         return tasks_list, -1


# Run app 
if __name__ == "__main__":
    app.run_server(debug=True)