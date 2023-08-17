# qianziwen

用成语组成千字文、生成超长成语接龙的程序。

制作超长成语接龙和成语千字文主要目的是方便小朋友们学习汉字及成语，过滤了包含低频字的成语。可以在scc_chengyu_jielong.py 中 调整阈值min_word_freq，生成更长的成语接龙。

## Project Structure

```
qianziwen
├── data                        ####成语相关数据，来源于https://github.com/pwxcoo/chinese-xinhua
│  ├── ci.csv
│  ├── ci.json
│  ├── idiom.json
│  ├── word.json
│  └── xiehouyu.json
├── find_jielong_qianziwen.py   ####从超长成语接龙列表中筛选重复字数最少的成语千字文的模块
├── font
│  └── msyhbd.ttf
├── jielong_result              ####超长成语接龙结果示例
│  ├── jielong_7850.docx
│  ├── jielong_7854.docx
│  ├── jielong_7856.docx
│  └── jielong_7866.docx
├── output_docx.py              ####将成语接龙列表写入word文档，并进行拼音标注的模块
├── qianziwen.py                ####寻找250个成语，1000个不同的字 组成的千字文 的模块
├── result                      ####由250个成语，1000个不同的字 组成的千字文 结果样例
│  ├── qianziwen1.docx
│  ├── qianziwen2.docx
│  └── qianziwen3.docx
├── scc_chengyu_jielong.py      ####基于tarjan算法寻找强连通分量，再对强连通分量进行深度遍历寻找超长成语接龙的模块
└── word_dict.xlsx
```

## Database Introduction

### 成语 (idiom.json)

```json
[
    {
        "derivation": "语出《法华经·法师功德品》下至阿鼻地狱。”",
        "example": "但也有少数意志薄弱的……逐步上当，终至堕入～。★《上饶集中营·炼狱杂记》",
        "explanation": "阿鼻梵语的译音，意译为无间”，即痛苦无有间断之意。常用来比喻黑暗的社会和严酷的牢狱。又比喻无法摆脱的极其痛苦的境地。",
        "pinyin": "ā bí dì yù",
        "word": "阿鼻地狱",
        "abbreviation": "abdy"
    },
    ...
]
```

### 词语 (ci.json)

```json
[
    { 
        "ci": "宸纶", 
        "explanation": "1.帝王的诏书﹑制令。" 
    },
    ...
]
```

### 汉字 (word.json)

```json
[
    {
        "word": "嗄",
        "oldword": "嗄",
        "strokes": "13",
        "pinyin": "á",
        "radicals": "口",
        "explanation": "嗄〈叹〉\n\n 同啊”。表示省悟或惊奇\n\n 嗄!难道这里是没有地方官的么?--宋·佚名《新编五代史平话》\n\n 嗄á叹词。在句首，〈表〉疑问或反问～，这是什么？～，你想干什么？\"嗄\"另见shà㈠。\n\n 嗄shà\n\n ⒈声音嘶哑～声。\n\n 嗄a 1.助词。表示强调﹑肯定或辩解。 2.助词。方言。表示疑问或反诘。\n\n 嗄xià 1.见\"嗄饭\"。 2.见\"嗄程\"。",
        "more": "嗄 ga、a 部首 口 部首笔画 03 总笔画 13  嗄2\nshà\n〈形〉\n(1)\n声音嘶哑的 [hoarse]\n终日嚎而嗌不嗄。--《老子》\n(2)\n又如嗄哑,嗄嘶(嗓音嘶哑)\n嗄\nshà\n〈叹〉\n(1)\n什么 [what]--表示否定\n我要丢个干干净,看你嗄法把我治。--清·蒲松龄《聊斋俚曲集》\n(2)\n旧时仆役对主人、下级对上级的应诺声 [yes]\n带进来”。两边军士应一声嗄”,即将牛皋推至面前。--《说岳全传》\n另见á\n嗄1\ná\n〈叹〉\n同啊”(á)。表示省悟或惊奇 [ah]\n嗄!难道这里是没有地方官的么?--宋·佚名《新编五代史平话》\n另见shà\n嗄1\nshà　ㄕㄚ╝\n嗓音嘶哑。\n郑码janr，u55c4，gbke0c4\n笔画数13，部首口，笔顺编号2511325111354\n嗄2\ná　ㄚˊ\n同啊2”。\n郑码janr，u55c4，gbke0c4\n笔画数13，部首口，笔顺编号2511325111354"
    },
    ... 
]
```

### 歇后语 (xiehouyu.json)

```json
[
    {
        "riddle": "飞机上聊天",
        "answer": "高谈阔论"
    },
    ...
]
```


## Copyright

本仓库的所有的成语相关数据参考 https://github.com/pwxcoo/chinese-xinhua 。超长成语接龙是方便给小朋友记忆成语用的。

**本仓库无任何商业目的！如果有侵权行为将及时删除！**
