#!/bin/bash
# source ../.venv/bin/activate
cd /askskan/askskan
export PYTHONPATH=`pwd`
python3 jobs/askskan_qa_job.py "$@"
