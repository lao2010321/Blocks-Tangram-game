level = {
    1:{"50": 4,"50x100": 3,"100x50": 1,"size":{"width":3,"high":7}},
    2:{"50": 3,"50x100": 3,"100x50": 3,"size":{"width":5,"high":3}},
    3:{"50": 6,"100x50": 5,"50x100": 4,"size":{"width":5,"high":5}},
    3:{"50":10,"100x50": 7,"50x100": 6,"size":{"width":6,"high":6}},
}

def load(a):
    ans = {}
    ans["50"] = level[a]["50"]
    ans["50x100"] = level[a]["50x100"]
    ans["100x50"] = level[a]["100x50"]
    ans["size"] = level[a]["size"]
    a = []
    for i in range(ans[a]["size"]["width"]):
        a.append(0)
    b = []
    for i in range(ans[a]["size"]["high"]):
        b.append(a)
        
    ans["map"] = b
    return ans