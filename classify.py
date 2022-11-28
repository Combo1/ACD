import concurrent.futures
import time
import defs
import pandas as pd

if __name__ == "__main__":
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        data = pd.read_csv('test.txt', sep="                               ", names=["Krankheit"],
                           skip_blank_lines=True, engine = "python")
        data = data.values.tolist()
        data_flattened = [element for sublist in data for element in sublist]
        secs = range(0, len(data_flattened), 100)
        results = executor.map(defs.fourth_match, secs)

        for result in results:
            df = pd.DataFrame(result, columns=['Data', 'ICD-10', 'Confidence Score'])
            compression_opts = dict(method='zip', archive_name='out')
            with open('fourth_iteration.csv.csv', 'a') as f:
                df.to_csv(f, header=False, compression=compression_opts, sep="|", index=False, line_terminator='\n')

    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s)')
    # We can divide the runtime by the number of available cores on our CPU!
    # We need for 40 entries ~120 seconds! -> 3 seconds per entry