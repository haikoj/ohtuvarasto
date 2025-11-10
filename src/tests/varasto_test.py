import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):

    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)
        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)
        saatu_maara = self.varasto.ota_varastosta(2)
        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)
        self.varasto.ota_varastosta(2)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_negatiivinen_tilavuus(self):
        v = Varasto(-1)
        self.assertAlmostEqual(v.tilavuus, 0)

    def test_negatiivinen_alkusaldo(self):
        v = Varasto(10, -1)
        self.assertAlmostEqual(v.saldo, 0)

    def test_alkusaldo_yli(self):
        v = Varasto(10, 15)
        self.assertAlmostEqual(v.saldo, 10)

    def test_negatiivinen_lisays(self):
        self.varasto.lisaa_varastoon(5)
        self.varasto.lisaa_varastoon(-1)
        self.assertAlmostEqual(self.varasto.saldo, 5)

    def test_lisays_yli(self):
        self.varasto.lisaa_varastoon(12)
        self.assertAlmostEqual(self.varasto.saldo, 10)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 0)

    def test_otto_negatiivinen(self):
        self.varasto.lisaa_varastoon(3)
        saatu = self.varasto.ota_varastosta(-1)
        self.assertAlmostEqual(saatu, 0.0)
        self.assertAlmostEqual(self.varasto.saldo, 3)

    def test_otto_yli_saldon(self):
        self.varasto.lisaa_varastoon(4)
        saatu = self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(saatu, 4)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_str(self):
        self.varasto.lisaa_varastoon(2)
        self.assertEqual(str(self.varasto), "saldo = 2, vielä tilaa 8")
