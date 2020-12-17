import time
import multiprocessing as mp
import signal
from multiprocessing import freeze_support


class CpuTest:

    __wrong_flag = 0

    def test_func(self, s_m):
        # 测试函数,计算斐波那契数列
        if s_m == 's':
            num = 2000000
        else:
            num = 250000
        n1, n2 = 0, 1
        count = 0
        while count < num:
            n3 = n1 + n2
            n1 = n2
            n2 = n3
            count += 1
        return 1

    def multi_task(self):
        # 多核测试，计算1024个250000位的斐波那契数列，统计总耗时
        test_num = 1024  # 多核测试计算数量

        print("多核测试\n计算斐波那契数列中。。。(Ctrl+C退出)")
        num_cores = int(mp.cpu_count())  # cpu核心数
        print("本地计算机有: " + str(num_cores) + " 核心")

        pool = mp.Pool(num_cores, self.del_worker)  # 创建进程池
        result = []
        time0 = time.time()
        for i in range(num_cores):
            result.append(pool.apply_async(self.test_func, args=('m')))

        # 每次向进程池中只添加最多cpu核心数个进程，保证cpu一直满负荷运行，直到1024个斐波那契数列计算完成
        try:
            last_c = 0  # 上一次计算完成数
            while True:
                cur_c = 0  # 当前计算完成数
                for res in result:
                    if res.ready():
                        cur_c += 1
                # print('c: ', cur_c, 'last_c: ', last_c)
                diff_c = cur_c - last_c  # 两次计算完成数之差，因为第一步只向进程池添加了cpu核心数个进程，所以此处diif_c一定小于等于cpu核心数
                last_c = cur_c
                if diff_c < (test_num - len(result)):  # 如果diff_c小于现在进程池里的进程数与目标数只差，则添加diff_c个进程
                    add_n = diff_c
                else:  # 否则只添加现在进程池里的进程数与目标数只差这么多个，让计算总数达到目标即可
                    add_n = test_num - len(result)
                for i in range(add_n):
                    # print(add_n, len(result))
                    result.append(pool.apply_async(self.test_func, args=('m')))

                if cur_c == test_num:
                    print(" \nPython CPU多核测试完成耗时: %.3fs" % (time.time() - time0))
                    break

        except KeyboardInterrupt:
            print(" \n主动停止")
            pool.terminate()
            pool.join()
            self.__wrong_flag = 1
            time.sleep(2)

        except Exception as e:
            print(" \n程序错误\n", e)
            self.__wrong_flag = 1
            time.sleep(10)

        pool.close()
        pool.join()

    def del_worker(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def run(self):
        freeze_support()

        flag = ''
        try:
            print(" ")
            flag = input("选择单核/多核测试(请输入s/m): ")
            print(" ")
        except KeyboardInterrupt:
            print(" \n主动退出")
            time.sleep(2)
        except Exception as e:
            print(" \n程序错误\n", e)
            time.sleep(10)

        try:
            if flag != 's' and flag != 'm':
                self.__wrong_flag = 1
                print("输入错误！")
                time.sleep(10)
            elif flag == 's':  # 执行单核测试
                print("单核测试\n计算斐波那契数列中。。。(Ctrl+C退出)")
                time0 = time.time()
                self.test_func('s')
                print(" \nPython CPU单核测试完成耗时: %.3fs" % (time.time() - time0))
            else:  # 执行多核测试
                self.multi_task()
            if not self.__wrong_flag:
                print("参考对比：\n"
                      "    i7 2600：单核40.053s/多核203.400s\n"
                      "    i7 8750H：单核28.693s/多核121.719s\n"
                      "    3400G：单核30.457s/多核162.702s\n"
                      "    3700X：单核28.839s/多核s\n"
                      "    3950X：单核28.065s/多核35.833s\n"
                      "    3990X：单核42.362s/多核14.856s\n"
                      "    树莓派4b：单核267.841s/多核1015.216s")
                time.sleep(60)
        except KeyboardInterrupt:
            print(" \n主动退出")
            time.sleep(2)
        except Exception as e:
            print(" \n程序错误\n", e)
            time.sleep(10)


if __name__ == '__main__':
    test = CpuTest()
    test.run()
