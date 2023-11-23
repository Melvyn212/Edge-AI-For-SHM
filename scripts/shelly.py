#! /usr/bin/python3

import argparse
import requests
import json
import sys

def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='shelly')
    parser.add_argument('-t', '--target', help='IP adress or FQDN of the shelly device', default='10.0.0.250', metavar='device_ip')
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="Enable verbosity")
    parser.add_argument("-p", "--pretty-print", action="store_true", help="Pretty print output")

    # Create subparsers
    subparsers_base = parser.add_subparsers(title='component', dest='component')

    create_scripts_menu(subparsers_base)
    create_switch_menu(subparsers_base)

    # Execute parsing
    args = parser.parse_args()

    if args.verbosity >= 2:
        print(f"debug2: {args}")

    if hasattr(args, 'func'):
        args.func(args)
    #elif hasattr(args, 'component') and args.component != None:
    else:
        parser.print_usage()

def create_scripts_menu(subparsers_base):
    parser_scripts = subparsers_base.add_parser('scripts', help='Shelly Scripts Menu')
    subparsers_scripts = parser_scripts.add_subparsers(title='action', dest='action')

    # Create common argument parser for start, stop, exec, update and delete endpoints
    adressable_parser = argparse.ArgumentParser(add_help=False)
    adressable_parser.add_argument('id', help='Script slot id', type=int)

    # Create common argument parser for create and update endpoints
    file_transporting_parser = argparse.ArgumentParser(add_help=False)
    file_transporting_parser.add_argument('file', help='Script file', type=str)

    # Create the parser for the "list" command
    parser_list = subparsers_scripts.add_parser('list', help='List scripts on the Shelly device')
    parser_list.add_argument('-e', '--enabled', action="store_true", help='Filter enabled script')
    parser_list.set_defaults(func=list_scripts)

    # Create the parser for the "create" command
    parser_create = subparsers_scripts.add_parser('create', help='Create a script on the Shelly device', parents=[file_transporting_parser])
    parser_create.add_argument('title', help='Name of your script')
    parser_create.set_defaults(func=create_script)

    # Create the parser for the "start" command
    parser_start = subparsers_scripts.add_parser('start', help='Start a script on the Shelly device', parents=[adressable_parser])
    parser_start.set_defaults(func=start_script)

    # Create the parser for the "exec" command
    parser_exec = subparsers_scripts.add_parser('exec', help='Execute a script on the Shelly device', parents=[adressable_parser])
    parser_exec.add_argument('code', help='Argument to evaluate', type=str)
    parser_exec.set_defaults(func=exec_script)

    # Create the parser for the "stop" command
    parser_stop = subparsers_scripts.add_parser('stop', help='Stop a script on the Shelly device', parents=[adressable_parser])
    parser_stop.set_defaults(func=stop_script)

    # Create the parser for the "update" command
    parser_update = subparsers_scripts.add_parser('update', help='Update a script on the Shelly device', parents=[adressable_parser,file_transporting_parser])
    parser_update.set_defaults(func=update_script)

    # Create the parser for the "delete" command
    parser_delete = subparsers_scripts.add_parser('delete', help='Delete a script on the Shelly device', parents=[adressable_parser])
    parser_delete.set_defaults(func=delete_script)

def create_switch_menu(subparsers_base):
    parser_switch = subparsers_base.add_parser('switch', help='Shelly Switch Menu')
    parser_switch.add_argument('--id', help='Id of the Switch component instance', type=int, default=0)

    subparsers_switch = parser_switch.add_subparsers(title='action', dest='action')


    parser_switch_status = subparsers_switch.add_parser('status', help='Get the status of the Switch component')
    parser_switch_status.set_defaults(func=switch_get_status)



# RPC help functions

def format_endpoint(base, endpoint):
    return 'http://'+base+'/rpc/'+endpoint

def print_response(json_payload, args):
    if args.pretty_print :
        print(json.dumps(json_payload, sort_keys=True, indent=4))
    else :
        print(json.dumps(json_payload))

def call_shelly(request, args):
    if args.verbosity >= 1:
        print(f"[debug1] Calling endpoint {request.url}")

    response = requests.Session().send(request.prepare())

    if args.verbosity >= 1:
        print(f"[debug1] Response Payload : {response.text}", end="")

    if response.ok:
        return response
    else:
        print(f"Error ({response.status_code}) executing method : {response.json()['message']}", file=sys.stderr)
        sys.exit(2)
    


# Core Scripts functions

def list_scripts(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptlist
    """
    endpoint = format_endpoint(args.target, 'Script.List')
    request = requests.Request('GET', endpoint)
    response = call_shelly(request, args)
    print_response(response.json()['scripts'], args)


def create_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptcreate
    """
    script_name = args.title
    script_file_name = args.file
    endpoint = format_endpoint(args.target, 'Script.Create')
    print(f"Create script {script_name} from file {script_file_name}")


def start_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptstart
    """
    script_id = args.id
    endpoint = format_endpoint(args.target, 'Script.Start')
    print(f"Start script {script_id}")


def exec_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scripteval
    """
    script_id = args.id
    param_str = args.code
    endpoint = format_endpoint(args.target, 'Script.Eval')
    print(f"Start script {script_id} with params : \"{param_str}\"")


def stop_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptstop
    """
    script_id = args.id
    endpoint = format_endpoint(args.target, 'Script.Stop')
    print(f"Stop script {script_id}")


def update_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptputcode
    """
    script_id = args.id
    script_file_name = args.file
    endpoint = format_endpoint(args.target, 'Script.PutCode')
    print(f"Update script {script_id} with file {script_file_name}")


def delete_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptdelete
    """
    script_id = args.id
    endpoint = format_endpoint(args.target, 'Script.Delete')
    print(f"Delete script {script_id}")

# Switch functions
def switch_get_status(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Switch#switchgetstatus
    """
    switch_id = args.id
    endpoint = format_endpoint(args.target, 'Switch.GetStatus')
    request = requests.Request('GET', endpoint, params={'id': switch_id})
    response = call_shelly(request, args)
    print_response(response.json(), args)

if __name__ == '__main__':
    main()
