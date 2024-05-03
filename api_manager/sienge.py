import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import os 


class Sienge:
    
    CURRENT = os.path.dirname(__file__)
    KEYS_FOLDER = "keys"
    SIENGE_TOKEN = os.path.join(CURRENT, KEYS_FOLDER, "sienge.json")
    
    with open(SIENGE_TOKEN, "r") as f:
        TOKEN = json.load(f)["token"]  
    
    ACCEPTED_OPERATION_TYPES = [
        "Recebimento",
        "Pagamento",
        "Adiantamento"
    ]

    ACCEPTED_COMPANIES = [1, 3, 4]


    def __init__(self):
        pass
    

    def __make_date(self, date, end=False):
        """
        Função para formatar a data.

        Parameters:
            date (str): Data  no formato "YYYYMM"
            end (bool): Se é data de fim do mês

        Returns:
            str: Data formatada.
        """

        if date == None:
            return None

        date = datetime.strptime(date, "%Y%m")

        if end:
            next_month = date.replace(day=28) + timedelta(days=4)
            date = next_month - timedelta(days=next_month.day)

        return date.strftime("%Y-%m-%d")
    

    def __get(self, endpoint, endpointType, **kwargs):
        """
        Função para realizar GET.

        Parameters:
            endpoint (str): Endpoint da API.
            endpointType (str): Tipo de endpoint (rest ou bulk).
            **kwargs: Parâmetros da query

        Returns:
            dict: Dicionário com a resposta da API.
        """

        base_urls = {
            "rest":"https://api.sienge.com.br/retrofit/public/api/v1",
            "bulk":"https://api.sienge.com.br/retrofit/public/api/bulk-data/v1"
        }

        if endpointType not in base_urls.keys():
            raise Exception("EndpointTypeError")

        if endpoint[0] != "/":
            raise Exception("EndpointError")
        
        parameters = "&".join(["{}={}".format(key, value) for key, value in kwargs.items()])

        url = base_urls[endpointType] + endpoint + "?" + parameters

        payload = {}
        headers = {
            "Authorization": f"Basic {self.TOKEN}",
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()

        return response


    def plano_financeiro(self):
        """
        Função para obter o plano financeiro.

        Returns:
            pandas.DataFrame: Plano financeiro.
        """
        endpoint = "/payment-categories"
        endpointType = "rest"

        response = self.__get(
            endpoint, 
            endpointType,
        )

        df = pd.DataFrame(response)
        df = df[["id" , "name"]]
        # df["l"] = df["id"].apply(lambda x: len(x))
        # df = df.sort_values(by=["l", "id"]).reset_index(drop=True)

        return df
    

    # def contas_a_pagar(self, startDate, endDate):
    #     """
    #     Função para obter as contas a pagar.

    #     Parameters:
    #         startDate (str): Data inicial no formato "YYYYMM".
    #         endDate (str): Data final no formato "YYYYMM".

    #     Returns:
    #         pandas.DataFrame: Contas a pagar.
    #     """

    #     # df_category = self.plano_financeiro()
    #     # plano_financeiro_categories = df_category[df_category["l"] == 3][["id", "name"]].set_index("id").to_dict(orient="index")

    #     endpoint = "/outcome"
    #     endpointType = "bulk"

    #     response = self.__get(
    #         endpoint, 
    #         endpointType, 
    #         startDate=self.__make_date(startDate), 
    #         endDate=self.__make_date(endDate, end=True),
    #         selectionType="P",
    #         correctionIndexerId=0,
    #         correctionDate=self.__make_date(startDate)
    #     )

    #     data = []

    #     for register in response["data"]:

    #         if register["companyId"] not in self.ACCEPTED_COMPANIES:
    #             continue

    #         for payment in register["payments"]:

    #             if payment["operationTypeName"] not in self.ACCEPTED_OPERATION_TYPES:
    #                 continue

    #             grossAmount = payment["grossAmount"]
    #             paymentDate = payment["paymentDate"][:7].replace("-", "")

    #             for category in register["paymentsCategories"]:
    #                 data.append({
    #                     "projectId": category["projectId"],
    #                     "projectName": category["projectName"],
    #                     "paymentDate": paymentDate,
    #                     # "financialCategoryName": plano_financeiro_categories[category["financialCategoryId"][:3]]["name"],
    #                     # "financialCategoryName": category["financialCategoryName"],
    #                     "financialCategoryId": category["financialCategoryId"],
    #                     "amount": grossAmount * category["financialCategoryRate"] / 100,
    #                 })

    #     df = pd.DataFrame(data).round(2)
    #     df = df.groupby(["projectId", "projectName", "paymentDate", "financialCategoryId"]).sum().reset_index()
        
    #     return df

    # def contas_a_pagar2(self, startDate, endDate):
    #         """
    #         Função para obter as contas a pagar.

    #         Parameters:
    #             startDate (str): Data inicial no formato "YYYYMM".
    #             endDate (str): Data final no formato "YYYYMM".

    #         Returns:
    #             pandas.DataFrame: Contas a pagar.
    #         """

    #         # df_category = self.plano_financeiro()
    #         # plano_financeiro_categories = df_category[df_category["l"] == 3][["id", "name"]].set_index("id").to_dict(orient="index")

    #         endpoint = "/outcome"
    #         endpointType = "bulk"

    #         response = self.__get(
    #             endpoint, 
    #             endpointType, 
    #             startDate=self.__make_date(startDate), 
    #             endDate=self.__make_date(endDate, end=True),
    #             selectionType="P",
    #             correctionIndexerId=0,
    #             correctionDate=self.__make_date(startDate)
    #         )

    #         data = []

    #         for register in response["data"]:

    #             if register["companyId"] not in self.ACCEPTED_COMPANIES:
    #                 continue

    #             for payment in register["payments"]:

    #                 if payment["operationTypeName"] not in self.ACCEPTED_OPERATION_TYPES:
    #                     continue

    #                 paymentDate = payment["paymentDate"][:7].replace("-", "")

    #                 for banco in payment["bankMovements"]:
    #                     amount = banco["amount"]

    #                     if banco["operationName"] == "Recebimento":
    #                         multiplicador = -1
    #                     else:
    #                         multiplicador = 1

    #                     for category in banco["paymentCategories"]:
    #                         data.append({
    #                             "bankMovementId": category["bankMovementId"],
    #                             "costCenterName": category["costCenterName"],
    #                             "paymentDate": paymentDate,
    #                             # "financialCategoryName": plano_financeiro_categories[category["financialCategoryId"][:3]]["name"],
    #                             "financialCategoryName": category["financialCategoryName"],
    #                             "financialCategoryId": category["financialCategoryId"],
    #                             "amount": multiplicador * amount * category["financialCategoryRate"] / 100,
    #                         })

    #         df = pd.DataFrame(data).round(2)
    #         df = df.groupby(["bankMovementId", "costCenterName", "financialCategoryId", "financialCategoryName"]).sum().reset_index()
            
    #         return df

    
    # def contas_a_pagar_tudo(self, startDate, endDate):
    #     """
    #     Função para obter as contas a pagar.

    #     Parameters:
    #         startDate (str): Data inicial no formato "YYYYMM".
    #         endDate (str): Data final no formato "YYYYMM".

    #     Returns:
    #         pandas.DataFrame: Contas a pagar.
    #     """

    #     # df_category = self.plano_financeiro()
    #     # plano_financeiro_categories = df_category[df_category["l"] == 3][["id", "name"]].set_index("id").to_dict(orient="index")

    #     endpoint = "/outcome"
    #     endpointType = "bulk"

    #     response = self.__get(
    #         endpoint, 
    #         endpointType, 
    #         startDate=self.__make_date(startDate),
    #         endDate=self.__make_date(endDate, end=True),
    #         selectionType="P",
    #         correctionIndexerId=0,
    #         correctionDate=self.__make_date(startDate)
    #     )

    #     data = []

    #     for register in response["data"]:

    #         if register["companyId"] not in self.ACCEPTED_COMPANIES:
    #             continue

    #         for payment in register["payments"]:

    #             grossAmount = payment["grossAmount"]
    #             paymentDate = payment["paymentDate"][:7].replace("-", "")

    #             for banco in payment["bankMovements"]:
    #                 if banco["operationName"] == "Recebimento":
    #                     multiplicador = -1
    #                 else:
    #                     multiplicador = 1

    #                 for category in banco["paymentCategories"]:
    #                     data.append({
    #                         "bankMovementId": category["bankMovementId"],
    #                         "costCenterName": category["costCenterName"],
    #                         "paymentDate": paymentDate,
    #                         # "financialCategoryName": plano_financeiro_categories[category["financialCategoryId"][:3]]["name"],
    #                         "financialCategoryName": category["financialCategoryName"],
    #                         "financialCategoryId": category["financialCategoryId"],
    #                         "amount": multiplicador * grossAmount * category["financialCategoryRate"] / 100,
    #                     })

    #     df = pd.DataFrame(data).round(2)
    #     df = df.groupby(["bankMovementId", "costCenterName", "financialCategoryId", "financialCategoryName"]).sum().reset_index()
        
    #     return df
    
    def pago(self, startDate, endDate):
        """
        Função para obter as devolucoes.

        Parameters:
            startDate (str): Data inicial no formato "YYYYMM".
            endDate (str): Data final no formato "YYYYMM".

        Returns:
            pandas.DataFrame: Contas a pagar.
        """

        # df_category = self.plano_financeiro()
        # plano_financeiro_categories = df_category[df_category["l"] == 3][["id", "name"]].set_index("id").to_dict(orient="index")

        endpoint = "/bank-movement"
        endpointType = "bulk"

        response = self.__get(
            endpoint, 
            endpointType, 
            startDate=self.__make_date(startDate),
            endDate=self.__make_date(endDate, end=True),
            # selectionType="P",
            # correctionIndexerId=0,
            # correctionDate=self.__make_date(startDate)
        )

        data = []

        for register in response["data"]:

            if register["companyId"] not in self.ACCEPTED_COMPANIES:
                continue

            for category in register["financialCategories"]:

                grossAmount = register["bankMovementAmount"]
                paymentDate = register["bankMovementDate"][:7].replace("-", "")

                if register["bankMovementOperationName"] == "Recebimento":
                    continue

                data.append({
                    "projectId": category["projectId"],
                    "projectName": category["projectName"],
                    "paymentDate": paymentDate,
                    # "financialCategoryName": plano_financeiro_categories[category["financialCategoryId"][:3]]["name"],
                    "financialCategoryName": category["financialCategoryName"],
                    "financialCategoryId": category["financialCategoryId"],
                    "amount": grossAmount * category["financialCategoryRate"] / 100,
                })

        df = pd.DataFrame(data).round(2)
        df = df.groupby(["projectId", "projectName", "financialCategoryId", "financialCategoryName", "paymentDate"]).sum().reset_index()
        
        return df

    def recebido(self, startDate, endDate):
        """
        Função para obter as devolucoes.

        Parameters:
            startDate (str): Data inicial no formato "YYYYMM".
            endDate (str): Data final no formato "YYYYMM".

        Returns:
            pandas.DataFrame: Contas a pagar.
        """

        # df_category = self.plano_financeiro()
        # plano_financeiro_categories = df_category[df_category["l"] == 3][["id", "name"]].set_index("id").to_dict(orient="index")

        endpoint = "/bank-movement"
        endpointType = "bulk"

        response = self.__get(
            endpoint, 
            endpointType, 
            startDate=self.__make_date(startDate),
            endDate=self.__make_date(endDate, end=True),
            # selectionType="P",
            # correctionIndexerId=0,
            # correctionDate=self.__make_date(startDate)
        )

        data = []

        for register in response["data"]:

            if register["companyId"] not in self.ACCEPTED_COMPANIES:
                continue

            for category in register["financialCategories"]:

                grossAmount = register["bankMovementAmount"]
                paymentDate = register["bankMovementDate"][:7].replace("-", "")

                if register["bankMovementOperationName"] != "Recebimento":
                    continue

                data.append({
                    "projectId": category["projectId"],
                    "projectName": category["projectName"],
                    "paymentDate": paymentDate,
                    "financialCategoryName": category["financialCategoryName"],
                    "financialCategoryId": category["financialCategoryId"],
                    "amount": grossAmount * category["financialCategoryRate"] / 100,
                })

        df = pd.DataFrame(data).round(2)
        df = df.groupby(["projectId", "projectName", "financialCategoryId", "financialCategoryName", "paymentDate"]).sum().reset_index()
        
        return df
    

    def contas_a_receber(self, startDate, endDate):
        """
        Função para obter as contas a receber.

        Parameters:
            startDate (str): Data inicial no formato "YYYYMM".
            endDate (str): Data final no formato "YYYYMM".
        
        Returns:
            pandas.DataFrame: Contas a receber.
        """
        endpoint = "/income"
        endpointType = "bulk"

        response = self.__get(
            endpoint, 
            endpointType, 
            startDate=self.__make_date(startDate), 
            endDate=self.__make_date(endDate, end=True),
            selectionType= "P"
        )

        data = []
    
        for register in response["data"]:

            if register["companyId"] not in self.ACCEPTED_COMPANIES:
                continue

            projectId = register["projectId"]
            projectName = register["projectName"]

            for receipt in register["receipts"]:

                if receipt["operationTypeName"] not in self.ACCEPTED_OPERATION_TYPES:
                    continue

                grossAmount = receipt["grossAmount"]
                paymentDate = receipt["paymentDate"][:7].replace("-", "")

                for category in register["receiptsCategories"]:
                    data.append({
                        "projectId": projectId,
                        "projectName": projectName,
                        "paymentDate": paymentDate,
                        "amount": grossAmount * category["financialCategoryRate"] / 100,
                    })

        df = pd.DataFrame(data).round(2)
        df = df.groupby(["projectId", "projectName", "paymentDate"]).sum().reset_index()

        return df
    

    def contas_a_receber_vencimento(self, startDate, endDate):
        """
        Função para obter as contas a receber por vencimento.

        Parameters:
            startDate (str): Data inicial no formato "YYYYMM".
            endDate (str): Data final no formato "YYYYMM".
        
        Returns:
            pandas.DataFrame: Contas a receber por vencimento.
        """

        endpoint = "/income"
        endpointType = "bulk"

        response = self.__get(
            endpoint, 
            endpointType, 
            startDate=self.__make_date(startDate), 
            endDate=self.__make_date(endDate, end=True),
            selectionType= "D"
        )

        data = []
    
        for register in response["data"]:

            if register["companyId"] not in self.ACCEPTED_COMPANIES:
                continue

            projectId = register["projectId"]
            projectName = register["projectName"]
            dueDate = register["dueDate"][:7].replace("-", "")
            grossAmount = register["originalAmount"]

            if len(register["receipts"]) == 0:

                for category in register["receiptsCategories"]:
                    data.append({
                        "projectId": projectId,
                        "projectName": projectName,
                        "dueDate": dueDate,
                        "amount": grossAmount * category["financialCategoryRate"] / 100,
                    })

            else:
                for receipt in register["receipts"]:
                    grossAmount = receipt["grossAmount"]

                    if receipt["operationTypeName"] not in self.ACCEPTED_OPERATION_TYPES:
                        continue

                    for category in register["receiptsCategories"]:
                        data.append({
                            "projectId": projectId,
                            "projectName": projectName,
                            "dueDate": dueDate,
                            "amount": grossAmount * category["financialCategoryRate"] / 100,
                        })

        df = pd.DataFrame(data).round(2)
        df = df.groupby(["projectId", "projectName", "dueDate"]).sum().reset_index()

        return df
    

    def orcamento_empresarial(self, startDate, endDate):
        """
        Função para obter o orçamento empresarial.

        Parameters:
            startDate (str): Data inicial no formato "YYYYMM".
            endDate (str): Data final no formato "YYYYMM".
        
        Returns:
            pandas.DataFrame: Orçamento empresarial.
        """

        endpoint = "/business-budget"
        endpointType = "bulk"

        response = self.__get(
            endpoint, 
            endpointType, 
            startDate=self.__make_date(startDate), 
            endDate=self.__make_date(endDate, end=True)
        )

        version = {}
        for budget in response["data"]:
            version[budget["description"]] = max(budget["versionNumber"], version.get(budget["description"], 0))

        data = []

        for budget in response["data"]:
            if budget["versionNumber"] != version[budget["description"]]:
                continue

            description = budget["description"]
            id = budget["id"]
            versionNumber = budget["versionNumber"]

            for category in budget["paymentCategories"]:
                category_id = category["id"]

                if len(category_id) != 1:
                    continue

                category_description = category["description"]
                
                for interval in category["interval"]:
                    totalPrice = interval["totalPrice"]
                    data.append({
                        "id":id,
                        "versionNumber":versionNumber,
                        "description":description,
                        "category_description": category_description,
                        "monthYear": interval["monthYear"],
                        "totalPrice": totalPrice,
                    })
        
        df = pd.DataFrame(data)
        df = df.pivot_table(index=["id", "versionNumber", "description", "monthYear"], columns="category_description", values="totalPrice", aggfunc="sum", fill_value=0).reset_index()
        df.columns.name = None
        
        return df
    
    def orcamento_planejado(self):
        """
        Função para obter as orçamentos planejados do projeto. 

        Parameters:
            None

        Returns:
            pandas.DataFrame: Orçamentos planejados.
        """

        endpoint = "/building-cost-estimation-items"
        endpointType = "bulk"

        response = self.__get(
            endpoint, 
            endpointType
        )

        data = []

        for register in response["data"]:
            
            data.append({
                "buildingId": register["buildingId"],
                "buildingName": register["buildingName"],
                "Expected": register["unitPrice"]
            })

        df = pd.DataFrame(data)
        df = df.groupby(["buildingId", "buildingName"]).sum().reset_index()
        
        return df
