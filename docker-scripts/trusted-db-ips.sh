echo "$ENVIRONMENT"
if [ "$ENVIRONMENT" = "Production" ]
then
	sed -i d /var/lib/postgresql/data/pg_hba.conf
	echo "host all  postgres  ::1/128	  		md5" >> /var/lib/postgresql/data/pg_hba.conf
	# add trusted remote ip addresses you want to allow connections to the database
fi