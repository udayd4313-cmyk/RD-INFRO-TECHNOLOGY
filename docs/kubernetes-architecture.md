# Kubernetes architecture

The `student-api` namespace isolates application resources. A Deployment maintains two or more non-root replicas and uses RollingUpdate, readiness, and liveness probes. The ClusterIP Service provides stable internal discovery; Ingress routes external HTTP traffic. ConfigMap carries non-sensitive configuration, while the example Secret documents the interface for an external secret manager. The PVC mounts durable application data. HPA scales replicas from CPU utilization. Resource requests and limits allow predictable scheduling and protect the cluster.

For blue-green delivery, deploy `student-api-blue` and `student-api-green` with identical labels except `version`; point the Service selector at the active version and switch it only after smoke tests. For canary delivery, use weighted ingress or Argo Rollouts and promote based on Prometheus error-rate alerts.
