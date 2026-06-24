from functools import lru_cache


@lru_cache(maxsize=1)
def _robjects():
    try:
        from rpy2 import robjects
    except ImportError as exc:
        raise ImportError(
            "rpy2 is required for jin_utils.rpy2_utils. "
            "Install it with: pip install 'jin_utils[rpy2]' or pip install rpy2"
        ) from exc
    return robjects


def array2d2Robj(mat):
    """
    Converts a 2D numpy array to an R matrix object.

    Args:
        mat (numpy.ndarray): A 2D numpy array.

    Returns:
        r.matrix: An R matrix object.
    """
    robj = _robjects()
    mat_vec = mat.reshape(-1)
    mat_vecR = robj.FloatVector(mat_vec)
    matR = robj.r.matrix(mat_vecR, nrow=mat.shape[0], ncol=mat.shape[1], byrow=True)
    return matR
