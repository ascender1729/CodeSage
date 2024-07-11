import multiprocessing
from functools import partial
from enhanced_analysis import EnhancedCodeSage

def analyze_file_wrapper(config, file_path):
    sage = EnhancedCodeSage(config)
    return file_path, sage.analyze_file(file_path)

def analyze_files_parallel(file_paths, config, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(partial(analyze_file_wrapper, config), file_paths)

    return dict(results)