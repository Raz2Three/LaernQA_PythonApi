FROM python
WORKDIR /tests_projects/
COPY requirements.txt .
RUN pip install -r reqirements.txt
ENV ENV=dev
CMD python -m pytest -s --alluredir=test_results/ /test_project/tests/