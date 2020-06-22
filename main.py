from sequential_read import main as seq_main
from threading_read import main as thread_main
from asyncio_read import main as async_main
from multiprocessing_read import main as mproc_main


# This script simply runs all previous ones and gets some results in terms of performance
if __name__ == "__main__":
    seq_dur = mt_dur =  async_dur = mproc_dur = 0
    print(f"Processing files with different approaches: sequential, multi-threaded, asyncio, multi-processing")
    print(f'Starting sequential read...')
    print(f'*' * 50)
    seq_dur = seq_main()
    print(f'Sequential read done')
    print(f'*' * 50)
    print(f'Starting multi thread read...')
    print(f'*' * 50)
    mt_dur = thread_main()
    print(f'Multi thread read done')
    print(f'*' * 50)
    print(f'Starting asyncio read...')
    print(f'*' * 50)
    async_dur = async_main()
    print(f'Async read done')
    print(f'*' * 50)
    print(f'Starting multi processing read...')
    print(f'*' * 50)
    mproc_dur = mproc_main()
    print(f'Multi processing read done')
    print(f'*' * 50)
    print(f'''Final results
        Sequential read: {seq_dur}
        Multi threaded read: {mt_dur}
        Async read: {async_dur}
        Multi process read: {mproc_dur}
    ''')