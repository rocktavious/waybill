waybill
=======

A python commandline tool to run commandline tools that are housed in docker images to make them like binary installs

Per present day shipping terms:
A "Waybill" is a non-negotiable document prepared by or on behalf of the carrier at origin. The document shows origin point, destination, route, consignor, consignee, shipment description and amount charged for the transportation service.

Waybill takes this concept and applys it to the docker ecosystem and gives you a commandline interface to create, share and use these shell environment shims to run tools contained in docker images, but automates the docker parts to make it so these docker images act like binary distributions.
All you do is define the necessary parameters and a shim will be created that you can use in your shell environment

# This is the creation interface for waybills
waybill create "mycustomtool" "docker.sample.com/mycustomtool:latest"

# This is an alternative command to create that helps you import waybill yaml definitions so you can share them with others easily
# You could also just share your ~/.waybills directory
waybill load waybills.yaml

# For more documentation see
waybill --help

# After the waybills have been defined/setup
$(waybill shellinit) # this could be run in .bash_rc or .profile or similar

# Now a custom shim should be in place
mycustomtool --version # will run the shim that runs a docker pull and docker run for the predefined image with the given command name and args
