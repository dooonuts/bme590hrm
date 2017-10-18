import hrm_class

def main(filename,
        user_specified_time1=0,
        user_specified_time2=30,
        brady_threshold=50,
        tachy_threshold=100,
        brady_time=5,
        tachy_time=5,
        inst=False,
        avg=False,
        ano=False,
        units=1):
    hrm_object = hrm_class.HrmData(filename);
    print(hrm_object.anomaly_hr)
    print(hrm_object.brady_times)

if __name__ == '__main__':
    # main('test_data/test_data2.csv')
    main('full_test.csv',units=1000)
