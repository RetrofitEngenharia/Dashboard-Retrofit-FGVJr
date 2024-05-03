import numpy as np

def real(value, size=None):
    form = f'{value:,.2f}'.replace(',', '.').rsplit('.', 1)
    form = ",".join(form)
    
    if size:
        form = form.rjust(size)

    return "R$ " + form

def perc(value, size=6, ready=False):
    value = value * 100.0 if not ready else value
    form = f'{value:,.2f}'.replace(',', '.').rsplit('.', 1)
    form = ",".join(form)
    
    if size:
        form = form.rjust(size)

    return form + " %"
