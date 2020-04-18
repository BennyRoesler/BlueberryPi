#Formatted printing for services. Need to figure out handling lists 'service_classes' and 'profiles', though maybe not useful
def printServices(services):
    if(len(services) == 0):
        print("No results")
    else:
        host = "Host"
        name = "Name"
        description = "Description"
        provider = "Provider"
        protocol = "Protocol"
        port = "Port"
        service_classes = "Service Classes"
        profiles = "Profiles"
        print(f"|{host:^20}|{name:^30}|{description:^20}|{provider:^20}|{protocol:^20}|{port:^20}")
        for match in services:
            host = "None" if match["host"] is None else match["host"]
            name = "None" if match["name"] is None else match["name"]
            description = "None" if match["description"] is None else match["description"]
            provider = "None" if match["provider"] is None else match["provider"]
            protocol = "None" if match["protocol"] is None else match["protocol"]
            port = "None" if match["port"] is None else match["port"]
            service_classes = "None" if match["service-classes"] is None else match["service-classes"]
            profiles = "None" if match["profiles"] is None else match["profiles"]
            print(f"|{host:^20}|{name:^30}|{description:^20}|{provider:^20}|{protocol:^20}|{port:^20}")
