import os, sys, time
sys.path.append(os.path.join(os.path.dirname(__file__)))
import download_file as download

def handler(event, context):
    try:
        start_time = time.perf_counter()
        bucket = os.environ['DATA_BUCKET']
        download.run_download(event, bucket)
        end_time = time.perf_counter()
        print(f"Time elapsed is {end_time - start_time}")
    except:
        # place holder for slack error handling
        raise