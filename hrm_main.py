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
        ano=False):
    hrm_object = hrm_class.HrmData(filename);
    print(hrm_object.average_hr);

if __name__ == '__main__':
    main('test_data/test_data2.csv')
