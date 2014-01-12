#!/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Jarge'
import ConfigParser
import random
import json


class CountRandomPlayTime:
    def __init__(self):
        self.config_parser = ConfigParser.ConfigParser()
        self.config_parser.read('params.ini')
        self.plan_user = self.config_parser.get('plan', 'plan_user')
        self.plan_imp = self.config_parser.get('plan', 'plan_imp')
        self.hour_rate = self.config_parser.get('hours_accounting', '24_hours_accounting')
        self.mc_id = self.config_parser.get('mc_info', 'mc_id')
        self.hour_plus_rate = []
        self.already_generated_min = set()
        self.hit_hours = []

        # 根据计划曝光量和计划用户数算出来曝光比
        self.imp_rate = float(self.plan_user) / float("{0:.2f}".format(float(self.plan_imp)))
        self.hours_accounting = []
        self.hit_mins = []
        self.gen_json = {}

    def __get_accounting(self):
        hours_count = self.config_parser.get('hours_accounting', '24_hours_count')
        hours_array = hours_count.split(',')
        day_sum_count = 0

        # calculate total count of all day.
        for each_hour_count in hours_array:
            day_sum_count += int(str(each_hour_count).rstrip())

        for index in range(0, len(hours_array)):
            each_hour_count = hours_array[index]
            # 计算占比，保留4位小数
            each_hour_accounting = float(each_hour_count) / day_sum_count
            self.hours_accounting.append("{0:.4f}".format(each_hour_accounting * self.imp_rate))

    # 计算平均随机比
    def __prepare_hour_plus_rate(self):
        current_sum = float(0)
        for index in range(0, len(self.hours_accounting)):
            current_sum += float(self.hours_accounting[index])
            temp_kv = [current_sum, index]
            self.hour_plus_rate.append(temp_kv)

    def dump_accounting(self):
        #dump hour_plus
        # for each_hour_plus in self.hour_plus_rate:
        #     print "%s,%s" % (each_hour_plus[0], each_hour_plus[1])

        # dump hit_hours
        # print("#" * 50)
        # self.hit_hours.sort()
        # for index in range(0, 24):
        #     print ("%s : %s" % (index, self.hit_hours.count(index)))

        print("#" * 50)
        print self.hit_mins
        self.__verify()

    # 生成随机比
    def generate_play_time(self):
        self.__get_accounting()
        self.__prepare_hour_plus_rate()
        for index in range(0, 1000):
            cur_ran = random.random() * self.imp_rate
            # self.hit_hours.append(self.__get_hour_by_random(cur_ran))
            generated = self.__generate_min(cur_ran)
            while generated in self.already_generated_min:
                generated = self.__generate_min(cur_ran)

            print "%d : %s" %(index, generated)
            self.already_generated_min.add(generated)
            self.hit_mins.append(generated)

        self.dump_accounting()
        self.write_out()

    #生成随机小时
    def __get_hour_by_random(self, cur_ran):
        hit_hour = 23
        for each_hour in self.hour_plus_rate:
            if float(cur_ran) <= each_hour[0]:
                hit_hour = each_hour[1]
                break
        return hit_hour

    def __generate_min(self, cur_ran):
        just_generated = self.__get_hour_by_random(cur_ran) * 60 + random.randint(0, 59)
        return just_generated

        #计算分钟按小时分布曲线

    def __verify(self):
        self.hit_mins.sort()
        sum_map = {}
        for each_min in self.hit_mins:
            hit_hour = each_min / 60
            if sum_map.has_key(hit_hour):
                sum_map[hit_hour] += 1
            else:
                sum_map[hit_hour] = 1
        print sum_map

    # 输出到文件
    def write_out(self):
        tmp_list = []
        for each_min in self.hit_mins:
            tmp_list.append({"time": each_min, "url": "http: //mc.funshion.com/?mcid=234"})
        self.gen_json["pvsch"] = tmp_list
        out = open("out_put", 'w')
        out.write(json.dumps(self.gen_json, indent=4, sort_keys=True))


class PlayTime:
    def __init__(self, play_time, url):
        self.play_time = play_time
        self.url = url

    def __str__(self):
        return "{\"time\":%d,\"url\":\"%s\"}" % (self.play_time, self.url)
        # return "{\"time\":" + str(self.play_time) + ",\"url\":\"" + str(self.url)+"\"}"


# class PlayTimeEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o,PlayTime):
#             return
#         return json.JSONEncoder.default(self, o)


if __name__ == "__main__":
    random_play = CountRandomPlayTime()
    random_play.generate_play_time()

