# What are scenarios?

Scenarios are typical attack case scenario files that allows us to change our infrastructure, which can allow us to expose specific attack vectors.
The predefined scenarios are based on the [Mitre attack framework](https://attack.mitre.org/).

## How are scenarios implemented?

Each scenario file in this directory contains only sections that we want to modify\add to the existing `network.json` topology file.

For example, if we want to add the `Unquoted Service Paths` attack technique to our existing `ws01` host. We will simply create the following scenario file:

```json
{
    "hosts": {
        "ws01": {
            "files": {
                "SinCityLogger.exe": "C:\\Program Files"
            },
            "win_services": {
                "SinCityLogger": {
                    "binpath": "C:\\Program Files\\SinCityLogger.exe",
                    "description": "Service that run under Domain Admin context",
                    "username": "basin.local\\dwight.mccarthy",
                    "password": "dkzs3f1A"
                }
            }
        }
    }
}
```

This is a an actual existing attack technique from [Mitre 1574.009](https://attack.mitre.org/techniques/T1574/009/).

The following scenario file will be merged with the existing `network.json` file, and a new `network.json` file will be created containing the new fields.

Pay attention that all existing `network.json` fields are not removed, they are actually being merged. If the host `ws01` already exists, the fields above will not be overwritten, but merged.

## Applying a scenario\multiple scenarios

You can apply a scenario with the following command:

```bash
# Apply the scenario T1574.009 mentioned above and merge with the existing `network.json`
sincity build --scenarios=T1574.009
```

You can also apply multiple scenarios:

```bash
sincity build --scenarios=T1574.009,T1558.004
```

You can also apply all scenarios using this command:

```bash
sincity build --scenarios=all
```

## Building your own generic scenario

Building a scenario can be easy, but modifying it to fit different topologies will require us to build it in a generic way using `Jinja 2` templating language.

Let's take a look at the example of `Unquoted Service Paths` (☝️), the JSON file is built too specific, and points to specific hosts. What if for example, we wanted it to be deployed into our main workstation?

We can simply use `Jinja 2` templating language and replace `ws01` with a generic variable called: `{{ main_workstation.key }}`. If the topology we are basing at (which is `network.json` by default), has a workstation with the variable `main_workstation` attached, it will use that as variable.

For example, let's take a look at this part of the `network.json` file:

```json
        ...
        "hosts": {
            ...
            "ws01": {
                "name": "ws01",
                "variable": "main_workstation", # <----- This is our variable
                "ip": "10.0.100.30",
                "type": "windows",
                "role": "workstation",
                "domain": "basin.local",
                "users": {
                    "locally": {
                        "password": "Aa123456"
                    }
                }
            },
            ...
        },
        ...
```

Now we can write a generic `scenario` file:

```json
{
    "hosts": {
        "{{ main_workstation.key }}": { # <----- This will be replaced with our workstation name instead
            "files": {
                "SinCityLogger.exe": "C:\\Program Files"
            },
            "win_services": {
                "SinCityLogger": {
                    "binpath": "C:\\Program Files\\SinCityLogger.exe",
                    "description": "Service that run under Domain Admin context",
                    "username": "basin.local\\dwight.mccarthy",
                    "password": "dkzs3f1A"
                }
            }
        }
    }
}
```