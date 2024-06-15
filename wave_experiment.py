import firedrake as fd
import matplotlib.pyplot as plt
import numpy as np

from wavedrag.momentummodel import MomentumModel
from wavedrag.surfaceutils import getxsurface, getsurfacevelocityfunction, getboundaryelevation

SEC_PER_YR = 31556926.0
DAYS_PER_YR = 365.2422
BOUNDARY_IDS = {"outflow": 41, "top": [42, 44, 46], "inflow": 47, "base": [43, 45, 48]}

def plot_surface_vel(mesh, u):
    xs, _ = getxsurface(mesh, BOUNDARY_IDS["top"])
    L = max(xs)
    x = np.linspace(0, L, 401)
    s_fn = getboundaryelevation(mesh, BOUNDARY_IDS['top'])
    u_fn, w_fn = getsurfacevelocityfunction(mesh, BOUNDARY_IDS['top'], u)

    fig, axs = plt.subplots(nrows=2)
    axs[0].plot(x, u_fn(x)*SEC_PER_YR, label="horizontal velocity")
    axs[0].set_ylabel("u [m/yr]")

    axs[1].plot(x, w_fn(x)*SEC_PER_YR, label="vertical velocity")
    axs[1].plot([x[0], x[-1]], [0, 0], c='k')
    axs[1].set_ylabel("w [m/yr]")
    axs[1].set_xlabel("x [m]")

    for ax in axs:
        ax.legend()
    
    plt.savefig("temp.png")


def plot_solution_field(mesh, u):
    fig, ax = plt.subplots()
    fd.tricontourf(u, axes=ax)
    ax.set_aspect("equal")
    plt.savefig("other.pdf")

def compute_steady_state_mean_speed(
    mm: MomentumModel, mesh: fd.Mesh, x_min=750 * 2, x_max=750 * 3
):
    """Gets the mean speed for a cycle at steady state."""
    R = fd.FunctionSpace(mesh, "R", 0)
    one = fd.Function(R).assign(1.0)
    x, _ = fd.SpatialCoordinate(mesh)
    chi_s = fd.conditional(x < x_max, fd.conditional(x > x_min, one, 0), 0)

    # compute area of cycle
    area_cycle = fd.assemble(chi_s * fd.dx)

    # compute average velocity in cycle
    return fd.assemble(fd.sqrt(fd.dot(mm.u, mm.u)) * chi_s * fd.dx) / area_cycle


def solve_stokes(
    mesh_path,
    save_path: str = None,
    alpha: float = 0.1,
    Dtyp: float = 2.0,
    eps: float = 0.01,
    Hin: float = 400,
    Hout: float = 400
):
    """
    Args:
      mesh_path: input file name ending with .msh
      save_path: output file name ending with .pvd
      alpha: downward slope of bed as angle in radians
      Dtyp: regularize viscosity using `+(eps Dtype)^2`
      eps: regularize viscosity using `+(eps Dtyp)^2`.
      Hin: upstream thickness of ice.
      Hout: downstream thickness of ice.
    """
    mesh = fd.Mesh(mesh_path)
    mesh.topology_dm.viewFromOptions("-dm_view")

    model = MomentumModel(eps=eps, alpha=alpha, Dtyp_pera=Dtyp, Hin=Hin, Hout=Hout)

    u, p = model.solve(mesh, BOUNDARY_IDS).subfunctions
    avg_speed, max_avg_speed, avg_pressure, max_pressure = model.solutionstats(mesh)
    steady_speed = compute_steady_state_mean_speed(model, mesh)
    print(steady_speed*SEC_PER_YR)
    nu = model.effectiveviscosity(mesh)
    plot_surface_vel(mesh, u)
    plot_solution_field(mesh, u)
    if save_path is not None:
        fd.output.VTKFile(save_path).write(u, p, nu)


def run_experiment():
    mesh_path = "model/waves.msh"
    solve_stokes(mesh_path)


if __name__ == "__main__":
    run_experiment()
