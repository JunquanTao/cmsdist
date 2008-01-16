### RPM cms dbs-server DBS_1_0_8

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Servers/JavaServer&export=DBS&tag=-r%{cvstag}&output=/dbs-server.tar.gz
Requires: apache-ant mysql mysql-deployment oracle apache-tomcat java-jdk dbs-schema

%prep
%setup -n DBS

%build
echo "PWD=$PWD"
cd Servers/JavaServer
# fix context.xml file
cat > etc/context.xml << EOF_CONTEXT
     <Resource name="jdbc/dbs"
              auth="Container"
              type="javax.sql.DataSource"
              maxActive="30"
              maxIdle="10"
              maxWait="10000"
              username="dbs"
              password="cmsdbs"
              driverClassName="org.gjt.mm.mysql.Driver"
              url="jdbc:mysql://localhost:3316/%{cvstag}?autoReconnect=true"/>
EOF_CONTEXT

mkdir -p bin/WEB-INF/lib
echo "PWD=$PWD"
source $JAVA_JDK_ROOT/etc/profile.d/init.sh
export JAVA_HOME=$JAVA_JDK_ROOT 
ant --noconfig dist
cd ../../

%install
mkdir -p %{i}/Servers/JavaServer/bin/WEB-INF/lib
cp -r Servers/JavaServer/* %{i}/Servers/JavaServer

# copy war file
cp %{i}/Servers/JavaServer/DBS.war $APACHE_TOMCAT_ROOT/webapps

mkdir -p %{i}/etc/profile.d
(echo "#!/bin/sh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_DEPLOYMENT_ROOT/etc/profile.d/init.sh"; \
 echo "source $APACHE_TOMCAT_ROOT/etc/profile.d/init.sh"; \
 echo "source $APACHE_ANT_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_SCHEMA_ROOT/etc/profile.d/init.sh"; \
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.csh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.csh"; \
 echo "source $MYSQL_DEPLOYMENT_ROOT/etc/profile.d/init.csh"; \
 echo "source $APACHE_TOMCAT_ROOT/etc/profile.d/init.csh"; \
 echo "source $APACHE_ANT_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_SCHEMA_ROOT/etc/profile.d/init.csh"; \
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.csh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

 
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

# setup MySQL server
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
VO_CMS_SW_DIR=`echo $DBS_SERVER_ROOT | awk '{split($1,a,SCRAM_ARCH); print a[1]}' SCRAM_ARCH=$SCRAM_ARCH`
export VO_CMS_SW_DIR
$MYSQL_DEPLOYMENT_ROOT/bin/mysql-deployment.sh

# set DBS DBs
MYSQL_PORT=3316
MYSQL_PATH=$MYSQL_ROOT/mysqldb
MYSQL_SOCK=$MYSQL_PATH/mysql.sock
MYSQL_PID=$MYSQL_PATH/mysqld.pid
MYSQL_ERR=$MYSQL_PATH/error.log
# grant permissions to CMS MySQL DBS account
echo "+++ Grand permission to dbs account, DBS DB ${DBS_SCHEMA_VERSION} ..."
echo "$MYSQL_ROOT/bin/mysql -udbs -pcmsdbs --socket=$MYSQL_SOCK"
echo "$DBS_SCHEMA_ROOT/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql"
# DBS uses trigger which requires to have SUPER priveleges, so we'll create DB using root
# and delegate this to dbs account.
$MYSQL_ROOT/bin/mysql -uroot -pcms --socket=$MYSQL_SOCK < $DBS_SCHEMA_ROOT/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql
$MYSQL_ROOT/bin/mysql --socket=$MYSQL_SOCK -uroot -pcms mysql -e "GRANT ALL ON ${DBS_SCHEMA_VERSION}.* TO dbs@localhost;"
