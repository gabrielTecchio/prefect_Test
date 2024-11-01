from prefect import flow

# Source for the code to deploy (here, a GitHub repo)
SOURCE_REPO="https://github.com/gabrielTecchio/prefect_Test.git"

if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint="main.py:myFlow", # Specific flow to run
    ).deploy(
        name="my-deployment",
        work_pool_name="my-work-pool", # Work pool target
        interval=90  # Interval in seconds (1800 seconds = 30 minutes)
    )
