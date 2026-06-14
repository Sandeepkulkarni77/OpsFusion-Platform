# OpsFusion-Platform
OpsFusion Platform is an end-to-end DevOps system that integrates CI/CD, containerization, Kubernetes orchestration, GitOps-based deployments, and observability into a unified automated workflow from development to production.

##  Architecture diagram

<img width="1056" height="705" alt="image" src="https://github.com/user-attachments/assets/da9ecfd5-790a-4339-9f4c-8fdc5be287bc" />


## Repository Structure

```text
ops-fusion-platform/
│
├── app/
│   ├── src/
│   ├── tests/
│   ├── migrations/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── Makefile
│
├── postman/
│   └── student-api.postman_collection.json
│
├── scripts/
│   ├── install_docker.sh
│   ├── install_minikube.sh
│   ├── install_kubectl.sh
│   └── setup_vagrant.sh
│
├── docker/
│   ├── docker-compose.yml
│   └── .env.example
│
├── nginx/
│   ├── nginx.conf
│   └── default.conf
│
├── vagrant/
│   ├── Vagrantfile
│   └── bootstrap.sh
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── update-image-tag.yml
│
├── kubernetes/
│   ├── api/
│   ├── database/
│   ├── vault/
│   ├── eso/
│   ├── observability/
│   └── argocd/
│
├── helm/
│   ├── api/
│   ├── postgres/
│   ├── vault/
│   ├── observability/
│   └── argocd/
│
├── docs/
│   ├── architecture.png
│   ├── kubernetes-architecture.png
│   ├── observability-architecture.png
│   └── screenshots/
│
└── README.md
