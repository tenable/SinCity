<powershell>
Import-Module AWSPowerShell
# $SecretAD = "admin_pwd"
# $SecretObj = (Get-SECSecretValue -SecretId $SecretAD)
# $Secret = ($SecretObj.SecretString  | ConvertFrom-Json)
# $password   = $Secret.Password | ConvertTo-SecureString -asPlainText -Force

echo "Setup ansible script loaded" >  ~/terrform.txt

 # Username and Password
$username = "root"
$password = ConvertTo-SecureString "Aa123456!" -AsPlainText -Force  # Super strong plane text password here (yes this isn't secure at all)

# Creating the user
New-LocalUser -Name "$username" -Password $password -FullName "$username" -Description "Root user for ansible"
Add-LocalGroupMember -Group "Administrators" -Member "$username"

Invoke-Expression ((New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/ansible/ansible/stable-2.6/examples/scripts/ConfigureRemotingForAnsible.ps1'))
Invoke-Expression ((New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/jborean93/ansible-windows/master/scripts/Install-WMF3Hotfix.ps1'))
</powershell>
