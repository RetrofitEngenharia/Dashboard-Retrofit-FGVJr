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

    def __set_df(self, ws_name, df):
        ws = self.sh.worksheet_by_title(ws_name)
        ws.clear()
        ws.update_values("A1", [df.columns.tolist()], extend=True)
        ws.update_values("A2", df.values.tolist(), extend=True)
        ws.adjust_column_width(start=1, end=df.shape[1])

    @property
    def orcamento_planejado(self):
        ws = self.sh.worksheet_by_title("orcamento_planejado")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    @orcamento_planejado.setter
    def orcamento_planejado(self, df):
        self.__set_df("orcamento_planejado", df)

    @property
    def orcamento_empresarial(self):
        ws = self.sh.worksheet_by_title("orcamento_empresarial")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    @orcamento_empresarial.setter
    def orcamento_empresarial(self, df):
        self.__set_df("orcamento_empresarial", df)

    # @property
    # def contas_a_pagar(self):
    #     ws = self.sh.worksheet_by_title("contas_a_pagar")
    #     return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    # @contas_a_pagar.setter
    # def contas_a_pagar(self, df):
    #     self.__set_df("contas_a_pagar", df)

    # @property
    # def contas_a_pagar2(self):
    #     ws = self.sh.worksheet_by_title("contas_a_pagar2")
    #     return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    # @contas_a_pagar2.setter
    # def contas_a_pagar2(self, df):
    #     self.__set_df("contas_a_pagar2", df)

    # @property
    # def contas_a_pagar_tudo(self):
    #     ws = self.sh.worksheet_by_title("contas_a_pagar_tudo")
    #     return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    # @contas_a_pagar_tudo.setter
    # def contas_a_pagar_tudo(self, df):
    #     self.__set_df("contas_a_pagar_tudo", df)

    @property
    def pago(self):
        ws = self.sh.worksheet_by_title("pago")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    @pago.setter
    def pago(self, df):
        self.__set_df("pago", df)

    @property
    def recebido(self):
        ws = self.sh.worksheet_by_title("recebido")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    @recebido.setter
    def recebido(self, df):
        self.__set_df("recebido", df)

    @property
    def contas_a_receber(self):
        ws = self.sh.worksheet_by_title("contas_a_receber")
        return ws.get_as_df(value_render=self.VALUE_RENDER)

    @contas_a_receber.setter
    def contas_a_receber(self, df):
        self.__set_df("contas_a_receber", df)

    @property
    def contas_a_receber_vencimento(self):
        ws = self.sh.worksheet_by_title("contas_a_receber_vencimento")
        return ws.get_as_df(value_render=self.VALUE_RENDER)

    @contas_a_receber_vencimento.setter
    def contas_a_receber_vencimento(self, df):
        self.__set_df("contas_a_receber_vencimento", df)
    

    @property
    def projectId_description_non_related(self):
        ws = self.sh.worksheet_by_title("projectId_description_non_related")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    @projectId_description_non_related.setter
    def projectId_description_non_related(self, df):
        self.__set_df("projectId_description_non_related", df)

    @property
    def plano_financeiro(self):
        ws = self.sh.worksheet_by_title("plano_financeiro")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    @plano_financeiro.setter
    def plano_financeiro(self, df):
        self.__set_df("plano_financeiro", df)
