import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, State, no_update, callback_context, MATCH
import uuid


class SlidesComponent(html.Div):
    # TODO - improve pattern matching association with external components
    # TODO - include options for fade/slide effects (have to do it with css)
    # TODO - re-write as a proper All-in-one component: https://dash.plotly.com/all-in-one-components
    # TODO - document usage with docstring and a better example app
    # TODO - maybe release as a pro Component
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.store = dcc.Store(
            # id={'component': 'slides-component', 'subcomponent': 'store', 'id': self.id}, 
            id=f'slides-component-store-{self.id}', 
            data=0
        )
        self.parent_app = kwargs.pop('parent_app')
        slides = kwargs.pop('slides')
        self.slides = [
            html.Div(sl, className='slide') 
            for sl in slides
        ]
        self.trigger_first_slide_id = kwargs.pop('trigger_first_slide_id', 'trigger-first-slide')
        self.trigger_previous_slide_id = kwargs.pop('trigger_previous_slide_id', 'trigger-previous-slide')
        self.trigger_next_slide_id = kwargs.pop('trigger_next_slide_id', 'trigger-next-slide')
        self.trigger_last_slide_id = kwargs.pop('trigger_last_slide_id', 'trigger-last-slide')
        button_style = style={
            'width': '65px',
            "border-radius": ".5rem",
            "font-weight": "bold",
        }
        self.controls = dbc.Row(
            children=[
                dbc.Col(
                    html.Button(
                        "|<", 
                        id="trigger-first-slide",
                        style=button_style
                    ),
                    style={'padding': '2px'}
                ),
                dbc.Col(
                    html.Button(
                        "<", 
                        id="trigger-previous-slide",
                        style=button_style
                    ),
                    style={'padding': '2px'}
                ),
                dbc.Col(
                    html.Button(
                        ">", 
                        id="trigger-next-slide",
                        style=button_style
                    ),
                    style={'padding': '2px'}
                ),
                dbc.Col(
                    html.Button(
                        ">|", 
                        id="trigger-last-slide",
                        style=button_style
                    ),
                    style={'padding': '2px'}
                ),
                dbc.Col(
                    dbc.Label(
                        f"slide 1 of {len(self.slides)}", 
                        # id={'component': 'slides-component', 'subcomponent': 'label-slide-number', 'id': self.id}, 
                        id=f'slides-component-label-slide-number-{self.id}', 
                        style={'width': '90px', 'color': 'gray', 'paddingTop': '8px'}
                    ),
                    style={'padding': '2px', 'paddingLeft': '30px'}
                )
            ], 
            style={'width': '400px', 'padding': '1px', 'paddingBottom': '25px'},
            justify="start"
        )

        self.page = html.Div(
            children=self.slides[0],
            # id={'component': 'slides-component', 'subcomponent': 'page', 'id': self.id}, 
            id=f'slides-component-page-{self.id}', 
        )
        
        super().__init__(**kwargs)
        self.children = [
            self.store,
            dbc.Card([
                dbc.CardBody([
                    self.controls,
                    self.page
                ])
            ]),
            html.Div(id='useless')
        ]

        @self.parent_app.callback(
            [
                # Output({'component': 'slides-component', 'subcomponent': 'page', 'id': MATCH}, "children"), 
                # Output({'component': 'slides-component', 'subcomponent': 'store', 'id': MATCH}, "data"),
                # Output({'component': 'slides-component', 'subcomponent': 'label-slide-number', 'id': MATCH}, "children")
                Output(f'slides-component-page-{self.id}', "children"), 
                Output(f'slides-component-store-{self.id}', "data"),
                Output(f'slides-component-label-slide-number-{self.id}', "children")
            ],
            [   
                Input(self.trigger_first_slide_id, "n_clicks"),
                Input(self.trigger_previous_slide_id, "n_clicks"),
                Input(self.trigger_next_slide_id, "n_clicks"),
                Input(self.trigger_last_slide_id, "n_clicks")
            ],
            [
                # State({'component': 'slides-component', 'subcomponent': 'store', 'id': MATCH}, 'data')
                State(f'slides-component-store-{self.id}', 'data')
            ],
            prevent_initial_call=True,
        )
        def change_slide(first, previous, next, last, slide_number):
            ctx = callback_context
            if not ctx.triggered:
                return no_update, no_update, no_update
            else:
                trigger = ctx.triggered[0]['prop_id'].split('.')[0]

            if trigger == self.trigger_first_slide_id:
                slide_number = 0

            if trigger == self.trigger_previous_slide_id:
                slide_number -= 1
                if slide_number < 0:
                    slide_number = len(self.slides) - 1

            if trigger == self.trigger_next_slide_id:
                slide_number += 1
                if slide_number >= len(self.slides):
                    slide_number = 0

            if trigger == self.trigger_last_slide_id:
                slide_number = len(self.slides) - 1

            return self.slides[slide_number], slide_number, f"slide {slide_number + 1} of {len(self.slides)}"
            # return slide_number, f"slide {slide_number + 1} of {len(self.slides)}"


        # # Changes visibility on clientside
        # self.parent_app.clientside_callback(
        #     """
        #     function(data, slides) {
        #         console.log(data)
        #         console.log(slides)
        #     }
        #     """,
        #     Output('useless', 'children'),
        #     [
        #         Input(f'slides-component-store-{self.id}', 'data'),
        #         Input(f'slides-component-page-{self.id}', 'children')
        #     ]
        # )
