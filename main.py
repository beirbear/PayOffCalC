import csv
import tkinter
import os
from datetime import datetime

INPUT_FILE = "test_case1.csv"
WORKING_SECONDS = 28800

def getTime_0800(my_date):
    return my_date.replace(hour=8, minute=0, second=0, microsecond=0)

def getTime_1200(my_date):
    return my_date.replace(hour=12, minute=0, second=0, microsecond=0)

def getTime_1300(my_date):
    return my_date.replace(hour=13, minute=0, second=0, microsecond=0)

def getTime_1700(my_date):
    return my_date.replace(hour=17, minute=0, second=0, microsecond=0)

def myRound(x, base=5):
    return base * round(x/base)

def get_first_am(my_times):
    t0800 = getTime_0800(my_times[0])
    res = list()
    for my_time in my_times:
        res.append((my_time - t0800).total_seconds())

    # print("LIST_AM_FIRST: " + str(res))
    idx = min(range(len(res)), key = lambda i: abs(res[i]-0))

    if res[idx] > 0 and idx - 1 >= 0:
        return my_times[idx - 1]

    return my_times[idx]

def get_last_am(my_times, prior=0):
    t1200 = getTime_1200(my_times[0])
    res = list()
    for my_time in my_times:
        res.append((t1200 - my_time).total_seconds())

    # print("LIST_AM_LAST: " + str(res))
    idx = min(range(len(res)), key = lambda i: abs(res[i]-0))

    return my_times[idx-prior]

def get_first_pm(my_times):
    t1300 = getTime_1300(my_times[0])
    res = list()
    for my_time in my_times:
        res.append((my_time -t1300).total_seconds())

    # print("LIST_PM_FIRST: " + str(res))
    idx = min(range(len(res)), key = lambda i: abs(res[i]-0))

    return my_times[idx]

def get_last_pm(my_times):
    t1700 = getTime_1700(my_times[0])
    res = list()
    for my_time in my_times:
        res.append((my_time -t1700).total_seconds())

    # print("LIST_PM_LAST: " + str(res))
    idx = min(range(len(res)), key = lambda i: abs(res[i]-0))

    return my_times[idx]

if __name__ == "__main__":

    # Check if input file exist!
    if not os.path.isfile(INPUT_FILE):
        # Read input file
        msg = "Input file " + INPUT_FILE + " doesn't exist!"
        print(msg)
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

            # for t in time_in[c_day]:
            #     print("ttt: " + str(t))

            tic = sorted(time_in[c_day])

            am_first = get_first_am(tic)
            # print("AM_FIRST " + str(am_first))

            am_last = get_last_am(tic)
            # print("AM_LAST " + str(am_last))

            pm_first = get_first_pm(tic)
            # print("PM_FIST " + str(pm_first))

            pm_last = get_last_pm(tic)
            # print("PM_LAST " + str(pm_last))

            # Calculate working hour
            am_start = None
            am_stop = None
            pm_start = None
            pm_stop = None

            T0800 = getTime_0800(tic[0])
            if am_first <= T0800:
                am_start = T0800
            else:
                am_start = am_first

            T1200 = getTime_1200(tic[0])
            T1300 = getTime_1300(tic[0])
            if am_last >= T1200 and am_last < T1300:
                am_stop = T1200
            else:
                am_stop = am_last

            if pm_first <= T1300:
                pm_start = T1300
            else:
                pm_start = pm_first

            T1700 = getTime_1700(tic[0])
            if pm_last > T1700:
                pm_stop = T1700
            else:
                pm_stop = pm_last

            # Ordinary Case
            working_hour = (am_stop - am_start) + (pm_stop - pm_start)

            # Case ไม่มีต้องออก ตอกเข้ากลางวัน
            if am_first == am_last and \
                pm_first == pm_last:
                print(str(c_day) + ": No AM Clock Out and No PM Clock In")
                working_hour = (pm_stop - am_start) - (T1300 - T1200)

            # Case ออกก่อนเทียง
            # print("AM_STOP: " + str(am_stop))
            # print("AM_LAST: " + str(am_last))

            elif am_last == pm_first and \
                    pm_last > pm_first and \
                    am_last < am_first:
                print(str(c_day) + ": AM Clock Out Before 1200")
                am_stop = get_last_am(tic, prior=1)
                working_hour = (am_stop - am_start) + (pm_stop - pm_start)

            # Case ลาบ่าย
            elif pm_stop <= pm_start:
                print(str(c_day) + ": No PM Clock In and Out")
                working_hour = am_stop - am_start
                pm_start = T1200
                pm_Stop = T1200

                # print(am_stop - am_start)
                # print(working_hour.seconds/WORKING_SECONDS*350)

            # Case ลาเช้า
            elif am_first == am_last:
                print(str(c_day) + ": No AM Clock In and Out")
                working_hour = pm_stop - pm_start

            # print("\nAM_START TIME " + str(am_start))
            # print("AM_STOP TIME " + str(am_stop))
            # print("PM_START TIME " + str(pm_start))
            # print("PM_STOP TIME " + str(pm_stop))


            wage = myRound(working_hour.seconds/WORKING_SECONDS*350)
            txt_am_start = None
            txt_am_stop = None
            txt_pm_start = None
            txt_pm_stop = None

            if am_start == T0800:
                txt_am_start = "มา"
            elif am_start > T0800:
                txt_am_start = str(am_start.time())
            else:
                txt_am_start = "ลา"

            if am_stop == T1200:
                txt_am_stop = "มา"
            elif am_stop < T1200 and am_stop > T0800:
                txt_am_stop = str(am_stop.time())
            else:
                txt_am_stop = "ลา"

            if pm_start == T1300:
                txt_pm_start = "มา"
            elif pm_start > T1300:
                txt_pm_start = str(pm_start.time())
            else:
                txt_pm_start = "ลา"

            if pm_stop == T1700:
                txt_pm_stop = "มา"
            elif pm_stop < T1700 and pm_stop > T1300:
                txt_pm_stop = str(pm_stop.time())
            else:
                txt_pm_stop = "ลา"

            msg = (str(c_day) + "," + txt_am_start + "," + txt_am_stop + "," +
                   txt_pm_start + "," + txt_pm_stop + "," + str(wage))
            print(msg)

        exit()
