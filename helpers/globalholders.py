# globalholders - Holder for global variables
# We use some global variables, not sure this
# is the best practice, but here they are.
#
# Marcelo Feitoza Parisi (marcelo@feitoza.com.br)

# To handle database connection for our route table
databaseConnection = None
# To handle kubernetes API connection
coreApi = None
# To hold Config Path
configPath = "/etc/config"
# Termination Device
terminationDevice = "/dev/termination-log"
# Route Table Path
routeTable = "/var/run/routes"