#! /usr/bin/python3

from argparse import ArgumentParser
from requests import Session, Request
import json
import sys
import csv

def main():
    # create the top-level parser
    parser = ArgumentParser(prog='shelly')
    parser.add_argument('--host', help='IP adress or FQDN of the shelly device', default='10.0.0.250', metavar='device_ip')
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="Enable verbosity")
    parser.add_argument("-p", "--pretty-print", action="store_true", help="Pretty print output")

    # Create subparsers
    subparsers_base = parser.add_subparsers(title='component', dest='component')

    create_scripts_menu(subparsers_base)
    create_switch_menu(subparsers_base)

    # Execute parsing
    args = parser.parse_args()

    if args.verbosity >= 2:
        debug(2, f"{args}", args)

    if hasattr(args, 'func'):
        args.func(args)
    #elif hasattr(args, 'component') and args.component != None:
    else:
        parser.print_usage()

def create_scripts_menu(subparsers_base):
    parser_scripts = subparsers_base.add_parser('scripts', help='Shelly Scripts Menu')
    subparsers_scripts = parser_scripts.add_subparsers(title='action', dest='action')

    # Create common argument parser for start, getcode, stop, exec, update and delete endpoints
    adressable_parser = ArgumentParser(add_help=False)
    adressable_parser.add_argument('id', help='Script slot id', type=int)

    # Create common argument parser for create and update endpoints
    file_transporting_parser = ArgumentParser(add_help=False)
    file_transporting_parser.add_argument('file', help='Script file', type=str)
    file_transporting_parser.add_argument('--chunk-size', help='Size of uploaded chunks', type=int, default=1024)

    # Create the parser for the "list" command
    parser_list = subparsers_scripts.add_parser('list', help='List scripts on the Shelly device')
    parser_list.add_argument('-e', '--enabled', action="store_true", help='Filter enabled script')
    parser_list.set_defaults(func=list_scripts)

    # Create the parser for the "create" command
    parser_create = subparsers_scripts.add_parser('create', help='Create a script on the Shelly device', parents=[file_transporting_parser])
    parser_create.add_argument('name', help='Name of your script')
    parser_create.set_defaults(func=create_script)

    # Create the parser for the "start" command
    parser_start = subparsers_scripts.add_parser('start', help='Start a script on the Shelly device', parents=[adressable_parser])
    parser_start.set_defaults(func=start_script)

    # Create the parser for the "eval" command
    parser_eval = subparsers_scripts.add_parser('eval', help='Execute a script on the Shelly device', parents=[adressable_parser])
    parser_eval.add_argument('code', help='Code to evaluate', type=str)
    parser_eval.set_defaults(func=eval_script)

    # Create the parser for the "call" command
    parser_call = subparsers_scripts.add_parser('call', help='Call a script registered HTTP API', parents=[adressable_parser])
    parser_call.add_argument('endpoint', help='API endpoint to call', type=str)
    parser_call.set_defaults(func=call_script_api)

    # Create the parser for the "stop" command
    parser_stop = subparsers_scripts.add_parser('stop', help='Stop a script on the Shelly device', parents=[adressable_parser])
    parser_stop.set_defaults(func=stop_script)

    # Create the parser for the "getcode" command
    parser_get_code = subparsers_scripts.add_parser('getcode', help='Downloads code from an existing script', parents=[adressable_parser])
    parser_get_code.set_defaults(func=get_code_script)

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



def debug(verbosity, message, args, end='\n'):
    if (args.verbosity >= verbosity):
        print(f"[debug{verbosity}] {message}", file=sys.stderr, end=end)

def debug_request(req, args):
    debug(3, '{}\n{}\r\n{}\r\n\r\n{}'.format(
        'The following HTTP request have been sent:',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ), args)


# RPC help functions

def format_url(base, endpoint, protocol='http://', section='/rpc'):
    return f"{protocol}{base}{section}/{endpoint}"

def print_response(json_payload, args):
    if args.pretty_print :
        response = json.dumps(json_payload, sort_keys=True, indent=4)
    else :
        response = json.dumps(json_payload)
    response = response.strip('"')
    print(response)
    return response

def call_shelly(request, args):
    debug(1, f"Calling endpoint {request.url}", args)
    debug_request(request.prepare(), args)
    if len(request.url) > 8000: # https://www.rfc-editor.org/rfc/rfc9110#name-uri-references
        debug(3, f"Your Request url is {len(request.url)} long. That may be a problem !")
    response = Session().send(request.prepare())
    debug(1, f"Response Payload : {response.text}", args, end="")

    if response.ok:
        return response
    else:
        print(f"Error ({response.status_code}) executing method : {response.json()['message']}", file=sys.stderr)
        sys.exit(2)

def upload_file_in_chunks(args, endpoint):
    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    debug(2, f"Script Payload has length {len(code)} bytes. You will need {(len(code)//args.chunk_size) + 1} chunk(s)", args)

    url = format_url(args.host, endpoint)
    request_data = {'id': args.id, 'append': False}

    pos = 0
    append = False
    while pos < len(code):
        chunk = code[pos : pos + args.chunk_size]
        pos += len(chunk)
        
        request_data['code'] = chunk
        request_json = json.dumps(request_data, ensure_ascii=False)
        request = Request('POST', url, data=request_json.encode('utf-8'))
        call_shelly(request, args)
        request_data['append'] = True


# Core Scripts functions

def list_scripts(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptlist
    """
    url = format_url(args.host, 'Script.List')

    debug(2, f"List scripts", args)

    request = Request('GET', url)
    response = call_shelly(request, args)
    print_response(response.json()['scripts'], args)

def create_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptcreate
    """
    url = format_url(args.host, 'Script.Create')

    debug(2, f"Create script {args.name} from file {args.file}", args)

    request = Request('GET', url, params={'name': f"\"{args.name.strip()}\""})
    response = call_shelly(request, args)

    args.id = response.json()['id']
    upload_file_in_chunks(args, 'Script.PutCode')
    print(args.id)

def start_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptstart
    """
    url = format_url(args.host, 'Script.Start')

    debug(2, f"Start script {args.id}", args)

    request = Request('GET', url, params={'id': args.id})
    response = call_shelly(request, args)
    print_response(response.json(), args)

def get_code_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptgetcode
    """
    url = format_url(args.host, 'Script.GetCode')
    request = Request('GET', url, params={'id': args.id})
    response = call_shelly(request, args)
    print_response(response.json()['data'], args)

def eval_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scripteval
    """
    debug(2, f"Start script {args.id} with params : \"{args.code}\"", args)
    url = format_url(args.host, 'Script.Eval')
    req_params = {'id': args.id}
    if args.code:
        req_params['code'] = f"\"{args.code}\""
    
    request = Request('GET', url, params=req_params)
    response = call_shelly(request, args)
    
    result = response.json()['result']
    try:
        json_result = json.loads(result)
        print_response(json_result, args)
    except ValueError as e:
        debug(3, f"Result payload is not json : {e}", args)
        print_response(result, args)

def call_script_api(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/Scripts/ShellyScriptLanguageFeatures/#httpserverregisterendpoint
    """
    debug(2, f"Call script {args.id} API with endpoint : \"{args.endpoint}\"", args)
    url = format_url(args.host, section="/script", endpoint=f"{args.id}/{args.endpoint}")
    
    request = Request('GET', url)
    response = call_shelly(request, args)
    
    result = response.json()
    # power_data = [result['current'], result['power'], result['timestamp'], result['voltage']]
    # write_to_csv('power_measurements.csv', power_data, header=['Current', 'Power', 'Timestamp', 'Voltage'])
    try:
        json_result = json.loads(result)
        csv_result= list_to_csv_dicts(result, "shelly_meas.csv")
        print_response(csv_result, args)
    except (ValueError, TypeError) as e:
        debug(3, f"Result payload is not json : {e}", args)
        print_response(result, args)
        
def list_to_csv_dicts(my_list, file_name):
    if not my_list:
        return  # Exit if the list is empty

    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=my_list[0].keys())
        writer.writeheader()
        for item in my_list:
            writer.writerow(item)

def stop_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptstop
    """
    url = format_url(args.host, 'Script.Stop')

    debug(2, f"Stop script {args.id}", args)

    request = Request('GET', url, params={'id': args.id})
    response = call_shelly(request, args)
    print_response(response.json(), args)

def update_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptputcode
    """
    debug(2, f"Update script {args.id} with file {args.file}", args)

    upload_file_in_chunks(args, 'Script.PutCode')

def delete_script(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script#scriptdelete
    """
    url = format_url(args.host, 'Script.Delete')

    debug(2, f"Delete script {args.id}", args)

    request = Request('GET', url, params={'id': args.id})
    call_shelly(request, args)

# Switch functions
def switch_get_status(args):
    """
    Calling endpoint https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Switch#switchgetstatus
    """
    url = format_url(args.host, 'Switch.GetStatus')
    request = Request('GET', url, params={'id': args.id})
    response = call_shelly(request, args)
    print_response(response.json(), args)

    data = response.json()
    # Prepare data to be written, e.g., [data['power'], data['timestamp']]
    prepared_data = [data['key1'], data['key2'], ...]  # Replace with actual keys
    write_to_csv('shelly_measurements.csv', prepared_data, header=['Power', 'Timestamp'])


def write_to_csv(file_name, data, header=None):
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        if header:
            writer.writerow(header)
        writer.writerow(data)


if __name__ == '__main__':
    main()


