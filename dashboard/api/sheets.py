import os.path
import pandas as pd
import pygsheets

SPREADSHEET_TITLE = "Dados Dashboard"

class Sheets:

    CURRENT = os.path.dirname(__file__)
    KEYS_FOLDER = "keys"
    SERVICE_ACCOUNT_CREDENTIALS = os.path.join(CURRENT, KEYS_FOLDER, "service_account_credentials.json")
    VALUE_RENDER = pygsheets.ValueRenderOption.UNFORMATTED_VALUE

    def __init__(self):
        self.gc = pygsheets.authorize(
            service_file=self.SERVICE_ACCOUNT_CREDENTIALS
        )
        self.sh = self.gc.open(SPREADSHEET_TITLE)

    @property
    def orcamento_empresarial(self):
        ws = self.sh.worksheet_by_title("orcamento_empresarial")
        return ws.get_as_df(value_render=self.VALUE_RENDER)

    @property
    def contas_a_pagar(self):
        ws = self.sh.worksheet_by_title("contas_a_pagar")
        return ws.get_as_df(value_render=self.VALUE_RENDER)

    @property
    def pago(self):
        ws = self.sh.worksheet_by_title("pago")
        return ws.get_as_df(value_render=self.VALUE_RENDER)

    @property
    def recebido(self):
        ws = self.sh.worksheet_by_title("recebido")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    @property
    def contas_a_receber(self):
        ws = self.sh.worksheet_by_title("contas_a_receber")
        return ws.get_as_df(value_render=self.VALUE_RENDER)

    @property
    def contas_a_receber_vencimento(self):
        ws = self.sh.worksheet_by_title("contas_a_receber_vencimento")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    @property
    def plano_financeiro(self):
        ws = self.sh.worksheet_by_title("plano_financeiro")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    



        
        
