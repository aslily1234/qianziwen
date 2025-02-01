'''
deepseek-q1:
已知一个超长的成语接龙序列，如何快速找出1个子序列
    要求1、子序列需由原序列中连续的成语组成
    要求2、子序列中需包含不重复的1200个以上的汉字
    要求3、子序列长度最短

请写出对应的python程序

# 示例用法
# idioms = ["成语1", "成语2", ...]  # 假设这是输入的成语列表
# subsequence = find_shortest_subsequence(idioms)
# print(subsequence)
'''

def find_shortest_subsequence(idioms, target=2500):
    char_count = {}
    unique_chars = 0
    left = 0
    min_len = float('inf')
    result = (0, 0)
    
    for right in range(len(idioms)):
        # 处理右指针指向的成语，更新字符计数和唯一字符数
        idiom = idioms[right]
        for c in idiom:
            if char_count.get(c, 0) == 0:
                unique_chars += 1
            char_count[c] = char_count.get(c, 0) + 1
        
        # 当满足条件时，尝试收缩左指针以找到更短的子序列
        while unique_chars >= target:
            current_length = right - left + 1
            if current_length < min_len:
                min_len = current_length
                result = (left, right)
            
            # 移动左指针，并更新字符计数和唯一字符数
            left_idiom = idioms[left]
            for c in left_idiom:
                char_count[c] -= 1
                if char_count[c] == 0:
                    unique_chars -= 1
            left += 1
    
    if min_len != float('inf'):
        return idioms[result[0]:result[1]+1]
    else:
        return None

def read_file_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # 去除每行末尾的换行符
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
        return []
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return []

if __name__ == "__main__":
    for i in range(0, 100):
        #依次从成语接龙文件中读取成语接龙列表
        file_path = 'jielong_result/new_output_' + str(i) + '.txt'
        idiom_sequence = read_file_lines(file_path)

        subsequence = find_shortest_subsequence(idiom_sequence, target=1500)
        try:
            print('\n', file_path, len(subsequence))
        except:
            pass
            # print(subsequence)


