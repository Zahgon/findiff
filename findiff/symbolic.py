from sympy import Add, IndexedBase, Matrix, Rational, Symbol, factorial, linsolve


class SymbolicMesh:

    def __init__(self, coord, equidistant=True):
        """Constructor.

        Parameters
        ----------
        coord: str
            A comma-separated string of coordinate names for the mesh,
            e.g. "x,y" or simply "x"

        equidistant: bool
            Flag indicating whether the mesh is equidistant.
        """
        assert isinstance(coord, str)

        self.equidistant = equidistant
        self._coord_names = [n.replace(" ", "") for n in coord.split(",")]
        self._coord = [IndexedBase(name) for name in self._coord_names]

    @property
    def ndims(self):
        pass

    @property
    def coord(self):
        pass

    @property
    def spacing(self):
        pass

    @staticmethod
    def create_symbol(name):
        pass


class SymbolicDiff:

    def __init__(self, mesh, axis=0, degree=1):
        """Constructor

        Parameters
        ----------
        mesh: SymbolicMesh
            The symbolic grid on which to evaluate the derivative.
        axis: int
            The index of the axis with respect to which to differentiate.
        degree: int > 0
            The degree of the partial derivative.

        """
        self.mesh = mesh
        self.axis = axis
        self.degree = degree

    def __call__(self, f, at, offsets):
        if not isinstance(at, tuple) and not isinstance(at, list):
            at = [at]

        if self.mesh.ndims != len(at):
            raise ValueError("Index tuple must match the number of dimensions!")

        coefs = self._compute_coefficients(f, at, offsets)
        terms = []
        for coef, off in zip(coefs, offsets):
            inds = list(at)
            inds[self.axis] += off
            inds = tuple(inds)
            terms.append(coef * f[inds])

        return Add(*terms).simplify()

    def _compute_coefficients(self, f, at, offsets):
        pass
