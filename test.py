import random
import time

from tqdm import tqdm

class Task:
    def __init__(self) -> None:
        self.jobs = int(1e3)

    @property
    def job_done(self) -> bool:
        return self.jobs <= 0

    def do_job(self) -> int:
        time.sleep(1)
        job_minus = random.randint(1, 50)
        self.jobs = max(0, self.jobs - job_minus)
        return job_minus


task: Task = Task()

info = { 'efficiency': None }

with tqdm(
    total=task.jobs, desc='Doing jobs'
) as t:

    while not task.job_done:

        job_minus = task.do_job()

        info['efficiency'] = job_minus
        t.update(job_minus)
        t.set_postfix(info)