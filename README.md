# gradle dependency mapper for Nexus IQ
Nexus IQ at this time doesnt manage direct and transitive dependencies for gradle correctly. This helper script reads the Nexus IQ results file and matches policy violations to `build.gradle` files and direct dependencies.

## Usage
```bash
# scan the project and get the results file
docker run -v `pwd`:/scan sonatype/nexus-iq-cli /sonatype/evaluate -a $USER:$PASS -s https://$IQSVR:$IQPORT -i $APP_NAME -r /scan/iqresults.json /scan

# map the dependencies
./gradle-direct-depends-mapper.py -r iqresults.json
```