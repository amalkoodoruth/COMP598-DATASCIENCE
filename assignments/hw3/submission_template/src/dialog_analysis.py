import csv
import pandas as pd
import sys
import re
import json


file = sys.argv[-1]

## check if file to be read is in csv format
if file[-4:] == ".csv":
    ds = pd.read_csv(file)

    count_twi = 0
    count_app = 0
    count_rar = 0
    count_pink = 0
    count_rdash = 0
    count_flu = 0

    twi = r"(?i)(^Twilight Sparkle$)"
    app = r"(?i)(^applejack$)"
    rar = r"(?i)(^rarity$)"
    pink = r"(?i)(^pinkie pie$)"
    rdash = r"(?i)(^rainbow dash$)"
    flu = r"(?i)(^fluttershy$)"

    for pony in ds['pony']:
        if re.match(twi, pony):
            count_twi += 1
        elif re.match(app, pony):
            count_app += 1
        elif re.match(rar, pony):
            count_rar += 1
        elif re.match(pink, pony):
            count_pink += 1
        elif re.match(rdash, pony):
            count_rdash += 1
        elif re.match(flu, pony):
            count_flu += 1

    tot = ds.count()[0]

    count_dict = {
        "twilight sparkle": count_twi,
        "applejack": count_app,
        "rarity": count_rar,
        "pinkie pie": count_pink,
        "rainbow dash": count_rdash,
        "fluttershy": count_flu
    }

    verbose_dict = {
        "twilight sparkle": round(count_twi / tot,2),
        "applejack": round(count_app / tot,2),
        "rarity": round(count_rar / tot,2),
        "pinkie pie": round(count_pink / tot,2),
        "rainbow dash": round(count_rdash / tot,2),
        "fluttershy": round(count_flu / tot,2)
    }

    out_dict = {"count": count_dict,
                "verbose": verbose_dict}

    json_out = json.dumps(out_dict,indent=4)

    ## output file name specified
    if sys.argv[1] == "-o":
        if sys.argv[2] == file:
            print("Error: Specify name of output file after '-o' ")
            sys.exit()
        else:
            out = sys.argv[2]
            with open(out, 'w') as output:
                output.write(json_out)
            sys.exit()


    ## output file name not specified. Assign default output.json
    else:
        out = "output.json"
        with open(out,'w') as output:
            output.write(json_out)
        sys.exit()


else:
    print("Error: Last positional argument should be a csv file")
