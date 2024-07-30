import csv
import tkinter
import os
from datetime import datetime

INPUT_FILE = "test_case1.csv"

def getTime_0800(my_date):
    return my_date.replace(hour=8, minute=0, second=0, microsecond=0)

def getTime_1200(my_date):
    return my_date.replace(hour=12, minute=0, second=0, microsecond=0)

def getTime_1300(my_date):
    return my_date.replace(hour=13, minute=0, second=0, microsecond=0)

def getTime_1700(my_date):
    return my_date.replace(hour=17, minute=0, second=0, microsecond=0)

def get_first_am(my_times):
    t0800 = getTime_0800(my_times[0])
    res = list()
    for my_time in my_times:
        res.append((my_time - t0800).total_seconds())

    print("LIST_AM_FIRST: " + str(res))
    idx = min(range(len(res)), key=lambda i: abs(res[i] - 11.5))

    return my_times[idx]

def get_last_am(my_times):
    t1200 = getTime_1200(my_times[0])
    res = list()
    for my_time in my_times:
        res.append((my_time - t1200).total_seconds())

    # print(res)
    neg_near_zero = res[-1]
    idx = 0
    for re in res:
        if re >= 0 and re < neg_near_zero:
            neg_near_zero = re
            idx += 1

    return my_times[idx]

def get_first_pm(my_times):
    t1300 = getTime_1300(my_times[0])
    res = list()
    for my_time in my_times:
        res.append((my_time -t1300).total_seconds())

    # print(res)
    neg_near_zero = res[0]
    idx = 0
    for re in res:
        if re < 0 and re > neg_near_zero:
            neg_near_zero = re
            idx += 1

    return my_times[idx]

def get_last_pm(my_times):
    t1700 = getTime_1700(my_times[0])
    res = list()
    for my_time in my_times:
        res.append((my_time -t1700).total_seconds())

    print(res)
    neg_near_zero = res[0]
    idx = 0
    for re in res:
        if re > neg_near_zero:
            neg_near_zero = re
            idx += 1

    return my_times[idx]

if __name__ == "__main__":

    # Check if input file exist!
    if not os.path.isfile(INPUT_FILE):
        # Read input file
        msg = "Input file " + INPUT_FILE + " doesn't exist!"
        tkinter.messagebox.showinfo(title=None, message=msg, **options)
        exit()

    # Structure { "id": "name" }
    ids = dict()
    tts = dict()

    # Read input file
    with open(INPUT_FILE, encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")

        for row in csvreader:
            # Explain row
            # row[0] = ชื่อเล่น
            # row[1] = ชื่อจริง เว้นวรรค และอักษรตัวแลกของ นามสกุล
            # row[2] = รหัสพนักงาน
            # row[3] = ฟิลป่าว
            # row[4] = เวลา
            # row[5] = วันที่
            # row[6] = สถานะ
            # row[7] = ฟิลป่าว

            # Set ID
            id = row[2]

            # Assign ids
            if id not in ids:
                ids[id] = [row[0], row[1]]

            # Create a record mapping
            if id not in tts:
                tts[id] = dict()

            # Mapping day with time
            tKey = datetime.strptime(row[5], '%d-%m-%Y').date()
            dKey = tKey.replace(year=tKey.year - 543)
            wday = dKey
            if wday not in tts[id]:
                # Convert year from BE to GE
                tts[id][dKey] = [datetime.strptime(row[4], '%H:%M')]
            else:
                tts[id][dKey] = tts[id][dKey] + [datetime.strptime(row[4], '%H:%M')]

    print("There are total " + str(len(tts.keys())) + " employees in total.")

    # then, loop through every employee
    for emp in tts.keys():

        # Assign Employee Name
        EM_NAME = ids[emp]
        print("Calculating " + EM_NAME[0])

        # Sort the working date by key
        tt = sorted(tts[emp].keys())

        correct_day = list()
        # RULE1: Discard weekend
        for a_key in tt:
            # Check is it a week day or not
            if a_key.weekday() >= 5:
                print("Weekend Found!\nAction: Skip weekend!")
            else:
                correct_day.append(a_key)

        # Rule2: Working Hours Count
        print("Total " + str(len(correct_day)) + " working day.")

        # Algorithm explain
        # The system define time block into 4 blocks
        # am_first คือ ช่างเวลาที่ใกล้8โมงเช้าที่สุด, โดยจะหาเวลาที่ใกล้8โมงที่สุด และก่อน8โมง
        # am_last คือ ช่วงเวลาหลังเที่ยงที่ใกล้เที่ยงที่สุด, แต่จะต้องก่อนบ่ายโมง
        # am_work_hr คือ จำนวนเวลาเวลาทำงานจริงๆช่วงเช้า
        # pm_first คือ ช่วงเวลาหลังเที่ยงที่เช้าที่สุด, แต่จะคำนวนเวลาหลังบ่ายโมง
        # pm_last คือ ช่วงเวลาท้ายที่สุดของวัน, โดยจะคิดคำนวนเวลาที่5โมงเท่านั้น
        # pm_work_hr คือช่วงเวลาทำงานจริงๆช่วงบ่าย

        for c_day in correct_day:
            time_in = tts[emp]

            for t in time_in[c_day]:
                print("ttt: " + str(t))

            am_first = get_first_am(time_in[c_day])
            print("AM_FIRST " + str(am_first))

            am_last = get_last_am(time_in[c_day])
            print("AM_LAST " + str(am_last))

            pm_first = get_first_pm(time_in[c_day])
            print("PM_FIST " + str(pm_first))

            pm_last = get_last_pm(time_in[c_day])
            print("PM_LAST " + str(pm_last))

        print(correct_day)
        exit()
