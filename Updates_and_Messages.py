import locale

locale.setlocale(locale.LC_ALL, "")

def generate_message(today, current_money, current_bill, quota, type):
    '''
    Generates a message with general facts about user's electricity usage
    with respect to quota amount
    '''
    bill = locale.currency(quota, grouping=True)
    if (quota < current_money):
        # Exceed
        exceed = locale.currency(current_money - quota, grouping=True)
        message = ("As of {}, your current bill is {}. Please note "
                   "that you have exceeded your {} quota of {} by {}.").format(today, current_bill, type, bill, exceed)
    else:
        savings = locale.currency(quota - current_money, grouping=True)
        message = ("As of {}, your current bill is {}. Please note "
                   "that you are {} below you're {} quota. Good Job!").format(today, current_bill, savings, type)
    return message


def create_update(latest_data, quota_money, quota_bill, curr_money, curr_bill, type):
    dic = {
        "Queried Time": str(latest_data.index.values[0]),
        "Current Energy": round(float(latest_data['Energy']), 5),
    }
    if type=='monthly':
        total_kwh = float(latest_data['Current KWH Total'])
        dic["Current KWH Total"] = round(total_kwh, 5)
        dic["Current Month Bill"] = curr_bill
        dic["Monthly Quota"] = quota_bill
        dic["Remaining Month Hours"] = round(float(latest_data['Remaining Hours']), 2)
        dic["Current Monthly Savings"] = locale.currency(quota_money - curr_money, grouping=True)
        dic["Current Monthly Exceed"] = locale.currency(curr_money - quota_money, grouping=True)
    else:
        dic["Current Day Bill"] = curr_bill
        dic["Day Quota"] = quota_bill
        dic["Current Day Savings"] = locale.currency(quota_money - curr_money, grouping=True)
        dic["Current Day Exceed"] = locale.currency(curr_money - quota_money, grouping=True)

    return dic
