
#初始化，构造字频索引，成语首字索引，成语首字同音索引，成语尾字索引，成语尾字同音索引
import json 
from xpinyin import Pinyin


p = Pinyin()

file = 'data/idiom.json'
idiom_info_list = None
with open(file,'r', encoding='UTF-8') as f:
     idiom_info_list = json.load(f)

#字频索引
word_dict = {}
#成语首字索引
idiom_head_list = {}
#成语尾字索引
idiom_tail_list = {}

#成语成语首字同音索引
idiom_pinyin_head_list = {}
#成语成语尾字同音索引
idiom_pinyin_tail_list = {}


'''
{
    "derivation": "语出《法华经·法师功德品》下至阿鼻地狱。”",
    "example": "但也有少数意志薄弱的……逐步上当，终至堕入～。★《上饶集中营·炼狱杂记》",
    "explanation": "阿鼻梵语的译音，意译为无间”，即痛苦无有间断之意。常用来比喻黑暗的社会和严酷的牢狱。又比喻无法摆脱的极其痛苦的境地。",
    "pinyin": "ā bí dì yù",
    "word": "阿鼻地狱",
    "abbreviation": "abdy"
}
'''
for data in idiom_info_list:
	idiom = data['word']

	idiom_word_list = list(idiom)

	#过滤掉非四字成语
	if len(idiom_word_list) != 4:
		print(idiom)
		continue

	#过滤掉有重复字的成语
	if len(set(idiom_word_list)) != 4:
		print(idiom)
		continue

	#统计字频
	for word in idiom_word_list:
		if word in word_dict:
			word_dict[word] += 1
		else:
			word_dict[word] = 1

	#构建成语首字索引库
	first_word = idiom_word_list[0]

	if first_word in idiom_head_list:
		idiom_head_list[first_word].append(idiom)
	else:
		idiom_head_list[first_word] = [idiom]

	#构建成语尾字索引库
	last_word = idiom_word_list[-1]

	if last_word in idiom_tail_list:
		idiom_tail_list[last_word].append(idiom)
	else:
		idiom_tail_list[last_word] = [idiom]

#构造首字母同音的成语索引
for word in idiom_head_list:
	word_pinyin = p.get_pinyin(word, tone_marks='marks')

	if word_pinyin in idiom_pinyin_head_list:
		idiom_pinyin_head_list[word_pinyin] += list(idiom_head_list[word])
	else:
		idiom_pinyin_head_list[word_pinyin] = list(idiom_head_list[word])

#构造尾字母同音的成语索引
for word in idiom_tail_list:
	word_pinyin = p.get_pinyin(word, tone_marks='marks')

	if word_pinyin in idiom_pinyin_tail_list:
		idiom_pinyin_tail_list[word_pinyin] += list(idiom_tail_list[word])
	else:
		idiom_pinyin_tail_list[word_pinyin] = list(idiom_tail_list[word])

#输出统计信息
print('word_num:', len(word_dict.keys()))
print('idiom_head_num:', len(idiom_head_list.keys()))
print('idiom_tail_num:', len(idiom_tail_list.keys()))
print('idiom_pinyin_head_list_num:', len(idiom_pinyin_head_list.keys()))
print('idiom_pinyin_tail_list_num:', len(idiom_pinyin_tail_list.keys()))

#对字频库进行排序 key使用lambda匿名函数按键进行排序
sort_word_dict = sorted(word_dict.items(),key = lambda x:x[1], reverse=False)

#输出字频索引
from openpyxl import Workbook

def write_dict_to_excel(data_dict, filename):
    # 创建一个新的Excel工作簿
    workbook = Workbook()

    # 获取活动的工作表
    worksheet = workbook.active

    # 写入字典的键作为表头
    headers = list(data_dict.keys())
    worksheet.append(headers)

    # 写入字典的值
    values = list(data_dict.values())
    worksheet.append(values)

    # 保存Excel文件
    workbook.save(filename)

write_dict_to_excel(word_dict, 'word_dict.xlsx')

'''
【不重复的成语千字文】
步骤一、随机从 idiom_head_list 里面选择一个字作为成语首字，随机从相同首字成语列表中选择一个成语作为候选成语idiom
步骤二、根据字频 和 不重复规则 进行过滤
	a.验证成语的所有字都未使用过（查找flag_dict）
	b.验证成语的所有字里面没有低频字（查找字频库表，出现次数至少大于等于n）
步骤三、如果idiom满足骤二的过滤条件，则将其加入article_list，并对flag_dict进行标记
步骤四、重复步骤一、步骤二、步骤三，直到 len(article_list) >= 250
'''
def generate_thousand_idiom(idiom_head_list, word_dict, freq_num = 15, article_list_len=200, max_try_count=100):
	#生成千字文
	import random
	article_list = [] #成语千字文列表
	flag_dict = {} #用于标识字是否使用

	idiom_head_list_keys = list(idiom_head_list.keys())
	while len(article_list) < 250:
		#多次尝试，避免出现重复字
		try_count = 0
		while try_count < max_try_count:
			random_word = random.choice(idiom_head_list_keys)
			random_idiom = random.choice(idiom_head_list[random_word])

			#过滤掉低频字 和 重复字
			repeat = 0
			not_freq = 0
			for word in list(random_idiom):
				if word in flag_dict:
					repeat = 1
					break

				if word_dict[word] < freq_num:
					not_freq = 1
					break

			#满足过滤条件，则加入千字文
			if (repeat == 0) and (not_freq == 0):
				article_list.append(random_idiom)

				for word in list(random_idiom):
					flag_dict[word] = 1

				break

			try_count += 1

		#end while try_count < max_try_count

		#如果多次尝试仍旧无法新增成语，则重新开始
		if (try_count == max_try_count) :
			if len(article_list) > article_list_len:
				print('\n成语数量:', len(article_list), '\n全部成语: \n', '，'.join(article_list))

			article_list = [] #成语千字文列表
			flag_dict = {} #用于标识字是否使用


	return article_list


'''
【不重复的成语接龙】
步骤一、随机从 idiom_head_list 里面选择一个字作为成语首字，随机从相同首字成语列表中选择一个成语作为候选成语idiom
步骤二、根据字频 和 不重复规则 进行过滤
	a.验证成语的所有字都未使用过（查找flag_dict）(首字允许重复)
	b.验证成语的所有字里面没有低频字（查找字频库表，出现次数至少大于等于n）
步骤三、如果idiom满足骤二的过滤条件，则将其加入article_list，并对flag_dict进行标记
步骤四、重复步骤一、步骤二、步骤三，直到 len(article_list) >= 250

freq_num = 1 #字频表阈值
'''
def generate_idiom_jielong(idiom_head_list, word_dict, freq_num=1, article_list_len=50, max_try_count=100):
	#生成千字文
	import random
	article_list = [] #成语千字文列表
	flag_dict = {} #用于标识字是否使用

	idiom_head_list_keys = list(idiom_head_list.keys())

	first_word = random.choice(idiom_head_list_keys)
	while len(article_list) < 250:

		#多次尝试，避免出现重复字
		try_count = 0
		while try_count < max_try_count:
			#从众多首字相同的成语中随机抽取一个
			random_idiom = random.choice(idiom_head_list[first_word])

			#过滤掉低频字 和 重复字(首字除外)
			repeat = 0
			not_freq = 0
			for word in list(random_idiom):
				if (word != first_word) and (word in flag_dict):
					repeat = 1
					break

				if word_dict[word] < freq_num:
					not_freq = 1
					break

			#性命交关，#####，观山玩水，

			#满足过滤条件，则加入千字文
			if (repeat == 0) and (not_freq == 0):
				article_list.append(random_idiom)

				for word in list(random_idiom):
					flag_dict[word] = 1

				break

			try_count += 1
		#end while try_count < max_try_count

		#将末尾字作为下一个成语的开头字
		first_word = list(random_idiom)[-1]

		if (try_count == max_try_count) or (first_word not in idiom_head_list):
			if len(article_list) > article_list_len:
				print('\n接龙次数:', len(article_list), '\n全部成语: \n', '，'.join(article_list))
			break

	#end while len(article_list) < 250

	return article_list


'''
【不重复的成语接龙拼音版（第二个成语的首字与第一个成语的尾字同音即可，依次类推）】
步骤一、随机从 idiom_head_list 里面选择一个字作为成语首字，随机从相同首字成语列表中选择一个成语作为候选成语idiom
步骤二、根据字频 和 不重复规则 进行过滤
	a.验证成语的所有字都未使用过（查找flag_dict）(首字允许重复)
	b.验证成语的所有字里面没有低频字（查找字频库表，出现次数至少大于等于n）
步骤三、如果idiom满足骤二的过滤条件，则将其加入article_list，并对flag_dict进行标记
步骤四、重复步骤一、步骤二、步骤三，直到 len(article_list) >= 250

freq_num = 1 #字频表阈值
'''
def generate_idiom_pinyin_jielong(idiom_pinyin_head_list, word_dict, freq_num=1, article_list_len=50, max_try_count=100):
	#生成千字文
	import random
	article_list = [] #成语千字文列表
	flag_dict = {} #用于标识字是否使用

	idiom_head_list_keys = list(idiom_pinyin_head_list.keys())

	first_word = random.choice(idiom_head_list_keys)
	while len(article_list) < 250:

		#多次尝试，避免出现重复字
		try_count = 0
		while try_count < max_try_count:
			#从众多首字相同的成语中随机抽取一个
			random_idiom = random.choice(idiom_pinyin_head_list[first_word])

			#过滤掉低频字 和 重复字(首字除外)
			repeat = 0
			not_freq = 0
			for word in list(random_idiom):
				if (word != first_word) and (word in flag_dict):
					repeat = 1
					break

				if word_dict[word] < freq_num:
					not_freq = 1
					break

			#满足过滤条件，则加入千字文
			if (repeat == 0) and (not_freq == 0):
				article_list.append(random_idiom)

				for word in list(random_idiom):
					flag_dict[word] = 1

				break

			try_count += 1
		#end while try_count < max_try_count

		#将末尾字作为下一个成语的开头字
		first_word = list(random_idiom)[-1]
		#转换为拼音
		first_word = p.get_pinyin(first_word, tone_marks='marks')

		if (try_count == max_try_count) or (first_word not in idiom_pinyin_head_list):
			if len(article_list) > article_list_len:
				print('\n接龙次数:', len(article_list), '\n全部成语: \n', '，'.join(article_list))
			break

	#end while len(article_list) < 250

	return article_list

#成语千字文
article_list = generate_thousand_idiom(idiom_head_list, word_dict, freq_num=7, article_list_len=245, max_try_count=150)
print('\n千字文成功:', len(article_list), '\n全部成语: \n', '，'.join(article_list))

#精准接龙版本
article_list = []
while len(article_list) < 250:
	article_list = generate_idiom_jielong(idiom_head_list, word_dict, freq_num=10, article_list_len=75, max_try_count=150)
print('\n\n接龙成功! 全部成语：', '，'.join(article_list))

#同音接龙版本
article_list = []
while len(article_list) < 250:
	article_list = generate_idiom_pinyin_jielong(idiom_pinyin_head_list, word_dict, freq_num=10, article_list_len=70, max_try_count=100)
print('\n\n接龙成功! 全部成语：', '，'.join(article_list))


