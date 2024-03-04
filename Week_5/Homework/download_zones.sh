# To exit bash script in case we get 404
set -e

# # Define variables
# TAXI_TYPE=$1 # $1 signifies the first argument in bash command
# YEAR=$2

URL_PREFIX="https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

URL="${URL_PREFIX}/misc/taxi_zone_lookup.csv"

LOCAL_PREFIX="data/misc/"
LOCAL_FILE="taxi_zone_lookup.csv"
LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

echo "downloading ${URL} to ${LOCAL_PATH}..."
mkdir -p ${LOCAL_PREFIX}
wget ${URL} -O ${LOCAL_PATH}
echo "...successfully downloaded ${URL} to ${LOCAL_PATH}"
