import Updates_and_Messages as um
import API_Calls as api_call
import Calculations as cal
import DataFrame as df
import datetime
import locale
import json

locale.setlocale(locale.LC_ALL, "")

def main():
    # Get Dates to Call API
    today = datetime.datetime.now()
    month_before = today + datetime.timedelta(days=-30)

    # Set some quota/threshold - $ and KWH
    # Note: quota/money is float and bill is $ amount (str)
    monthly_quota = 2.0
    monthly_quota_bill = locale.currency(monthly_quota, grouping=True)
    monthly_quota_kwh = cal.calculate_kwh_from_bill(monthly_quota)

    day_quota = monthly_quota/30
    day_quota_bill = locale.currency(day_quota, grouping=True)
    # day_quota_kwh = cal.calculate_kwh_from_bill(day_quota) not needed at the time

    api = api_call.API()
    logged_in = api.login()
    print ("Logged into API")

    if logged_in[0]:

        # Successful Login
        print(logged_in[1])

        # Collect Data to Populate Data Frame
        collecting_data = api.get_data(cal.api_time(str(month_before)), cal.api_time(str(today)))
        print ("Collected Data")

        if collecting_data[0]:

            # If we're able to collect data, do the following...

            # 1. Clean Data
            [avg_power, cleaned_data] = cal.clean_month_data(collecting_data[1], monthly_quota, monthly_quota_kwh)
            avg_power = avg_power / 1000.0
            quota_hours = monthly_quota_kwh / avg_power
            cleaned_data["Remaining Hours"] = [(quota_hours - (kwh / avg_power)) for kwh in
                                               cleaned_data["Current KWH Total"]]
            print ("Cleaned Data")

            # 2. Create DataFrame with New Data
            data_frame = df.DF(cleaned_data)
            print ("Created DataFrame")

            # 3. Get Recent/Latest Update and Average Energy
            latest_data = data_frame.get_latest(1)
            current_kwh_total = float(latest_data['Current KWH Total'])
            current_day_kwh = float(latest_data['Energy'])

            print ("Got Latest Update")

            # 4. Create Graphs -- Optional
            # cal.create_graph('Current Bill', "Current Quota Bill Difference", monthly_quota, dataFrame)
            # cal.create_graph('Current KWH Total', "Current Quota KWH Difference", monthly_quota_kwh, dataFrame)

            # 5. Check if Monthly and Day Quotas are/were Met
            [current_day_money, current_day_bill] = cal.calculate_bill(current_day_kwh)
            day_update = um.create_update(latest_data, day_quota, day_quota_bill,
                                                current_day_money, current_day_bill, 'daily')
            day_message = um.generate_message(str(today), current_day_money, current_day_bill,
                                                day_quota, "daily")

            [current_month_money, current_month_bill] = cal.calculate_bill(current_kwh_total)
            month_update = um.create_update(latest_data, monthly_quota, monthly_quota_bill,
                                                  current_month_money, current_day_bill, 'monthly')
            month_message = um.generate_message(str(today), current_month_money, current_month_bill,
                                                monthly_quota, "monthly")
            print ("Checked Quotas")


            print (data_frame.to_string())

            output = {"All Good": True,
                      "Status_Report_Month": {
                          "Month_Update": month_update,
                          "Month_Message": month_message
                        },
                      "Status_Report_Day": {
                          "Day_Update": day_update,
                          "Day_Message": day_message
                        }
                      }
            print ("Output Created")
            print (output["Status_Report_Month"])
            print (output["Status_Report_Day"])
            return json.dumps(output)

        else:

            # Unable to Request Data
            output = {"All Good": False}
            return json.dumps(output)

    else:

        # Unsuccessful Login
        return logged_in[1]


if __name__ == "__main__":

    # Run main function above
    main()
