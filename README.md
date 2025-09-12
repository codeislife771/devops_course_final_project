# 📝 Flask Task Manager – DevOps Final Project

A simple **Task Manager application** built with **Flask**, storing tasks in **JSON**, and deployed on **Kubernetes (EKS)** with **Terraform**.  
Includes CI/CD pipelines using **GitHub Actions**.

---

## 🚀 Tech Stack
- **Flask** – REST API + HTML template (`index.html`)
- **Docker** – Containerized application
- **Terraform** – Infrastructure as Code (AWS EKS)
- **Kubernetes** – Deployment, ConfigMap, Load Balancer
- **GitHub Actions** – CI/CD (build, test, deploy)

---

## 📂 Project Structure
```
.
├── app.py                # Flask application
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image
├── tasks.json            # JSON storage
├── templates/index.html  # Frontend page
├── test_tasks.py         # Unit tests
│
├── terraform/            # Terraform configuration (EKS cluster)
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars
│
├── deploy/               # Kubernetes manifests
│   ├── flask-configmap.yaml
│   ├── flask_app_deployment.yaml
│   └── load_balancer.yaml
│
└── .github/workflows/    # CI/CD pipelines
    ├── ci-dev.yaml
    └── cd-main.yaml
```

---

## ⚡ Run Locally (Development)

```bash
# Clone repo
git clone https://github.com/codeislife771/devops_course_final_project.git
cd devops_course_final_project

# Build Docker image
docker build -t flask-task-manager .

# Run container
docker run -d -p 5000:5000 flask-task-manager

# Check health endpoint (JSON)
curl http://localhost:5000/health

# Open main application (HTML UI)
http://localhost:5000/tasks
```

---

## ☸️ Deployment on Kubernetes (EKS)

1. **Provision EKS with Terraform**:
   ```bash
   cd terraform
   terraform init
   terraform apply
   ```

2. **Deploy Flask app**:
   ```bash
   kubectl apply -f deploy/flask-configmap.yaml
   kubectl apply -f deploy/flask_app_deployment.yaml
   kubectl apply -f deploy/load_balancer.yaml
   ```

3. **Access via Load Balancer**:  
   Once deployed, get the LB URL:
   ```bash
   kubectl get svc flask-service
   ```

---

## 🔄 CI/CD Pipelines
- **ci-dev.yaml** – runs on feature/dev branches (build + test)  
- **cd-main.yaml** – runs on `main`, builds + pushes Docker image, deploys to EKS  

---

## 📌 API Endpoints
- `GET /api/tasks` → Get all tasks  
- `POST /tasks` → Create a task  
- `GET /tasks/<uuid>` → Get a single task  
- `PUT /tasks/<uuid>` → Update a task  
- `DELETE /tasks/<uuid>` → Delete a task  
- `GET /health` → Health check  

---

## 🧪 Example Usage

```bash
# Create a new task
curl -X POST http://localhost:5000/tasks   -H "Content-Type: application/json"   -d '{"name": "Learn DevOps", "author": "Student"}'

# Get all tasks
curl http://localhost:5000/api/tasks
```

---

## 🔑 Required GitHub Secrets & Variables

To run the CI/CD pipelines successfully, the following must be configured in **GitHub Repository Settings**:

### Secrets
- `AWS_ACCESS_KEY_ID` – AWS access key for Terraform & EKS
- `AWS_SECRET_ACCESS_KEY` – AWS secret key for Terraform & EKS
- `DOCKER_ACCESS_TOKEN` – Access token for DockerHub
- `DOCKER_LOGIN_RUN` – DockerHub username or login credential

### Variables
- `AWS_REGION` – AWS region (e.g., `us-east-1`)
- `EKS_CLUSTER_NAME` – Name of the target EKS cluster

---

## 🔒 Branch Protection Rules
The repository uses the following rules on the **main** branch:
- No direct pushes (require Pull Request)
- Restrict deletions
- Block force pushes

---

## 👨‍💻 Author
Project by Chen George(*codeislife771*) as part of **DevOps Final Project**.
