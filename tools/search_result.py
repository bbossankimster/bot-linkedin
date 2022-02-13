import json
import time
import datetime

TIMEFORMAT = "%d/%m/%Y, %H:%M:%S"

def read_json(file):
    data_dict = {}
    with open(file, "r") as f:
        data_dict = json.load(f)
    return data_dict


def write_json(file, result_dict):
    with open(file, "w") as f:
        f.writelines(json.dumps(result_dict, indent=1))



def prepare_dict(jobs_data_list, category="python"):
    filename = "search_results_{}.json".format(category)
    search_results = read_json(filename)
    search_id_last = int(search_results["last_id"])
    results = search_results["results"]
    #search_results = {}
    #results = {}
    #search_id_last = 10000
    search_id = search_id_last + 1
    print("search_id_last", search_id_last)
    print("search_id new", search_id)
    results[search_id] = {
        "jobs_data_list": jobs_data_list,
        "search_time": datetime.datetime.today().strftime(TIMEFORMAT)
        }
    search_results["results"] = results
    search_results["last_id"] = search_id
    print(search_results)
    write_json(filename, search_results)


def get_new_jobs(time_delta_minutes=15, category="python"):
    filename = "search_results_{}.json".format(category)
    search_results = read_json(filename)
    search_id_last = int(search_results["last_id"])
    results = search_results["results"]
    all_urls = set()
    for result_id in sorted([*results]):
        jobs_data_list = results[result_id]["jobs_data_list"]
        for job in jobs_data_list:
            all_urls.add(job["job_link"])
        search_time_txt = results[result_id]["search_time"]
        search_time = datetime.datetime.strptime(search_time_txt, TIMEFORMAT)
        # time_last = datetime.timedelta(search_time)
        time_now = datetime.datetime.now()
        delta = time_now - search_time
        if delta.seconds/60 <= time_delta_minutes:
            print("id/time_delta",print(result_id), ":", delta.seconds/60, search_time_txt)
    print(all_urls)

