# Simple (2023-01-26)

- Rework gitlab-ci:
    - Use directly gitlab job context to run tests and do not reload docker images from cold storage
    - Simplify gitlab-ci integration by removing workspace (jobs from different stages reusing services) alike behavior
    - Support for custom CACERTS
    - Cache all downloaded docker images in a common registry cache
    - Only build CI images where tests are run when it's neccessary
    - Use buildkit for using both local and registry based cache
    - Support for promote and deploy at once
    - Make most jobs retryable again
- Django integration
    - Add support for bash/mysql/psql/ipython history
    - Support celery>=5
    - Modernize tox integration

# Pre 2022 changes were not tracked
