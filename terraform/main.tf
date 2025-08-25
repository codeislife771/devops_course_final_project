terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Get available AZs
data "aws_availability_zones" "available" {}

data "aws_caller_identity" "current" {}

# Minimal VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.cluster_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = slice(data.aws_availability_zones.available.names, 0, 2)
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.3.0/24", "10.0.4.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  # Standard tags only (public = ELB, private = internal ELB)
  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }
}

# EKS (single managed node group)
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name                   = var.cluster_name
  cluster_version                = "1.29"
  vpc_id                         = module.vpc.vpc_id
  subnet_ids                     = module.vpc.private_subnets
  control_plane_subnet_ids       = module.vpc.private_subnets
  cluster_endpoint_public_access = true
  enable_irsa                    = true
  authentication_mode = "API_AND_CONFIG_MAP"

  # Essential add-ons only
  cluster_addons = {
    coredns    = { most_recent = true }
    kube-proxy = { most_recent = true }
    vpc-cni    = { most_recent = true }
  }

  # Map your IAM identity to Kubernetes RBAC using EKS Access Entries.
  # IMPORTANT: principal_arn must exactly match who runs kubectl.
  # Run: aws sts get-caller-identity  -> copy the "Arn" and use it here (user or role).
  access_entries = {
    admin = {
      # Example for an IAM User named "dan_user"
      principal_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/dan_user"

      policy_associations = {
        admin = {
          # Grant cluster-admin rights using EKS Cluster Access Policy (not generic IAM AdministratorAccess)
          policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"

          # Cluster-wide access (you can restrict to specific namespaces later if needed)
          access_scope = {
            type       = "cluster"
          }
        }
      }
    }
  }

  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.small"]

      min_size     = 0
      max_size     = 2
      desired_size = 1

      disk_size     = 20
      capacity_type = "SPOT"
    }
  }
}

# Simple outputs
output "cluster_name" {
  value = module.eks.cluster_name
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "update_kubeconfig_command" {
  value = "aws eks update-kubeconfig --region ${var.region} --name ${var.cluster_name}"
}
