while :
do
  /usr/local/opt/python@3.8/bin/python3.8 get_data.py http://10.17.0.242:9090 nginx_ingress_controller_requests#statements
  sleep 10
done
