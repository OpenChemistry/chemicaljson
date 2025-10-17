from __future__ import annotations

from typing import List, Optional

from pydantic.v1 import BaseModel, Field


class Elements(BaseModel):
    """List of elements for the atoms in the molecule.

    Length must match the number of atoms.
    """

    number: List[int] = Field(..., description="Required list of atomic numbers for the atoms in this file.")


class Coords(BaseModel):
    """Coordinates for the atoms in the molecule.

    Length must match the number of atoms*3 (x, y, z).
    """

    field3d: List[float] = Field(..., alias="3d", description="List of 3d Cartesian coordinates (in Angstrom) for the atoms [ x, y, z, x, y, z, ... ]")
    field3dFractional: Optional[List[float]] = Field(None, alias="3dFractional", description="Optional list of 3d fractional coordinates for the atoms [ x, y, z, x, y, z, ... ]")
    field3dSets: Optional[List[List[float]]] = Field(None, alias="3dSets", description="Optional list of lists of 3d Cartesian coordinates (in Angstrom) for the atoms [ [x, y, z], [x, y, z], ... ]")


class Atoms(BaseModel):
    """Atoms in the molecule."""

    elements: Elements = Field(..., description="List of atomic numbers for the atoms.")
    coords: Coords = Field(..., description="List of coordinates.")
    formalCharges: Optional[List[int]] = Field(None, description="Optional list of formal charges for the atoms.")
    labels: Optional[List[str]] = Field(None, description="Optional list of custom labels for atoms (e.g., 'R' / 'S' or '0.12', etc.)")
    layer: Optional[List[int]] = Field(None, description="Optional list of layer numbers for the atoms (generally just 1 for most molecules).")


class Connections(BaseModel):
    """Connections - list of connections between atom indices.

    Length must be the number of bonds * 2
    """

    index: List[int]


class Bonds(BaseModel):
    """
    Optional bonds between atoms, including connections and bond orders for the atoms in the molecule. (Optional)
    """

    connections: Connections
    order: List[int]


class BasisSet(BaseModel):
    """Basis Set information (optional)

    At the moment, implied to be Gaussian basis sets.
    """

    coefficients: List[float] = Field(..., description="List of coefficients for the basis functions.")
    exponents: List[float] = Field(..., description="List of exponents for the basis functions.")
    primitivesPerShell: List[int] = Field(..., description="List of number of primitives per shell.")
    shellToAtomMap: List[int] = Field(..., description="List of atom indices for the basis functions.")
    shellTypes: List[int] = Field(..., description="List of shell types for the basis functions (l-value, so s=0, p=1, d=2, etc.).")


class Orbitals(BaseModel):
    """Information about molecular orbital energies and coefficients. (Optional)
    
    To be useful, this should include basis set information, electronCount, energies, 
    """

    electronCount: int = Field(..., description="Number of electrons in the species")
    energies: Optional[List[float]] = Field(None, description="List of energies for the molecular orbitals (in eV)")
    moCoefficients: Optional[List[float]] = Field(None, description="List of coefficients (flattened) for restricted molecular orbitals, i.e., alpha=beta (requires BasisSet to be present).")
    alphaCoefficients: Optional[List[float]] = Field(None, description="List of coefficients (flattened) for alpha open-shell orbitals, (requires BasisSet to be present).")
    betaCoefficients: Optional[List[float]] = Field(None, description="List of coefficients (flattened) for beta open-shell orbitals, (requires BasisSet to be present).")
    occupations: Optional[List[int]] = Field(None, description="List of occupations for the molecular orbitals")
    symmetries: Optional[List[List[str]]] = Field(None, description="Symmetry of the orbital (e.g., a1, eg, t1g, etc.)")


class Electronic(BaseModel):
    """Electronic spectra (optional)"""

    energies: List[float] = Field(..., description="List of excitation energies for the electronic spectra (in eV)")
    intensities: List[float] = Field(..., description="List of intensities for the electronic spectra")
    rotation: Optional[List[float]] = Field(None, description="Optional list of rotation angles for the CD spectra (in degrees)")


class Nmr(BaseModel):
    """NMR spectra (optional)"""

    shifts: List[float] = Field(..., description="List of absolute chemical shifts for the NMR spectra (in ppm)")


class Spectra(BaseModel):
    """Spectra (optional)

    Objects for non-vibrational spectra, including electronic, NMR, and other spectra.
    """

    electronic: Optional[Electronic] = Field(None, description="Optional electronic spectra")
    nmr: Optional[Nmr] = Field(None, description="Optional NMR spectra")


class Properties(BaseModel):
    """Properties of the molecule / system. (Optional)

    A set of key-value properties.
    """

    molecularMass: Optional[float] = None
    meltingPoint: Optional[float] = None
    boilingPoint: Optional[float] = None
    totalCharge: Optional[int] = Field(0, description="Total charge of the system. If omitted, assume 0 (charge neutral)")
    totalSpinMultiplicity: Optional[int] = Field(1, description="Total spin multiplicity of the system (2S+1, e.g., 1, 2, 3, etc.). If omitted, assume to be 1 (singlet)")
    totalEnergy: Optional[float] = Field(None, description="Optional total energy of the system in eV")


class Metadata(BaseModel):
    """Metadata for the calculation. (Optional)

    Attributes:
        runDate: date calculation was done
    """
    runDate: Optional[str] = None

class InputParameters(BaseModel):
    """Input parameters for the calculation. (Optional)

    Attributes:
        basis: Basis set used for the calculation (e.g. "6-31G(d)" or "Custom").
        dispersion: Dispersion correction used for the calculation (e.g. "D3" or "D3BJ")
        functional: Functional used for the calculation if DFT (e.g. "B3LYP" or "Custom").
        grid: Keyword describing the DFT grid keyword usedf if DFT.
        memory: The amount of memory requested for the calculation.
        processors: The number of processors requested for the calculation.
        task: "Energy" or "Optimize" or "Frequencies" or "Transition State" or "Custom".
        theory: Method used for the calculation (e.g. "DFT" or "HF" or "MP2").
    """

    basis: Optional[str] = None
    dispersion: Optional[str] = None
    functional: Optional[str] = None
    grid: Optional[str] = None
    memory: Optional[str] = None
    processors: Optional[str] = None
    task: Optional[str] = None
    theory: Optional[str] = None


class PartialCharges(BaseModel):
    """Partial charges for the atoms in the molecule. (Optional)

    Keys represent the partial charge method, followed by the computed partial charges.
    e.g.
    - "Mulliken": [ 0.01, 0.02, 0.03, ... ]
    - "Gasteiger": [ 0.01, 0.02, 0.03, ... ]
    """

    mulliken: List[float]


class UnitCell(BaseModel):
    """Unit cell for the system. (Optional)

    Current versions of Avogadro will output and preferentially use cellVectors,
    since they fully specify the unit cell, but will also output a, b, c,
    alpha, beta, gamma parameters and use them if no cellVectors field is found.
    """

    a: float = Field(..., description="Unit cell a-axis length (in Angstrom).")
    b: float = Field(..., description="Unit cell b-axis length (in Angstrom).")
    c: float = Field(..., description="Unit cell c-axis length (in Angstrom).")
    alpha: float = Field(..., description="Unit cell alpha angle (in degrees).")
    beta: float = Field(..., description="Unit cell beta angle (in degrees).")
    gamma: float = Field(..., description="Unit cell gamma angle (in degrees).")
    cellVectors: Optional[List[float]] = Field(
        min_items=9, max_items=9, default_factory=lambda: [0.0 for _ in range(9)], description="Optional list of cell vectors (in Angstrom): [ x1, y1, z1, x2, y2, z2, ... ]"
    )


class Vibrations(BaseModel):
    """Vibrations for the molecule. (Optional)

    Attributes:
        ramanIntensities: Optional list of Raman intensities for the vibrations.
        modes: Optional list of mode numbers (e.g, [ 1, 2, 3, 4, 5, 6, ... ])
        symmetries: Optional list of symmetries for the vibrations (e.g., 'a1g', 'eg' ...)
    """

    frequencies: List[float] = Field(... , description="List of frequencies (in cm-1) for the vibrations.")
    intensities: List[float] = Field(... , description="List of IR intensities for the vibrations.")
    eigenVectors: List[List[float]] = Field(..., description="List of eigenvectors (displacements in Angstroms) for the vibrations.")
    ramanIntensities: Optional[List[float]]
    symmetries: Optional[List[str]]
    modes: Optional[List[int]]


class Enable(BaseModel):
    """Optional enable flags for different render types for each layer

    Length of each much match the number of layers.
    """

    ballAndStick: Optional[List[bool]] = Field(alias="Ball and Stick")
    cartoons: Optional[List[bool]]
    closeContacts: Optional[List[bool]] = Field(alias="Close Contacts")
    labels: Optional[List[bool]]
    licorice: Optional[List[bool]]
    vanDerWaals: Optional[List[bool]] = Field(alias="Van der Waals")
    wireframe: Optional[List[bool]]


class Settings(BaseModel):
    """Settings for the render types. (Optional)"""

    ballAndStick: Optional[List[str]] = Field(alias="Ball and Stick", description="Settings for the Ball and Stick rendering type")
    cartoons: Optional[List[str]]
    wireframe: Optional[List[str]]


class Layer(BaseModel):
    """Layer settings for the molecule. (Optional)

    Attributes:
        enable: Enable flags for different render types for each layer.
        settings: Settings for the render types.
        locked: List of locked layers (e.g., atoms in this layer should not change)
        visible: List of visible layers (e.g., atoms in this layer should be visible / invisible)
    """

    enable: Enable
    locked: List[bool]
    settings: Settings
    visible: List[bool]


class CJSONModel(BaseModel):
    """Full Chemical JSON model.

    A Chemical JSON (CJSON) model is intended to represent one molecular or periodic system.
    Catenating multiple systems will result in invalid JSON - store separate systems as
    separate files / JSON entries.

    Attributes:
        vibrations: Vibrations object. Optional.
        unitCell: UnitCell object. Optional.
        layer: Layer object. Optional (used by the GUI for rendering / settings)
        basisSet: BasisSet object. Optional.
        orbitals: Orbitals object. Optional. Requires BasisSet to be present.
    """

    chemicalJson: int = Field(1, description="Version number of the Chemical JSON format. Currently 1. Only changed for backwards-incompatible changes to the schema.")
    atoms: Atoms = Field(..., description="Atoms object, describing the atoms in this system.")
    name: Optional[str] = Field(None, description="Optional name / title for the molecule")
    inchi: Optional[str] = Field(None, description="Optional InChI descriptor for the molecule")
    formula: Optional[str] = Field(None, description="Optional chemical formula in Hill order")
    bonds: Optional[Bonds] = Field(None, description="Optional Bonds object, describing covalent bonds")
    properties: Optional[Properties] = Field(None, description="Optional free-form Properties, including total charge and total spin multiplicity.")
    inputParameters: Optional[InputParameters] = Field(None, description="Optional InputParameters object, including calculation metadata such as basis set, job type, etc.")
    metadata: Optional[Metadata] = Field(None, description="Optional metadata object, including calculation details which do not directly impact results")
    partialCharges: Optional[PartialCharges] = Field(None, description="Optional PartialCharges object. Includes atomic partial charges and population analysis.")
    vibrations: Optional[Vibrations] = None
    unitCell: Optional[UnitCell] = None
    layer: Optional[Layer] = None
    basisSet: Optional[BasisSet] = None
    orbitals: Optional[Orbitals] = None
    spectra: Optional[Spectra] = None


if __name__ == "__main__":
    with open("cjson.schema", "w") as handle:
        handle.write(CJSONModel.schema_json(indent=2))
        handle.write("\n")
