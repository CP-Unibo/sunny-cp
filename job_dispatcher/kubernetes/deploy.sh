
# create namespace and rbac rules
kubectl apply -f rbac_rules_namespace.yml

# create default ingress returning 404
#kubectl apply -f ingress_default_backend.yaml

# create sunny services (replication number to be configured. Default is 1)
kubectl apply -f http_sunny.yaml

# add ingress rule
kubectl apply -f ingress_rules.yaml

# configure haproxy-ingress
#kubectl apply -f haproxy_configmap.yaml

# deploy haproxy-controller
#kubectl apply -f haproxy_ingress.yaml

#return the port to use to send requests
#kubectl --namespace=sunny-namespace get services | grep haproxy-ingress

#to test
# curl -H 'Host: sunny' http://IP:PORT/solvers
# curl -H 'Host: sunny' -F "-P=gecode" -F "mzn=@zebra.mzn" http://IP:PORT/process
# the ip is one of the IPs of the nodes of the cluster
# the port is the NodePort used to redirect port 80
