import numpy as np
import pickle
from easydict import EasyDict as edict
import logging
import os
from pathlib import Path

def get_mypkg_path(max_iter=5):
    """Find the mypkg folder under the current working directory 
    args: 
        - max_iter: int, the maximum number of iterations to go up the directory tree
    """
    work_path = Path(os.getcwd())
    cur_path = work_path

    mypkg_path = None
    # find the mypkg folder under work_path
    for i in range(max_iter):
        if (cur_path/"mypkg").exists():
            mypkg_path = cur_path/"mypkg"
            break
        else: 
            cur_path = cur_path.parent
    if mypkg_path is None:
        raise FileNotFoundError("Cannot find mypkg folder")
    return str(mypkg_path)

def _set_verbose_level(verbose, logger):
    """Set the verbose level of logger
    """
    if verbose == 0:
        verbose_lv = logging.ERROR
    elif verbose == 1:
        verbose_lv = logging.WARNING
    elif verbose == 2:
        verbose_lv = logging.INFO
    elif verbose == 3:
        verbose_lv = logging.DEBUG
    if len(logger.handlers)>0:
        logger.handlers[0].setLevel(verbose_lv)
    else:
        logger.setLevel(verbose_lv)

def _update_params(input_params, def_params, logger, check_ky=True):
    """Update the default parameters with input parameters
    args: 
        - input_params (dict): the input parameters
        - def_params (dict): the default parameters
        - logger (logging.Logger): the logger
        - check_ky (bool): whether to check the keys or not 
    """
    for ky, v in input_params.items():
        if ky not in def_params.keys() and check_ky:
            logger.warning(f"Check your input, {ky} is not used.")
        else:
            if v is not None:
                def_params[ky] = v
    return edict(def_params)


def load_pkl_folder2dict(folder, excluding=[], including=["*"], verbose=True):
    """The function is to load pkl file in folder as an edict
        args:
            folder: the target folder
            excluding: The files excluded from loading
            including: The files included for loading
            Note that excluding override including
    """
    if not isinstance(including, list):
        including = [including]
    if not isinstance(excluding, list):
        excluding = [excluding]
        
    if len(including) == 0:
        inc_fs = []
    else:
        inc_fs = list(set(np.concatenate([list(folder.glob(nam+".pkl")) for nam in including])))
    if len(excluding) == 0:
        exc_fs = []
    else:
        exc_fs = list(set(np.concatenate([list(folder.glob(nam+".pkl")) for nam in excluding])))
    load_fs = np.setdiff1d(inc_fs, exc_fs)
    res = edict()
    for fil in load_fs:
        res[fil.stem] = load_pkl(fil, verbose)                                                                                                                                  
    return res

# save a dict into a folder
def save_pkl_dict2folder(folder, res, is_force=False, verbose=True):
    assert isinstance(res, dict)
    for ky, v in res.items():
        save_pkl(folder/f"{ky}.pkl", v, is_force=is_force, verbose=verbose)

# load file from pkl
def load_pkl(fil, verbose=True):
    if verbose:
        print(f"Load file {fil}")
    with open(fil, "rb") as f:
        result = pickle.load(f)
    return result

# save file to pkl
def save_pkl(fil, result, is_force=False, verbose=True):
    if not fil.parent.exists():
        fil.parent.mkdir()
        if verbose:
            print(fil.parent)
            print(f"Create a folder {fil.parent}")
    if is_force or (not fil.exists()):
        if verbose:
            print(f"Save to {fil}")
        with open(fil, "wb") as f:
            pickle.dump(result, f)
    else:
        if verbose:
            print(f"{fil} exists! Use is_force=True to save it anyway")
        else:
            pass

        
def num2str(num, digits=3,
             sci_bds=[0.01, 1000], dp="d", mp="m"):
    """Return a string representation of a number with a given number of decimal places.
    for save file name
    if num is large 1e8, it will be converted to 1e8
    args: 
        - num (float): the number to be converted to a string
        - digits (int): the number of significant digits
        - sci_bds (list): the scientific bounds, smaller than sci_bds[0] or larger than sci_bds[1] will be converted to scientific notation
        - dp (str): the decimal place separator
        - mp (str): the minus sign
    return: 
        - strn (str): the string representation of the number
    """
    if num == 0:
        return "0"

    digits = int(digits)
    is_negative = num < 0
    num = np.abs(num)
    if num >= sci_bds[1] or num <= sci_bds[0]:
        strn = f"{num:.{digits}e}"
    elif num.is_integer():
        strn = f"{num:.0f}"
    else: 
        addn = 0
        if num < 0.1:
            log10num = np.log10(num)
            addn = np.floor(np.abs(log10num))
            if log10num.is_integer():
                addn = addn -1
            digits = digits + int(addn)
        strn = f"{num:.{digits}f}"
    strn = strn.lower()
    strn = strn.replace(".", dp)
    strn = strn.replace("-", mp)
    strn = strn.replace("+", "")
    # remove trailing zeros, if 8d0 then remove d0, if 1d800e10 then remove 00
    if dp in strn:
        if "e" not in strn:
            strn = strn.rstrip("0")
            if strn.endswith(dp):
                strn = strn[:-1]
        else: 
            p1, p2 = strn.split("e")
            p1 = p1.rstrip("0")
            if p1.endswith(dp):
                p1 = p1[:-1]
            strn = p1 + "e" + p2
    #remove the 0 in 1e08
    if "em0" in strn:
        p1, p2 = strn.split("em")
        p2 = p2.lstrip("0")
        strn = p1 + "em" + p2
    if "e0" in strn:
        p1, p2 = strn.split("e")
        p2 = p2.lstrip("0")
        strn = p1 + "e" + p2

    if is_negative:
        strn = mp + strn
    return strn


def str2num(s, dp="d", mp="m"): 
    """Given a string representation of a number, return the number
    """
    s = s.replace(dp, ".")
    s = s.replace(mp, "-")
    return float(s)

