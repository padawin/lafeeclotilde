docker exec -it db-lafeeclotilde psql -U postgres -c 'DROP DATABASE lafeeclotilde;'
docker exec -it db-lafeeclotilde psql -U postgres -c 'CREATE DATABASE lafeeclotilde;'
docker exec -it db-lafeeclotilde psql -U postgres lafeeclotilde -a -f /tmp/data/initial.sql
