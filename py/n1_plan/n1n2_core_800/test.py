import json

with open("words2.json", "r") as f:
    s = f.read()
    s = json.loads(s)

    sorted_s = sorted(s, key=lambda x: x["index"])

    i = 0
    lesson  = 1
    res = []
    group = [sorted_s[i:i+20] for i in range(0,len(sorted_s),20) ]
    for gi in range(len(group)):
        for x in group[gi]:
            x["lesson"] = gi + 1
            res.append(x)
    print(res)
    with open("words2_lesson.json", "w") as f:
        f.write(json.dumps(res, indent=4, ensure_ascii=False))
