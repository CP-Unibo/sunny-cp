# haproxy-controller
kubectl delete -f haproxy_ingress.yaml

# delete conf haproxy-ingress
kubectl delete -f haproxy_configmap.yaml

# delete ingress rule
kubectl delete -f ingress_rules.yaml

# delete sunny services
kubectl delete -f http_sunny.yaml

# delete default ingress returning 404
kubectl delete -f ingress_default_backend.yaml

# delete namespace and rbac rules
kubectl delete -f rbac_rules_namespace.yml
