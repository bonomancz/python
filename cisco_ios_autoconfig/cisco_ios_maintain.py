'''
########################################################################
### Cisco IOS router administration script
### Author: jan.novotny.cz@gmail.com
### Date: 29.4.2024
########################################################################
'''

from netmiko import ConnectHandler
import netmiko
import re


hostname = "ip.address.of.a.device"
username = "user"
password = "pass"

device = {
    "device_type":"cisco_ios",
    "ip" : hostname,
    "username" : username,
    "password" : password,
    "secret" : password
}


def main():
    '''main function'''
    try:
        sshConnection = devConnect(**device)
        # show dial-peers command
        command = "show dial-peer voice summary"
        iosStr = str(execCommand(sshConnection, command))
        dialPeers = list(set(getDialPeerNumbers(iosStr))) # deduplication set

        # show voice translation-profile command
        command = "show voice translation-profile"
        iosStr = str(execCommand(sshConnection, command))
        voiceProfiles = getVoiceProfiles(iosStr)

        '''
        # remove dialpeers
        if len(dialPeers) != 0:
            commands = []
            for number in dialPeers:
                if int(number) > 6:
                    commands.append(f"no dial-peer voice {number} voip")
        print(configCommand(sshConnection, commands))
        '''

        # remove translation-profiles
        if len(voiceProfiles) != 0:
            commands = []
            for voiceProfile in voiceProfiles:
                commands.append(f"no voice translation-profile {voiceProfile}")

        print(configCommand(sshConnection, commands))

        closeConnection(sshConnection)
    except netmiko.ConnectionException as e:
        print(f"Exception: {e}")
    return 0


def getDialPeerNumbers(inputStr) -> list:
    '''IOS: get dial-peer numbers from ios output'''
    rePattern = r'\b\d{2,3}\b'
    matches = re.findall(rePattern, inputStr)
    return matches


def getVoiceProfiles(inputStr) -> list:
    '''IOS: get voice-profiles numbers from ios output'''
    rePattern = r"voice-profile-in-\d+"
    matches = re.findall(rePattern, inputStr)
    return matches


def devConnect(**dev):
    '''ssh device connection'''
    sshClient = ConnectHandler(**dev)
    sshClient.enable()
    return sshClient


def execCommand(sshConn, command) -> str:
    '''command execution function'''
    return sshConn.send_command(command)


def configCommand(sshConn, commandsList) -> str:
    '''command execution function'''
    return sshConn.send_config_set(commandsList)


def closeConnection(sshConn):
    sshConn.disconnect()


if __name__ == "__main__":
    main()
