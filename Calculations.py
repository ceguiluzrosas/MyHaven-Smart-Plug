import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as pp
import locale

locale.setlocale(locale.LC_ALL, "")


def calculate_bill(total_kwh):
    '''Given KWH usage, function returns electricity bill as [$ amount, float]'''
    if total_kwh > 1000:
        # different calculation if kwh > 1,000
        fuel_cost = (0.038570 * 1000) + (0.048570 * (total_kwh - 1000))
        non_fuel_cost = (0.046990 * 1000) + (0.056990 * (total_kwh - 1000))
    else:
        fuel_cost = (0.038570 * total_kwh)
        non_fuel_cost = (0.046990 * total_kwh)
    money = fuel_cost + non_fuel_cost
    bill = locale.currency(money, grouping=True)
    return [money, bill]


def calculate_kwh_from_bill(bill):
    '''Given bill (float), function returns KWH usage'''
    if bill > 85.56:
        other = (0.038570 * 1000) + (0.046990 * 1000) - (0.048570 * 1000) - (0.056990 * 1000)
        return (bill - other) / (0.048570 + 0.056990)
    else:
        return bill / (0.038570 + 0.046990)


def convert_time(date_time):
    '''Returns a formatted datetime string for Data Frame'''
    if "." in date_time:
        idx = date_time.index(".") + 4
        final_date_time = datetime.datetime.strptime(date_time[:idx], "%Y-%m-%dT%H:%M:%S.%f")
        return str(datetime.datetime.strftime(final_date_time, "%Y-%m-%d %H:%M:%S.%f"))
    else:
        idx = 19
        final_date_time = datetime.datetime.strptime(date_time[:idx], "%Y-%m-%dT%H:%M:%S")
        return str(datetime.datetime.strftime(final_date_time, "%Y-%m-%d %H:%M:%S.000000"))


def api_time(date_time):
    '''Returns a formatted datetime string for API'''
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
    return str(datetime.datetime.strftime(date_time, "%Y-%m-%dT%H:%M:%S.")) + "000-04:00"


def create_graph(col, col2, quota, dataFrame):
    '''Optional: creates a generic time series graph'''
    title = "Time Series Graph for Smart Plug - " + col
    pp.title(title, size='x-large')
    pp.xlabel("DateTime", size='x-large')
    if col == 'Current Bill':
        pp.ylabel("Bill Amount ($)", size='x-large')
    else:
        pp.ylabel("KWH Amount", size='x-large')
    dataFrame[col].plot(figsize=(20, 10), subplots=False, marker="o", markersize=3, color='blue', alpha=0.5)
    dataFrame[col2].plot(figsize=(20, 10), subplots=False, marker="o", markersize=3, color='purple', alpha=0.5)
    # add horizontal lines to show thresholds
    pp.axhline(y=quota, color='red', linestyle='-', label="Threshold")
    pp.axhline(y=quota * 0.75, color='orange', linestyle='-', label="Close to Threshold")
    pp.axhline(y=quota * 0.5, color='yellow', linestyle='-', label="Half of Threshold")
    pp.axhline(y=quota * 0.25, color='green', linestyle='-', label="Half of Threshold")
    pp.grid(True)
    pp.tight_layout()
    pp.legend()
    path = "Graphs/" + col + ".png"
    pp.savefig(path, orientation='landscape')
    pp.close()


def clean_day_data(data):
    ''':returns a dict with cleaned data for current date time'''
    clean_data = {"Queried Time": convert_time(data['devices'][0]["lastDataReceivedDate"])}
    for i in data['devices'][0]['parameters']:
        # it is possible that items are out of order
        if i['name'] == "energy":
            clean_data["energy"] = i["value"]
        elif i['name'] == "outletStatus":
            clean_data["outletStatus"] = i["value"]
        elif i['name'] == "power":
            clean_data["power"] = i["value"]
        elif i['name'] == "rssi":
            clean_data["rssi"] = i["value"]
    return clean_data


def clean_month_data(data, monthly_quota, monthly_quota_kwh):
    '''Returns a length 2 list with avg power and clean data (dict)'''
    clean_data = {"Time Stamp": [], "Energy": [], "Current KWH Total": [],
                  "Current Bill": [], "Current Quota Bill Difference": [],
                  "Current Quota KWH Difference": []}
    power_sum = 0.0
    power_counts = 0
    current_kwh_total = 0
    for i in data['readings']:
        par = i['params']
        for d in par:
            if d['name'] == 'power' and d['value'] > 0:
                power_sum += eval(d['value'])
                power_counts += 1
            if d['name'] == 'energy':
                clean_data["Time Stamp"].append(convert_time(i['timeStamp']))
                val = eval(d['value']) / 1000.0
                current_kwh_total += val
                clean_data["Energy"].append(val)
                clean_data["Current KWH Total"].append(current_kwh_total)
                [money, _ ] = calculate_bill(current_kwh_total)
                clean_data["Current Bill"].append(money)
                clean_data["Current Quota Bill Difference"].append(monthly_quota - money)
                clean_data["Current Quota KWH Difference"].append(monthly_quota_kwh - current_kwh_total)
    return [power_sum / power_counts, clean_data]

