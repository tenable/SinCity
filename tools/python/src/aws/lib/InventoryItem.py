class InventoryItem:
    """
    Represents an inventory item, which later on will be used by ansible.
    """

    def __init__(self, instance) -> None:
        self.instance = instance

        # Populate all of the tags as key\value pair
        self.tags = {}

        # If there are no tags for this instance
        if instance.tags is None:
            return

        for tag in instance.tags:
            self.tags[tag['Key']] = tag['Value']

    def parse_inventory_keyvalues(self, keyvalues: dict) -> str:
        output = ''

        for key in keyvalues:
            output += f'{key}={keyvalues[key]} '

        # Remove the last ','
        output = output[:-1]

        return output

    @property
    def application_role(self) -> str:
        return 'Application Role' in self.tags and self.tags['Application Role']

    @property
    def project(self) -> str:
        return 'Project' in self.tags and self.tags['Project']

    @property
    def operating_system(self) -> str:
        return 'Operating System' in self.tags and self.tags['Operating System']

    @property
    def instance_ip(self) -> str:
        return self.instance.public_ip_address

    @property
    def instance_name(self) -> str:
        return 'Name' in self.tags and self.tags['Name']

    @property
    def is_customer(self) -> bool:
        return 'Customer' in self.tags

    @property
    def customer_name(self) -> str:
        return self.tags['Customer']

    @property
    def fixed_customer_name(self) -> str:
        """
        Replaces special characters with the customer name to be parsed correctly later on with ansible.
        """
        return self.customer_name.replace('-', '_')

    @property
    def keypair_name(self) -> str:
        return (self.instance.key_pair and self.instance.key_pair.key_name) or 'no_keypair'

    @property
    def server_username(self) -> str:
        """
        Returns the username associated with the server.
        """
        return 'Server Username' in self.tags and self.tags['Server Username']

    @property
    def inventory_entry(self) -> str:
        """
        Returns a single inventory entry, for example: 'dc01    ansible_host=3.55.12.3.
        """
        return f'{self.instance_name}   ansible_host={self.instance_ip}'

    @property
    def file_entries(self) -> dict:
        """
        Returns a dictionary containing all of the files name with the associated section and entries.

        For example: { "customers.ini": { "cal": 83.42.41.2 }}
        """
        if not hasattr(self, '_file_entries'):
            output = {}

            # The key\value pairs to bet written inside the invetory
            key_values = {'ansible_host': self.instance_ip,
                          'ansible_ssh_private_key_file': f'keys/{self.keypair_name}.pem'}

            # If this server has a username provided, use it
            if self.server_username:
                key_values['ansible_user'] = self.server_username

            parsed_key_values = self.parse_inventory_keyvalues(key_values)

            if self.is_customer:
                output['customers'] = {
                    f'customer_{self.fixed_customer_name}': f'{self.application_role or "no_role"}_{self.fixed_customer_name} {parsed_key_values}'
                }

            if self.application_role:
                entry_value = self.instance_ip if not self.is_customer else f'{self.application_role}_{self.fixed_customer_name} {parsed_key_values}'
                output['applications'] = {
                    self.application_role: entry_value
                }

            self._file_entries = output

        return self._file_entries
