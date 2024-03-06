
import os
import sys

def __main__():
    n_ver = 1.0
    os.system('mode 130, 80')
    os.system('color')
    _print(f"Shid's Usermaps/BT Fixer v{n_ver}", 3)
    s_template_path = '/rex/templates/ZM Mod Level/usermaps/template'
    s_share_bt_path = '/share/raw/scripts/zm/_hb21_zm_behavior.gsc'
    
    try: p_root = _get_bo3_root(s_template_path)
    except:
        _print('Could not get BO3 root dir!', 3)
        input('|> ')
        exit()

    if not _verify_valid_path(p_root, s_share_bt_path):
        _print(f'{p_root}{s_share_bt_path} not found!', 3)
        _print(f'Copy _hb21_zm_behavior.gsc into {p_root}/share/raw/scripts/zm and run this tool again.', 1)
        input('Press any key to exit.\n|> ')
        exit()
        
    if _replace_template(p_root, s_template_path): _print('Finished BT fix in ZM Mod Level template.', 1)
    else: _print('Could not do BT fix for ZM Mod Level template!', 3)
    
    if _replace_usermaps(p_root): _print('Finished BT fix in usermaps!', 1)
    else: _print('Could not do BT fix for usermaps!', 3)
    
    input('Press any key to exit! [where is the any key?]\n|> ')
        
def _get_bo3_root(s_template_path : str) -> str:

    b_ok = False
    
    try:
        p_dir_in = _strip_dir_chars(sys.argv[1])
        if _verify_valid_path(p_dir_in, s_template_path): return p_dir_in
        else: _print("Drag-dropped folder was an invalid BO3 folder.", 2)
    except: pass
    
    while not b_ok:
        _print('Enter or drag-drop BO3 root path (Call of Duty Black Ops III)', 1)

        s_dir_in = input('|> ')
        p_dir_in = _strip_dir_chars(s_dir_in)
        
        if not _verify_valid_path(p_dir_in, s_template_path):
            _print(f'Invalid BO3 root folder!', 3)
            continue
        
        b_ok = True
        return p_dir_in

def _strip_dir_chars(s_dir : str) -> str:
    return s_dir.replace('\\', '/').strip('/').replace('"', '').replace('& ', '').replace("'", "")
        
def _verify_valid_path(s_dir : str, s_template_path  : str = '') -> bool:
    if not os.path.exists(f'{s_dir}{s_template_path}'): return False
    return True
 
def _replace_template(p_root : str, s_template_path : str) -> bool:
    try:
        p_template_gsc = f'{p_root}{s_template_path}/scripts/zm/template.gsc'
        _replace_gsc(p_template_gsc, 'ZM Mod Level Template')
        
        p_template_zone = f'{p_root}{s_template_path}/zone_source/template.zone'
        _replace_zone(p_template_zone, 'ZM Mod Level Template')

        return True
    
    except: return False

def _replace_usermaps(p_root : str) -> bool:
    try:     
        p_usermaps= f'{p_root}/usermaps/'
        list_maps = [entry.name for entry in os.scandir(p_usermaps)] # for prov3ntus ;)
    except: return False

    for s_map in list_maps:
        if not s_map.startswith('zm_'): continue
            
        p_map_gsc = f'{p_usermaps}{s_map}/scripts/zm/{s_map}.gsc'
        try: _replace_gsc(p_map_gsc, s_map)
        except:
            _print(f'Failed to add GSC line to {s_map}.gsc!', 3)
            continue
            
        p_map_zone = f'{p_usermaps}{s_map}/zone_source/{s_map}.zone'
        try: _replace_zone(p_map_zone, s_map)
        except:
            _print(f'Failed to add zone line to {s_map}.zone!', 3)
            continue
        
    return True
 
def _replace_gsc(p_gsc : str, s_map : str) -> None:
    b_write_line = True
    with open(p_gsc, 'r+') as fp:
        list_lines = fp.readlines()
        for line in list_lines:
            if('function main()' in line and b_write_line):
                list_lines.insert(47, '#using scripts\zm\_hb21_zm_behavior;\n')
                fp.seek(0, 0)
                fp.writelines(list_lines)
                _print(f'Added GSC line to {s_map}.', 1)
                break
                    
            if '#using scripts\zm\_hb21_zm_behavior' in line:
                b_write_line = False
                break

def _replace_zone(p_zone : str, s_map : str) -> None:
    with open(p_zone, 'r+') as fp:
        list_lines = fp.readlines()
        b_write_line = True
        for line in list_lines:
            if 'scriptparsetree,scripts/zm/_hb21_zm_behavior.gsc' in line:
                b_write_line = False
                break
                    
        if b_write_line:
            list_lines.append('scriptparsetree,scripts/zm/_hb21_zm_behavior.gsc')
            fp.seek(0, 0)
            fp.writelines(list_lines)
            _print(f'Added zone line to {s_map}.', 1)

def _print(s_msg : str, n_flag : int = 0) -> None:
    match(n_flag):
        case 1: print(f'\033[92m{s_msg}\033[0m') # ok
        case 2: print(f'\033[93m{s_msg}\033[0m') # warn
        case 3: print(f'\033[91m{s_msg}\033[0m') # fail
        case _: print(s_msg) # normal

# +++ main
if __name__ == '__main__': __main__()
# --- main
