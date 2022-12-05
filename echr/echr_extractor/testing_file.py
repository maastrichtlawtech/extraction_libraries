from echr import get_echr_extra,get_echr



if __name__ == '__main__':
    df,json = get_echr_extra(count=100,save_file='y',threads=10)
    df = get_echr(start_id=1,save_file='y')


    df,json = get_echr_extra(start_id=20,end_id=3000,save_file='n')

    df = get_echr(start_id=1000,count=2000,save_file='n')