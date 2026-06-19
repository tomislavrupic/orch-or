from __future__ import annotations

import unittest

from orch_or.geometry import (
    DEFAULT_GEOMETRY,
    CoordinateMassCloud,
    collapse_time_for_domain,
    coordinate_cloud_from_points,
    cylinder_mass_density_from_cloud,
    coherence_domain_mass_kg,
    compute_eg_gaussian_pair,
    compute_eg_diosi_regularized,
    compute_eg_quadrature_validation,
    compute_eg_uniform_cylinder,
    gaussian_smearing_radius_from_cloud,
)


class GeometryTests(unittest.TestCase):
    def test_default_geometry_is_bounded(self) -> None:
        self.assertEqual(DEFAULT_GEOMETRY.protofilaments, 13)
        self.assertEqual(DEFAULT_GEOMETRY.dimers_per_protofilament, 8)
        self.assertGreater(DEFAULT_GEOMETRY.mass_density_kg_m3, 0.0)

    def test_default_geometry_total_dimers_matches_lattice(self) -> None:
        self.assertEqual(DEFAULT_GEOMETRY.total_dimers, 104)

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

    def test_coordinate_cloud_mass_proxy(self) -> None:
        cloud = coordinate_cloud_from_points(
            points_m=((0.0, 0.0, 0.0), (1.0e-9, 0.0, 0.0), (0.0, 1.0e-9, 0.0)),
            masses_kg=(1.0, 1.0, 1.0),
        )
        self.assertIsInstance(cloud, CoordinateMassCloud)
        self.assertAlmostEqual(cloud.total_mass_kg, 3.0)
        self.assertGreater(cloud.rms_radius_m(), 0.0)
        self.assertGreater(gaussian_smearing_radius_from_cloud(cloud), 0.0)
        self.assertAlmostEqual(cylinder_mass_density_from_cloud(cloud, 3.0), 1.0)


if __name__ == "__main__":
    unittest.main()
