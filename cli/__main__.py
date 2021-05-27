from argparse import ArgumentParser
from .init_groups import fill_groups
from .refresh_user_props import refresh_users
from .verify_server import verify_server

ACTION_REFRESH_USERS = 'refresh-users'
ACTION_FILL_GROUPS = 'fill-groups'
ACTION_VERIFY_SERVER = 'verify-server'

if __name__ == '__main__':
    parser = ArgumentParser(description='CLI Utils for SESC MATE.')
    parser.add_argument('action', help='Action', nargs='?', type=str,
                        choices=[ACTION_REFRESH_USERS, ACTION_FILL_GROUPS, ACTION_VERIFY_SERVER])
    opts, rem_args = parser.parse_known_args()
    action = opts.action

    parser.add_argument('--token', help='VK service token (verify-server, refresh-urls)', type=str,
                        required=action == ACTION_VERIFY_SERVER or action == ACTION_REFRESH_USERS)
    parser.add_argument('--server-id', help='Server ID (verify-server)', type=int,
                        required=action == ACTION_VERIFY_SERVER)
    parser.add_argument('--group-id', help='Group ID (verify-server)', type=int,
                        required=action == ACTION_VERIFY_SERVER)
    parser.add_argument('--api-endpoint', help='API endpoint  (verify-server)', type=str,
                        required=action == ACTION_VERIFY_SERVER)

    args = parser.parse_args(rem_args, namespace=opts)

    if action == ACTION_VERIFY_SERVER:
        verify_server(args.token, args.api_endpoint, args.group_id, args.server_id)
    elif action == ACTION_REFRESH_USERS:
        refresh_users(args.token)
    elif action == ACTION_FILL_GROUPS:
        fill_groups()
