

from typing import Any, List
from ipywidgets import widgets, Layout
from IPython import display

def display_inline(*tables: Any):
    table_widgets: List[widgets.Output] = []
    for _ in range(0, len(tables)):
        table_widgets.append(widgets.Output())

    for i, widget in enumerate(table_widgets):
        with widget:
            display.display(tables[i])
            tables[i].info()

    box_layout = Layout(display='flex',
        flex_flow='row',
        justify_content='space-around',
        width='auto'
    )

    hbox = widgets.HBox(table_widgets, layout=box_layout)  # type: ignore

    return hbox