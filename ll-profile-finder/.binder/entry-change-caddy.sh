## This script is run by the entrypoint.sh script in the Coder image.
## It is used to configure Caddy as a reverse proxy for the Coder service
## that removes the /user/username/ prefix from the URL because Coder needs to get acessed at the root URL.


echo "Setting up Caddy as reverse proxy for Coder"

## JUPYTERHUB_SERVICE_PREFIX is the prefix of the URL that the JupyterHub proxy will use to access this service.
## It is of the form: /user/my-name/ - so it has a leading and trailing slash.
BASE_PATH=${JUPYTERHUB_SERVICE_PREFIX-/}

echo "Using BASE_PATHfor reverse proxy: $BASE_PATH"

cat > /etc/caddy/Caddyfile <<EOF
# The Caddyfile is an easy way to configure your Caddy web server.
:8888 {
    # Set this path to your site's directory.
    # root * /usr/share/caddy

    # Enable the static file server.
    # file_server

    handle_path ${BASE_PATH}* {
        # uri strip_prefix $BASE_PATH
        reverse_proxy 127.0.0.1:8080
    }
}

EOF

## Actually start Caddy - in background
echo "Starting Caddy"
caddy run --config /etc/caddy/Caddyfile &
