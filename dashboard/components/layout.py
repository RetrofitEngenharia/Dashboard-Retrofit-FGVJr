from dash import html

def column(children, style={}):
    current_style = {
        "width": "100%",
        "height": "100%",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center",
        "gap": "0.5rem",
    }

    current_style.update(style)
    return html.Div(
        children,
        className="my_column",
        style=current_style,
    )

def row(children, style={}):
    current_style = {
        "width": "100%",
        "height": "100%",
        "display": "flex",
        "flexDirection": "row",
        "justifyContent": "center",
        "alignItems": "center",
        "gap": "0.5rem",
    }

    current_style.update(style)
    return html.Div(
        children,
        className="my_row",
        style=current_style,
    )

def container_inner(children, style={}, className="", id=""):
    current_style={
        "height": "calc(100% - 25px)",
        "width": "100%",
    }

    current_style.update(style)

    return html.Div(
        children,
        className="my_container_inner "+className,
        style=current_style,
        id=id,
    )

def container(children, id="", style={}) :
    current_style = {
        "width": "100%",
        "height": "100%",
        "borderRadius": "var(--border-radius)",
        "padding": "var(--default-padding)",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "gap": "var(--default-padding)",
    }

    current_style.update(style)
    return html.Div(
        children,
        className="my_container container-style",
        style=current_style,
        id=id,
    )

def content(children, id=""):
    return html.Div(
        children, 
        className="my_content",
        style={
            "width": "100%",
            "height": "100%",
            "display": "flex",
            "flexDirection": "column",
            "gap": "0.5rem",
        },
        id=id,
    )

def grid(children=[], style={}):
    n_columns = 6
    n_rows = 2
    current_style = {
        "display": "grid",
        "gridTemplateColumns": "1fr "*n_columns,
        "gridTemplateRows": "minmax(0, 1fr) "*n_rows,
        "gap": "var(--default-padding)",
        "height": "100%",
        "width": "100%",
    }

    current_style.update(style)
    return html.Div(
        children,
        className="my_grid",
        style=current_style
    )

