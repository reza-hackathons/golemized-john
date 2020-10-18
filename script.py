import asyncio

import yapapi
from yapapi.log import enable_default_logger, log_summary, log_event_repr  # noqa
from yapapi.runner import Engine, Task, vm
from yapapi.runner.ctx import WorkContext
from datetime import timedelta

async def main(subnet_tag = "testnet", nodes = 4):
    package = await vm.repo(
        image_hash="cfbf0729861e7a9245467e9e7cff285386fd041669beb89ea7889a5b",
        min_mem_gib=2,
        min_storage_gib=0.75,
    )

    async def worker(ctx: WorkContext, tasks):
        async for task in tasks:
            node = str(task.data['node'])
            nodes = str(task.data['nodes'])
            ctx.log(f"inside node '{node}' of '{nodes}'")
            johhny = (f"john --rules --node={node}/{nodes} --wordlist=/usr/share/john/password.lst /golem/hash-bundles/passwd.txt >> /golem/output/log.txt 2>&1;"
                      f"john --show /golem/hash-bundles/passwd.txt >> /golem/output/cracked.txt")
            ctx.run("/bin/bash",
                    "-c",
                    johhny)
            ctx.log(task.data)
            node = task.data['node']
            output_file = f"out/cracked_by_node_{node}.txt"
            ctx.download_file("/golem/output/cracked.txt", output_file)
            yield ctx.commit()
            accepted = False
            f =  open(output_file, "r")
            result = f.read()
            f.close()
            if result.find("0 password hashes") > -1:
                ctx.log(f"node '{node}' failed to crack the passwd.")
            else:
               ctx.log(f"node '{node}' succeeded in cracking the passwd.")            
            task.accept_task(result = output_file)

        # ctx.log("yay, cracked some passwd file.")

    # the nodes we would like to crack out the passwd file for us
    nodes = [Task(data={'node': n + 1, 'nodes': nodes}) for n in range(nodes)]
    init_overhead: timedelta = timedelta(minutes = 3)
    # By passing `event_emitter=log_summary()` we enable summary logging.
    # See the documentation of the `yapapi.log` module on how to set
    # the level of detail and format of the logged information.
    async with Engine(
        package = package,
        max_workers = 10,
        budget = 100.0,
        timeout = init_overhead + timedelta(minutes = 20),
        subnet_tag = subnet_tag,
        event_emitter = log_summary(log_event_repr),
    ) as engine:
        async for task in engine.map(worker, nodes):
            print(f"[task done: {task}, result: {task.output}")

enable_default_logger()
loop = asyncio.get_event_loop()    
task = loop.create_task(main(subnet_tag = "devnet-alpha.2", nodes = 4))
try:
    asyncio.get_event_loop().run_until_complete(task)

except (Exception, KeyboardInterrupt) as e:
    print(e)
    task.cancel()
    asyncio.get_event_loop().run_until_complete(task)
