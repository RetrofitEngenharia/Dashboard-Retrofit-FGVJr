import sys
import pandas as pd
import datetime
import Levenshtein
import logging
import os

from sheets import Sheets
from sienge import Sienge

pd.options.display.float_format = '{:,.2f}'.format
today = datetime.date.today().strftime("%Y-%m-%d")
logging.basicConfig(
    filename = os.path.join(os.path.dirname(__file__), "log",f"{today}.log"),
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

class ApiManager:

    START_DATE = "2019-08-01"
    DELTA_DAYS_MORE = int(365 * 1.5)
    DELTA_DAYS_LESS = 15

    def __init__(self):
        logger.info("Starting ApiManager")
        self.sheets = Sheets()
        self.sienge = Sienge()

        self.projects = {}
        self.descriptions = {}


    def __make_date(self, date):
        """
        Recebe uma data e retorna no formato YYYYMM
        """

        if isinstance(date, datetime.date):
            return date.strftime("%Y%m")
        elif isinstance(date, str):
            return date[:7].replace("-", "")
        else:
            raise Exception("InvalidType")
        
    
    def __get_projects(self, df):
        """
        Recebe um dataframe com as colunas projectId e projectName
        e atualiza o atributo projects

        Parameters:
            df (pd.DataFrame): Dataframe com a coluna description
        """

        uniques = df[["projectId", "projectName"]].drop_duplicates().to_dict("records")

        for row in uniques:
            if row["projectName"] not in self.projects:
                self.projects[row["projectName"]] = row


    def __get_descriptions(self, df):
        """
        Recebe um dataframe com as colunas descriptionId e descriptionName
        e atualiza o atributo descriptions

        Parameters:
            df (pd.DataFrame): Dataframe com a coluna description
        """

        self.descriptions = {x:{} for x in df["description"].unique()}


    def __generate_correlate_projects_description(self, df):
        logger.info("Starting correlate_projects_description")
        
        correlation = {}

        # Correlação direta
        added = []
        for description in self.descriptions.keys():
            if description in self.projects:
                correlation[description] = self.projects[description]
                correlation[description]["description"] = description
                added.append(description)
                self.projects.pop(description)
        for add in added: self.descriptions.pop(add)

        # strip
        self.projects = {x["projectName"].strip():x for x in self.projects.values()}
        added = []
        for description in self.descriptions.keys():
            if description in self.projects:
                correlation[description] = self.projects[description]
                correlation[description]["description"] = description
                added.append(description)
                self.projects.pop(description)
        for add in added: self.descriptions.pop(add)

        # Correlação por similaridade
        added = []
        for description in self.descriptions.keys():
            for projectName, project in self.projects.items():
                if Levenshtein.distance(description, project["projectName"]) < 5:
                    correlation[description] = project
                    correlation[description]["description"] = description
                    self.projects.pop(projectName)
                    added.append(description)
                    break
        for add in added: self.descriptions.pop(add)

        df_non_related_projects = pd.DataFrame(self.projects.values())
        df_non_related_descriptions = pd.DataFrame(self.descriptions.keys(), columns=["description"])
        
        df_non_related = pd.concat([df_non_related_projects, df_non_related_descriptions], axis=0).fillna("")
        self.sheets.projectId_description_non_related = df_non_related
        del df_non_related

        df_correlation = pd.DataFrame(correlation.values())

        return pd.merge(df, df_correlation, on='description', how='left').fillna("")
    

    
    def __set_plano_financeiro(self):
        logger.info("Starting plano_financeiro")
        df = self.sienge.plano_financeiro()
        df = df.sort_values(by="id")
        self.sheets.plano_financeiro = df
        
    
        
    # def __set_contas_a_pagar(self, startDate, endDate, df_old=None):
    #     logger.info("Starting contas_a_pagar")
    #     df = self.sienge.contas_a_pagar(startDate, endDate)
    #     plano_financeiro = self.sheets.plano_financeiro

    #     plano_financeiro["l"] = plano_financeiro["id"].apply(lambda x: len(str(x)))
    #     plano_financeiro = plano_financeiro.loc[plano_financeiro["l"] == 3]
    #     plano_financeiro.drop(columns=["l"], inplace=True)

    #     df["financialCategoryName"] = df["financialCategoryId"].apply(lambda x: plano_financeiro.loc[plano_financeiro["id"]==int(str(x)[:3]), "name"].max())

    #     if df_old is not None:
    #         df_old["paymentDate"] = df_old["paymentDate"].astype(str)
    #         df_old = df_old[df_old["paymentDate"] < startDate]
    #         df = pd.concat([df_old, df], axis=0)

    #     self.__get_projects(df)

    #     self.sheets.contas_a_pagar = df


    # def __set_contas_a_pagar2(self, startDate, endDate, df_old=None):
    #     logger.info("Starting contas_a_pagar2")
    #     df = self.sienge.contas_a_pagar2(startDate, endDate)

    #     plano_financeiro = self.sheets.plano_financeiro



    #     plano_financeiro["l"] = plano_financeiro["id"].apply(lambda x: len(str(x)))
    #     plano_financeiro = plano_financeiro.loc[plano_financeiro["l"] == 3]
    #     plano_financeiro.drop(columns=["l"], inplace=True)

    #     df["financialCategoryName"] = df["financialCategoryId"].apply(lambda x: plano_financeiro.loc[plano_financeiro["id"]==int(str(x)[:3]), "name"].max())

    #     if df_old is not None:
    #         df_old["paymentDate"] = df_old["paymentDate"].astype(str)
    #         df_old = df_old[df_old["paymentDate"] < startDate]
    #         df = pd.concat([df_old, df], axis=0)


    #     self.sheets.contas_a_pagar2 = df
    
    # def __set_contas_a_pagar_tudo(self, startDate, endDate, df_old=None):
    #     logger.info("Starting contas_a_pagar_tudo")
    #     df = self.sienge.contas_a_pagar_tudo(startDate, endDate)

    #     plano_financeiro = self.sheets.plano_financeiro

    #     plano_financeiro["l"] = plano_financeiro["id"].apply(lambda x: len(str(x)))
    #     plano_financeiro = plano_financeiro.loc[plano_financeiro["l"] == 3]
    #     plano_financeiro.drop(columns=["l"], inplace=True)

    #     df["financialCategoryName"] = df["financialCategoryId"].apply(lambda x: plano_financeiro.loc[plano_financeiro["id"]==int(str(x)[:3]), "name"].max())

    #     if df_old is not None:
    #         df_old["paymentDate"] = df_old["paymentDate"].astype(str)
    #         df_old = df_old[df_old["paymentDate"] < startDate]
    #         df = pd.concat([df_old, df], axis=0)


    #     self.sheets.contas_a_pagar_tudo = df

    def __set_pago(self, startDate, endDate, df_old=None):
        logger.info("Starting pago")
        df = self.sienge.pago(startDate, endDate)

        plano_financeiro = self.sheets.plano_financeiro

        plano_financeiro["l"] = plano_financeiro["id"].apply(lambda x: len(str(x)))
        plano_financeiro = plano_financeiro.loc[plano_financeiro["l"] == 3]
        plano_financeiro.drop(columns=["l"], inplace=True)

        # df["financialCategoryName"] = df["financialCategoryId"].apply(lambda x: plano_financeiro.loc[plano_financeiro["id"]==int(str(x)[:3]), "name"].max())

        if df_old is not None:
            df_old["paymentDate"] = df_old["paymentDate"].astype(str)
            df_old = df_old[df_old["paymentDate"] < startDate]
            df = pd.concat([df_old, df], axis=0)


        self.sheets.pago = df
    
    def __set_recebido(self, startDate, endDate, df_old=None):
        logger.info("Starting recebido")
        df = self.sienge.recebido(startDate, endDate)

        plano_financeiro = self.sheets.plano_financeiro

        plano_financeiro["l"] = plano_financeiro["id"].apply(lambda x: len(str(x)))
        plano_financeiro = plano_financeiro.loc[plano_financeiro["l"] == 3]
        plano_financeiro.drop(columns=["l"], inplace=True)

        # df["financialCategoryName"] = df["financialCategoryId"].apply(lambda x: plano_financeiro.loc[plano_financeiro["id"]==int(str(x)[:3]), "name"].max())

        if df_old is not None:
            df_old["paymentDate"] = df_old["paymentDate"].astype(str)
            df_old = df_old[df_old["paymentDate"] < startDate]
            df = pd.concat([df_old, df], axis=0)


        self.sheets.recebido = df

    def __set_contas_a_receber(self, startDate, endDate, df_old=None):
        logger.info("Starting contas_a_receber")
        df = self.sienge.contas_a_receber(startDate, endDate)

        if df_old is not None:
            df_old["paymentDate"] = df_old["paymentDate"].astype(str)
            df_old = df_old[df_old["paymentDate"] < startDate]
            df = pd.concat([df_old, df], axis=0)

        self.__get_projects(df)
        
        self.sheets.contas_a_receber = df

    
    def __set_contas_a_receber_vencimento(self, startDate, endDate, df_old=None):
        logger.info("Starting contas_a_receber_vencimento")
        df = self.sienge.contas_a_receber_vencimento(startDate, endDate)

        if df_old is not None:
            df_old["dueDate"] = df_old["dueDate"].astype(str)
            df_old = df_old[df_old["dueDate"] < startDate]
            df = pd.concat([df_old, df], axis=0)

        self.__get_projects(df)

        self.sheets.contas_a_receber_vencimento = df


    def __set_orcamento_empresarial(self, endDate):
        logger.info("Starting orcamento_empresarial")
        df_orcamento_empresarial = self.sienge.orcamento_empresarial("200001", endDate)

        self.__get_descriptions(df_orcamento_empresarial)
        df_orcamento_empresarial = self.__generate_correlate_projects_description(df_orcamento_empresarial)

        self.sheets.orcamento_empresarial = df_orcamento_empresarial

    def __set_orcamento_planejado(self):
        logger.info("Starting orcamento_planejado")
        df_orcamento_planejado = self.sienge.orcamento_planejado()

        # self.__get_descriptions(df_orcamento_planejado)
        # df_orcamento_planejado = self.__generate_correlate_projects_description(df_orcamento_planejado)

        self.sheets.orcamento_planejado = df_orcamento_planejado

    def start(self):
        logger.info("Starting start")

        self.__set_plano_financeiro()

        startDate = self.__make_date(self.START_DATE)
        endDate = self.__make_date(datetime.date.today())

        # self.__set_contas_a_pagar(startDate, endDate)
        # self.__set_contas_a_pagar2(startDate, endDate)
        # self.__set_contas_a_pagar_tudo(startDate, endDate)
        self.__set_pago(startDate, endDate)
        self.__set_recebido(startDate, endDate)
        self.__set_contas_a_receber(startDate, endDate)
        
        endDate = self.__make_date(datetime.date.today() + datetime.timedelta(days=self.DELTA_DAYS_MORE))

        self.__set_contas_a_receber_vencimento(startDate, endDate)
        self.__set_orcamento_empresarial(endDate)

        self.__set_orcamento_planejado()
        

    def update(self):
        logger.info("Starting update")

        self.__set_plano_financeiro()

        startDate = self.__make_date(datetime.date.today() - datetime.timedelta(days=self.DELTA_DAYS_LESS))
        endDate = self.__make_date(datetime.date.today())

        # self.__set_contas_a_pagar(startDate, endDate, self.sheets.contas_a_pagar)
        # self.__set_contas_a_pagar2(startDate, endDate, self.sheets.contas_a_pagar2)
        # self.__set_contas_a_pagar_tudo(startDate, endDate, self.sheets.contas_a_pagar_tudo)
        self.__set_pago(startDate, endDate, self.sheets.pago)
        self.__set_recebido(startDate, endDate, self.sheets.recebido)

        self.__set_contas_a_receber(startDate, endDate, self.sheets.contas_a_receber)

        endDate = self.__make_date(datetime.date.today() + datetime.timedelta(days=self.DELTA_DAYS_MORE))

        self.__set_contas_a_receber_vencimento(startDate, endDate, self.sheets.contas_a_receber_vencimento)
        self.__set_orcamento_empresarial(endDate)

        self.__set_orcamento_planejado()


    def update_orcamento_empresarial(self):
        logger.info("Starting update_orcamento_empresarial")

        self.__get_projects(self.sheets.contas_a_pagar)
        self.__get_projects(self.sheets.contas_a_receber)
        self.__get_projects(self.sheets.contas_a_receber_vencimento)
        self.__get_projects(self.sheets.orcamento_planejado)

        endDate = self.__make_date(datetime.date.today() + datetime.timedelta(days=self.DELTA_DAYS_MORE))

        self.__set_orcamento_empresarial(endDate)


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        logger.error("MissingCommand")
        raise Exception("MissingCommand")
 
    if sys.argv[1] == "update":
        logger.info(" main.py update")
        api_manager = ApiManager()
        api_manager.update()
        logger.info("Finished update")
    elif sys.argv[1] == "start":
        logger.info(" main.py start")
        api_manager = ApiManager()
        api_manager.start()
        logger.info("Finished start")
    elif sys.argv[1] == "update_orcamento_empresarial":
        logger.info(" main.py update_orcamento_empresarial")
        api_manager = ApiManager
        api_manager.update_orcamento_empresarial()
        logger.info("Finished update_orcamento_empresarial")
    else:
        raise Exception("CommandNotFound")
        