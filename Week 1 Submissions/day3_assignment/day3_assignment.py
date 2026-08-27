import numpy as np
import pandas as pd

def marks_calcucations(marks):
    marks_array = np.array(marks)
    return {
        "mean": np.mean(marks_array),
        "median": np.median(marks_array),
        "min": np.min(marks_array),
        "max": np.max(marks_array)
    }

def create_data():
    # | ProductName | Category | QuantitySold | UnitPrice | Region |
    # | --- | --- | ---: | ---: | --- |
    # | Leather Recliner | Recliners | 12 | 500 | North America |
    # | Fabric Recliner | Recliners | 8 | 400 | Europe |
    # | Sectional Sofa | Sofas | 15 | 700 | North America |
    # | Sleeper Sofa | Sofas | 5 | 650 | Europe |


    json_array = [
        {"ProductName":"Leather Recliner","Category":"Recliner","QuantitySold":12,"UnitPrice":500,"Region":"North America"},
        {"ProductName":"Leather Recliner","Category":"Recliner","QuantitySold":8,"UnitPrice":400,"Region":"Europe"},
        {"ProductName":"Leather Recliner","Category":"Recliner","QuantitySold":15,"UnitPrice":700,"Region":"North America"},
        {"ProductName":"Leather Recliner","Category":"Recliner","QuantitySold":5,"UnitPrice":650,"Region":"Europe"}
    ]
    return pd.DataFrame(json_array)

def filtered_products(sales_data,min_quantity_sold):
    return sales_data[sales_data["QuantitySold"]>min_quantity_sold]

def regional_sales(sales_data):
    return sales_data.groupby("Region").apply(
        lambda p: pd.Series({
            'Total Revenue':(p["QuantitySold"]*p["UnitPrice"]).sum()
        })
    ).reset_index()

if __name__ ==  "__main__":
    data = create_data()
    print(data)
    print(regional_sales(data))
    print(filtered_products(data,10))
    print(marks_calcucations([50,60,70,90,80]))