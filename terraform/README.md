# 🚀 Terraform — VPC & EKS Setup

Minimal **Terraform configuration** that provisions:
- A **VPC** with public + private subnets  
- An **EKS cluster** (v1.29) with one managed node group  
- IAM → RBAC mapping using **EKS access entries**

---

## ✅ What this creates
### Networking (VPC Module)
- Region: `us-east-1`
- CIDR: `10.0.0.0/16`
- 2 × private subnets (`10.0.1.0/24`, `10.0.2.0/24`)
- 2 × public subnets (`10.0.3.0/24`, `10.0.4.0/24`)
- Single **NAT Gateway** for private subnets

### Kubernetes (EKS Module)
- Cluster name: `myEKS-cluster`  
- Version: `1.29` (configurable)  
- Managed node group: `t3.small` spot instance  
- `enable_irsa = true` → IAM Roles for Service Accounts  
- `authentication_mode = "API_AND_CONFIG_MAP"` → allows both ConfigMap + API-based access  
- `access_entries` → maps IAM user/role (e.g. `dan_user`) to Kubernetes admin

---

## ▶️ Usage

Initialize & apply:

```bash
terraform init
terraform apply
```

Update kubeconfig:

```bash
aws eks update-kubeconfig --region us-east-1 --name myEKS-cluster
kubectl get nodes
```

---

## 🧰 Files

- **main.tf** — provider, VPC, EKS (with IRSA + access entries)  
- **variables.tf** — region, cluster_name  
- **terraform.tfvars** — values (`us-east-1`, `myEKS-cluster`)  

---

## 🧹 Clean up
```bash
terraform destroy
```
Deletes VPC, EKS cluster, and node group.  
⚠️ Reminder: **EKS + NAT Gateway incur hourly cost**.
