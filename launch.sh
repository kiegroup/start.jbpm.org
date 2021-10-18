#!/bin/bash
cd ..
MVN_ARG_LINE=()

for arg in "$@"
do
    case "$arg" in
        *)
            MVN_ARG_LINE+=("$arg")
        ;;
    esac
done

startDateTime=`date +%s`

# check that Maven args are non empty
if [ "$MVN_ARG_LINE" != "" ] ; then
    mvnBin="mvn"
    if [ -a $M3_HOME/bin/mvn ] ; then
       mvnBin="$M3_HOME/bin/mvn"
    fi
    echo
    echo "----> Running maven build on available projects (using Maven binary '$mvnBin')"

    "$mvnBin" -v
    echo
    projects=( "*.org")

    for suffix in "${projects[@]}"; do

        for repository in $suffix;  do
        echo
            if [ -d "$repository" ]; then
                echo "==============================================================================="
                echo "$repository"
                echo "==============================================================================="

                cd $repository

                "$mvnBin" -B "${MVN_ARG_LINE[@]}"
                returnCode=$?

                if [ $returnCode != 0 ] ; then
                    exit $returnCode
                fi

                cd ..
                fi

        done;
    done;
    endDateTime=`date +%s`
    spentSeconds=`expr $endDateTime - $startDateTime`
    echo
    echo "----> Total build time: ${spentSeconds}s"

else
    echo "----> No Maven arguments skipping maven build"
fi

if [[ "$@" =~ "docker" ]]; then
    echo "----> Launching the application as docker container..."  
    docker run --rm -it -p 8090:8090 --name jbpm-bootstrap jbpm/jbpm-bootstrap-service:latest
else

	echo "----> Launching the application locally..."
	folder="*.org"
	cd $folder
	pattern="*-service"
	files=( $pattern )
	cd ${files[0]}
	executable="$(ls  *target/jbpm*.jar | tail -n1)"

    ## if on CI, we just verify the 8090 port and close the process
    if [[ -z "${CI}" ]]; then
        java -jar "$executable"
    else
        java -jar "$executable" &

        APP_PID=$!
        echo "----> Process PID is ${APP_PID}. Waiting 1m to boot."
        sleep 1m

        echo "----> Verifying if application is up."
        status_code=$(curl --write-out '%{http_code}' --silent --output /dev/null http://localhost:8090)
        exit_status=0
        if [[ ${status_code} == 200 ]]; then
            echo "----> Everything looks fine, returning"
        else   
            echo "----> Application is not responding, returning."
            exit_status=1
        fi
        kill $APP_PID
        exit ${exit_status}
    fi
fi  
