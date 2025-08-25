# Terraform Exercise — VPC & EKS Setup (main.tf only)

A minimal Terraform configuration that provisions a **VPC** and an **Amazon EKS cluster** using public modules.  
This exercise focuses on declaring providers, consuming modules, and passing inputs.

---

## ✅ What this creates

### Networking (VPC Module)
- **AWS region:** `us-east-1`  
- **VPC CIDR:** `10.0.0.0/16`  
- **Availability Zones:** `us-east-1a`, `us-east-1b`  
- **Subnets:**  
  - 2 × **private** — `10.0.1.0/24`, `10.0.2.0/24`  
  - 2 × **public** — `10.0.3.0/24`, `10.0.4.0/24`  
- **Internet access:** single **NAT Gateway** for private subnets  

### Kubernetes (EKS Module)
- **EKS Cluster:** named `myEKS-cluster`  
- **Cluster version:** defined in `terraform.tfvars`  
- **Managed Node Group:**  
  - At least 1 node (t3.medium by default, configurable)  
  - Nodes spread across the private subnets  
- **IAM roles & security groups** required for cluster and nodes  

> ℹ️ This repo intentionally uses a single file: **`main.tf`**, plus variable values in `terraform.tfvars`.

---

## 💡 Learning goals

- Declare and configure the **AWS provider**  
- Use Terraform Registry modules:  
  - **VPC module** for networking  
  - **EKS module** for Kubernetes cluster  
- Pass inputs like subnets, AZs, cluster name, and tags  
- Launch a managed **EKS Node Group** inside the VPC  

---

## 🧰 Prerequisites

- Terraform `>= 1.5`  
- AWS account with permissions for VPC, IAM, and EKS  
- Credentials configured via one of:  
  - `aws configure` (AWS CLI), or  
  - environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION=us-east-1`)  

---

## ▶️ How to run

From the folder containing `main.tf`:

```bash
terraform init          # Download providers and modules
terraform validate      # (optional) Static checks
terraform plan          # (optional) Preview resources
terraform apply         # Create VPC + EKS + Node Group
```

Once apply completes, update your kubeconfig:

```bash
aws eks update-kubeconfig --region us-east-1 --name myEKS-cluster
kubectl get nodes        # Verify the worker nodes are ready
```

---

## 🧹 Clean up

Destroy all resources when you’re done:

```bash
terraform destroy
```

This will delete the VPC, the EKS cluster, and the managed node group.  

---

## 💸 Cost notice

Running an **EKS cluster** with worker nodes and a NAT Gateway incurs hourly charges.  
Use `terraform destroy` after the exercise to avoid unnecessary costs.

---

## 🧭 Key elements in `main.tf`

- **`provider "aws"`** block for region setup  
- **`module "vpc"`** for network infrastructure  
- **`module "eks"`** for Kubernetes control plane & nodes  
- **`terraform.tfvars`** provides region, cluster name, and other inputs  

