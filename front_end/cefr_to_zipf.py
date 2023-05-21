def cefr_to_zipf_func(cefr):
    if cefr == "A1":
        return 7.0 #mean of range 6.0-8.0
    if cefr == "A2":
        return 6.0 #mean of 5.5-6.5
    if cefr == "B1":
        return 5.5 #mean of 5.0 and 6.0
    if cefr == "B2":
        return 5.0 #mean of 4.5 and 5.5
    if cefr == "C1":
        return 4.5 #mean of 4.0 and 5.0
    if cefr == "C2":
        return 2.0 # mean of 0 and 4
    return 0.0


#initialize in front_end trial (& maybe create __init__.py files in back + front end folders)
# cefr = "A2"
# zipf = cefr_to_zipf_func(cefr)
# print(zipf)
#from ..back_end.cefr_to_zipf import cefr_to_zipf_func