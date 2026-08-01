# Installation guide

## Local Python

Use Python 3.12+, copy `.env.example` to `.env`, install `requirements.txt`, then run `pytest -q`, `flake8 app tests main.py`, and `python main.py`.

## Docker Compose

Run `docker compose up --build`. The API persists data in the `student-data` volume. Stop with `docker compose down`; add `-v` only when intentionally deleting data.

## Kubernetes

Install an ingress controller and metrics-server first. Create the Secret using your secret manager, update the image and host, then run `kubectl apply -k kubernetes`. Inspect `kubectl -n student-api get all,hpa,ingress` and validate with `kubectl rollout status`.

## AWS

Copy `terraform.tfvars.example`, provide an AMI and a narrowly scoped administrator CIDR, then run `terraform init`, `plan`, and `apply`. Update the Ansible inventory with the output IP and run `ansible-playbook`.

## GitHub Actions

Configure Docker Hub and cluster credentials as encrypted repository/environment secrets. Protect the production environment with required reviewers for a safer promotion gate.
