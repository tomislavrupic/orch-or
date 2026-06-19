from __future__ import annotations

import unittest

from orch_or.geometry import (
    DEFAULT_GEOMETRY,
    collapse_time_for_domain,
    coherence_domain_mass_kg,
    compute_eg_gaussian_pair,
    compute_eg_diosi_regularized,
    compute_eg_quadrature_validation,
    compute_eg_uniform_cylinder,
)


class GeometryTests(unittest.TestCase):
    def test_default_geometry_is_bounded(self) -> None:
        self.assertEqual(DEFAULT_GEOMETRY.protofilaments, 13)
        self.assertEqual(DEFAULT_GEOMETRY.dimers_per_protofilament, 8)
        self.assertGreater(DEFAULT_GEOMETRY.mass_density_kg_m3, 0.0)

    def test_mass_scales_with_coherent_dimers(self) -> None:
        mass_13 = coherence_domain_mass_kg(DEFAULT_GEOMETRY, 13)
        mass_26 = coherence_domain_mass_kg(DEFAULT_GEOMETRY, 26)
        self.assertAlmostEqual(mass_26, 2.0 * mass_13)

    def test_eg_models_diverge(self) -> None:
        gaussian = compute_eg_gaussian_pair(DEFAULT_GEOMETRY, 13, 1.0e-9, 1.0e-9)
        cylinder = compute_eg_uniform_cylinder(DEFAULT_GEOMETRY, 13, 1.0e-9)
        quadrature = compute_eg_quadrature_validation(DEFAULT_GEOMETRY, 13, 1.0e-9)
        diosi = compute_eg_diosi_regularized(DEFAULT_GEOMETRY, 13, 1.0e-9, 1.0e-9)
        self.assertNotEqual(gaussian, cylinder)
        self.assertNotEqual(cylinder, quadrature)
        self.assertGreater(gaussian, 0.0)
        self.assertGreater(cylinder, 0.0)
        self.assertGreater(quadrature, 0.0)
        self.assertGreater(diosi, 0.0)
        self.assertLessEqual(diosi, gaussian)

    def test_collapse_helper_returns_energy_and_time(self) -> None:
        eg_j, tau_s = collapse_time_for_domain(
            DEFAULT_GEOMETRY,
            coherent_dimers=13,
            separation_m=1.0e-9,
            smearing_radius_m=1.0e-9,
            eg_model="gaussian",
        )
        self.assertGreater(eg_j, 0.0)
        self.assertGreater(tau_s, 0.0)


if __name__ == "__main__":
    unittest.main()
